import sqlite3
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def get_par_unit_mappings():
    """Get dataframe mapping parameters and units as reported by Vestfold Lab and Eurofins
        to those used in Vannmiljø.

    Args:
        None

    Returns:
        Dataframe.
    """
    df = pd.read_excel(
        r"../../data/parameter_unit_mapping.xlsx",
        sheet_name="vestfoldlab_to_vannmiljo",
        keep_default_na=False,
    )

    return df


def read_data_template(file_path, sheet_name="Ark1", lab="VestfoldLAB"):
    """Read lab data from the agreed template. An example of the template is here:

            ../../data/vestfold_lab_data_to_2020-08-31.xls

        Also converts units and parameter names to match those in Vannmiljø.

    Args:
        file_path:  Raw str. Path to Excel template
        sheet_name: Str. Name of sheet to read
        lab:        Str. Name of lab. One of ['VestfoldLAB', 'Eurofins']

    Returns:
        Dataframe.
    """
    assert lab in [
        "VestfoldLAB",
        "Eurofins",
    ], "'lab' must be one of ['VestfoldLAB', 'Eurofins']."

    # Read reference station details
    stn_df = pd.read_excel(r"../../data/active_stations_2020.xlsx", sheet_name="data")

    # Read data
    par_df = get_par_unit_mappings()

    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        skiprows=1,
        usecols="C,D,F,G,I:AB",
        header=None,
    )

    # Parse header
    header = df[:2]
    df = df[2:]
    first = header.loc[1].tolist()[:4]
    pars = header.loc[0].tolist()[4:]
    units = header.loc[1].tolist()[4:]
    pars_units = [f"{par}_{unit}" for par, unit in zip(pars, units)]
    df.columns = first + pars_units

    df.rename(
        {
            "Lokalitets-ID": "vannmiljo_code",
            "Prøvested": "station_name",
            "Prøvedato": "sample_date",
            "Dybde": "depth1",
        },
        inplace=True,
        axis="columns",
    )

    # Check station ID have consistent names
    print("\nThe following location IDs have inconsistent names within this template:")
    site_ids = df["vannmiljo_code"].unique()
    for site_id in site_ids:
        true_name = stn_df.query("vannmiljo_code == @site_id")["station_name"].values
        names = df.query("vannmiljo_code == @site_id")["station_name"].unique()

        if len(names) > 1:
            print("    ", f"{site_id} {true_name}", "  ==>  ", names)

    # Check station names have consistent IDs
    print("\nThe following location names have multiple IDs within this template:")
    site_names = df["station_name"].unique()
    for site_name in site_names:
        true_id = stn_df.query("station_name == @site_name")["vannmiljo_code"].values
        ids = df.query("station_name == @site_name")["vannmiljo_code"].unique()

        if len(ids) > 1:
            print("    ", f"{site_name} {true_id}", "  ==>  ", ids)

    # Assume no mixed/integrated samples
    df["depth2"] = df["depth1"]

    # Parse dates
    df["sample_date"] = pd.to_datetime(df["sample_date"], format="%d.%m.%Y")

    # Get pars of interest
    cols = [
        f"{par}_{unit}"
        for par, unit in zip(
            par_df[f"{lab.lower()}_name"], par_df[f"{lab.lower()}_unit"]
        )
    ]
    df = df[["vannmiljo_code", "sample_date", "depth1", "depth2"] + cols]

    # Melt to long format
    df = pd.melt(
        df,
        id_vars=["vannmiljo_code", "sample_date", "depth1", "depth2"],
        var_name="par_unit",
    )
    df.dropna(subset=["value"], inplace=True)
    df["flag"] = np.where(df["value"].astype(str).str.contains("<"), "<", np.nan)
    df["value"] = pd.to_numeric(df["value"].astype(str).str.strip("<"))
    df["lab"] = lab

    # Convert to VM par names and units
    par_df["par_unit"] = (
        par_df[f"{lab.lower()}_name"] + "_" + par_df[f"{lab.lower()}_unit"]
    )
    par_df["vm_par_unit"] = par_df["vannmiljo_id"] + "_" + par_df["vannmiljo_unit"]

    df = pd.merge(
        df,
        par_df[["par_unit", "vm_par_unit", f"{lab.lower()}_to_vm_conv_fac"]],
        how="left",
        on="par_unit",
    )

    df["value"] = df["value"] * df[f"{lab.lower()}_to_vm_conv_fac"]

    # Assume depth is 0 unless otherwise stated
    df["depth1"].fillna(0, inplace=True)
    df["depth2"].fillna(0, inplace=True)

    df = df[
        [
            "vannmiljo_code",
            "sample_date",
            "lab",
            "depth1",
            "depth2",
            "vm_par_unit",
            "flag",
            "value",
        ]
    ]

    df.rename({"vm_par_unit": "par_unit"}, inplace=True, axis="columns")

    assert pd.isna(df).sum().sum() == 0, "Dataframe contains missing values."

    df = df.astype(
        {
            "vannmiljo_code": "str",
            "sample_date": "datetime64",
            "lab": "str",
            "depth1": "float",
            "depth2": "float",
            "par_unit": "str",
            "flag": "str",
            "value": "float",
        }
    )

    return df


def read_historic_data(file_path):
    """Read historic data exported from Vannmiljø.

     Args:
        file_path:  Raw str. Path to Excel template

    Returns:
        Dataframe.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        df = pd.read_excel(
            file_path,
            sheet_name="VannmiljoEksport",
            #usecols="A:I,Q:U,W", # For use with Vannmiljø files exported before July 2021
            usecols="A:J,R:W,Y", # Compatible with new Vannmiljø layout (August 2021 onwards)
            keep_default_na=False,
        )

        # Get just the monitoring project of interest
        df = df.query("Aktivitet_id == 'KALK'")

        # Tidy
        df["par_unit"] = df["Parameter_id"] + "_" + df["Enhet"]
        df["value"] = pd.to_numeric(df["Verdi"].str.replace(",", "."))

        for col in ["Ovre_dyp", "Nedre_dyp"]:
            df[col] = pd.to_numeric(df[col])

        df.drop(
            [
                "Vannlokalitet",
                "Type",
                "Aktivitet_id",
                "Aktivitet_navn",
                "Oppdragsgiver",
                "Parameter_navn",
                "Parameter_id",
                "Enhet",
                "Verdi",
            ],
            inplace=True,
            axis="columns",
        )

        df.rename(
            {
                "Vannlokalitet_kode": "vannmiljo_code",
                "Oppdragstaker": "lab",
                "Tid_provetak": "sample_date",
                "Ovre_dyp": "depth1",
                "Nedre_dyp": "depth2",
                "Operator": "flag",
            },
            inplace=True,
            axis="columns",
        )

        # Parse dates
        df["sample_date"] = pd.to_datetime(
            df["sample_date"], format="%Y-%m-%d %H:%M:%S"
        )

        # Tidy
        df["depth1"].fillna(0, inplace=True)
        df["depth2"].fillna(0, inplace=True)
        df["flag"].fillna("", inplace=True)

        # Cols of interest
        df = df[
            [
                "vannmiljo_code",
                "sample_date",
                "lab",
                "depth1",
                "depth2",
                "par_unit",
                "flag",
                "value",
            ]
        ]

        assert pd.isna(df).sum().sum() == 0, "Dataframe contains missing values."

        df = df.astype(
            {
                "vannmiljo_code": "str",
                "sample_date": "datetime64",
                "lab": "str",
                "depth1": "float",
                "depth2": "float",
                "par_unit": "str",
                "flag": "str",
                "value": "float",
            }
        )

    return df


def check_data_ranges(df):
    """Takes a tidied dataframe and checks for values outside of the ranges specified in
        parameter_unit_mapping.xlsx. Assumes values should be in the range

        min < value < max

        (i.e. not <=). The checks are split by 'parameter' and 'period'.

    Args:
        df: Dataframe. Containing water chemistry

    Returns:
        Dataframe with problem rows in historic time period removed.
    """
    for col in ["parameter", "period", "value"]:
        assert col in df.columns, f"Dataframe must contain a column named {col}"

    assert set(df["period"].unique()) == set(
        ["historic", "new"]
    ), "'period' must contain only 'historic' or 'new'."

    # Get min and max values
    par_df = get_par_unit_mappings()

    for period in ["historic", "new"]:
        print(f"\nChecking data ranges for the '{period}' period.")
        for idx, row in par_df.iterrows():
            par = row["vannmiljo_id"]
            par_min = row["min"]
            par_max = row["max"]
            data_min = df.query("(period == @period) and (parameter == @par)")[
                "value"
            ].min()
            data_max = df.query("(period == @period) and (parameter == @par)")[
                "value"
            ].max()

            if data_min <= par_min:
                print(
                    f"    {par}: Minimum value of {data_min:.2f} is less than or equal to lower limit ({par_min:.2f})."
                )

            if data_max >= par_max:
                print(
                    f"    {par}: Maximum value of {data_max:.2f} is greater than or equal to upper limit ({par_max:.2f})."
                )

    # Remove values outside of plausible ranges from historic dataset
    print("\nDropping problem rows from historic data.")
    for idx, row in par_df.iterrows():
        par = row["vannmiljo_id"]
        par_min = row["min"]
        par_max = row["max"]

        drop_df = df.query(
            "(parameter == @par) and "
            "(period == 'historic') and "
            "((value <= @par_min) or (value >= @par_max))"
        )

        if len(drop_df) > 0:
            print(f"    Dropping rows for {par}.")
            df.drop(drop_df.index, axis="rows", inplace=True)

    return df


def read_data_from_sqlite():
    """Convenience function for reading all water chemistry data (historic and new)
        from the database.

    Returns:
        Tuple of dataframes (stn_df, wc_df)
    """
    # Connect to database
    dbname = "kalk_data.db"
    eng = sqlite3.connect(dbname, detect_types=sqlite3.PARSE_DECLTYPES)

    # Read tables
    stn_df = pd.read_sql("SELECT * FROM stations", eng)
    par_df = pd.read_sql("SELECT * FROM parameters_units", eng)
    wc_df = pd.read_sql("SELECT * FROM water_chemistry", eng)
    wc_df["sample_date"] = pd.to_datetime(
        wc_df["sample_date"], format="%Y-%m-%d %H:%M:%S"
    )

    # Combine pars and units into one column
    wc_df["par_unit"] = wc_df["parameter"] + "_" + wc_df["unit"]
    wc_df.drop(["parameter", "flag", "unit"], axis="columns", inplace=True)

    # Convert to wide format
    df = wc_df.set_index(
        [
            "vannmiljo_code",
            "sample_date",
            "lab",
            "period",
            "depth1",
            "depth2",
            "par_unit",
        ]
    ).unstack("par_unit")

    # Tidy
    df.columns = df.columns.get_level_values(1)
    df.reset_index(inplace=True)
    df.columns.name = ""

    return (stn_df, df)


def isolation_forest(df, par_cols, contamination=0.01, random_state=42):
    """Apply sklearn's Isolation Forest algorithm.

    Args:
        df:            Dataframe. Samples to be classified
        par_cols:      List of str. Numeric columns to use for outlier detection
        contamination: Float. Proportion of total samples expected to be 'outliers'
        random_state:  Int. Initialisation state for random forest (for repeatability)

    Returns:
        Copy of df with new column names 'outlier' added.
    """
    assert pd.isna(df).sum().sum() == 0, "Dataframe cannot contain missing values."

    # Run Iso Forest
    iso = IsolationForest(contamination=contamination, random_state=random_state)
    df["pred"] = iso.fit_predict(df[par_cols])
    df["pred"].replace({1: "inlier", -1: "outlier"}, inplace=True)

    return df
