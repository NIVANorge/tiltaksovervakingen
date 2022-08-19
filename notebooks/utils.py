import os
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
        sheet_name="to_vannmiljo",
        keep_default_na=False,
    )

    return df


def read_data_template_to_wide(file_path, sheet_name="Ark1", lab="VestfoldLAB"):
    """Read lab data from the agreed template in 'wide' format. An example of
    the template is here:

            ../../data/vestfold_lab_data_to_2020-08-31.xls

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

    # Tidy
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
    df["depth1"].fillna(0, inplace=True)  # Assume depth is 0 unless otherwise stated
    df["depth2"] = df["depth1"]  # Assume no mixed/integrated samples
    df["sample_date"] = pd.to_datetime(df["sample_date"], format="%d.%m.%Y")

    # Get pars of interest
    cols = [
        f"{par}_{unit}"
        for par, unit in zip(
            par_df[f"{lab.lower()}_name"], par_df[f"{lab.lower()}_unit"]
        )
    ]
    df = df[
        ["vannmiljo_code", "station_name", "sample_date", "depth1", "depth2"] + cols
    ]

    return df


def perform_basic_checks(df):
    """Perform basic checks using 'wide' template data.

    Args:
        df: Dataframe of tidied template data in 'wide' format

    Returns:
        None. Possible issues are printed to output.
    """
    stn_df = pd.read_excel(r"../../data/active_stations_2020.xlsx", sheet_name="data")

    check_stations(df, stn_df)
    check_quarter(df)
    check_numeric(df)
    check_greater_than_zero(df)
    check_lod_consistent(df)
    check_no3_totn(df)
    check_ral_ilal_lal(df)

    return None


def wide_to_long(df, lab):
    """Converts 'wide' format data to 'long' format, including parsing of LOD
    flags and conversion of units to match Vannmiljø.

    Args:
        df:     Dataframe of tidied 'wide' format water chemistry data
        lab:    Str. Name of lab submitting data

    Returns:
        Dataframe.
    """
    par_df = get_par_unit_mappings()

    del df["station_name"]
    df = pd.melt(
        df,
        id_vars=["vannmiljo_code", "sample_date", "depth1", "depth2"],
        var_name="par_unit",
    )
    df.dropna(subset=["value"], inplace=True)
    df["flag"] = np.where(df["value"].astype(str).str.contains("<"), "<", np.nan)
    df["value"] = pd.to_numeric(
        df["value"].astype(str).str.strip("<").str.replace(",", ".")
    )
    df["lab"] = lab

    df = convert_units_to_vannmiljo(df, par_df, lab)

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


def check_numeric(df):
    """Check that relevant columns in 'df' contain numeric data. LOD values
    beginning with '<' are permitted.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output. Raises a ValueError
        if data cannot be parsed
    """
    print("\nChecking for non-numeric data:")
    non_num_cols = ["vannmiljo_code", "station_name", "sample_date"]
    num_cols = [col for col in df.columns if col not in non_num_cols]
    n_errors = 0
    for col in num_cols:
        num_series = pd.to_numeric(
            df[col].fillna(-9999).astype(str).str.strip("<").str.replace(",", "."),
            errors="coerce",
        )
        non_num_vals = df[pd.isna(num_series)][col].values
        if len(non_num_vals) > 0:
            n_errors += 1
            print(f"    {col} contains non-numeric values: {non_num_vals}")

    if n_errors > 0:
        raise ValueError(
            "The template contains non-numeric data (see above). Please fix these issues before continuing."
        )
    else:
        print("    Done.")

    return None


def check_greater_than_zero(df):
    """Check that relevant columns in 'df' contain values greater than zero.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    print("\nChecking for values less than zero:")
    gt_zero_cols = [
        "pH_enh",
        "Kond_ms/m",
        "Alk_mmol/l",
        "Tot-P_µg/l",
        "Tot-N_µg/l",
        "NO3_µg/l",
        "TOC_mg/l",
        "RAl_µg/l",
        "ILAl_µg/l",
        "Cl_mg/l",
        "SO4_mg/l",
        "Ca_mg/l",
        "K_mg/l",
        "Mg_mg/l",
        "Na_mg/l",
        "SIO2_µg/l",
    ]
    n_errors = 0
    for col in gt_zero_cols:
        num_series = pd.to_numeric(
            df[col].fillna(-9999).astype(str).str.strip("<").str.replace(",", ".")
        )
        num_series[num_series == -9999] = np.nan
        if num_series.min() <= 0:
            n_errors += 1
            print(f"    {col} contains values less than or equal to zero.")

    if n_errors == 0:
        print("    Done.")

    return None


def check_lod_consistent(df):
    """Check that the LOD for each parameter in 'df' is consistent.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    print("\nChecking for consistent LOD values:")
    n_errors = 0
    for col in df.columns:
        lods = df[df[col].astype(str).str.contains("<")][col].unique()
        if len(lods) > 1:
            n_errors += 1
            print(f"    {col} contains multiple LOD values: {lods}.")

    if n_errors == 0:
        print("    Done.")

    return None


def check_stations(df, stn_df):
    """Basic check of station data in 'df' against reference data in 'stn_df'.

    Args:
        df:     Dataframe of sumbitted water chemistry data
        stn_df: Dataframe of reference station details

    Returns:
        None. Problems identified are printed to output.
    """
    print("\nChecking stations:")
    if not set(df["vannmiljo_code"]).issubset(set(stn_df["vannmiljo_code"])):
        print(
            "The following location IDs in the new data are not in the definitive station list."
        )
        print(set(df["vannmiljo_code"]) - set(stn_df["vannmiljo_code"]))

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

    return None


def check_quarter(df):
    """Check all samples come from the same year quarter.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    print("\nChecking sample dates:")
    quarters = df["sample_date"].dt.quarter
    if len(quarters.unique()) > 1:
        print("    The file contains samples from several year quarters.")
    else:
        print("    Done.")

    return None


def check_no3_totn(df):
    """Check nitrate < TOTN.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    print("\nChecking NO3 and TOTN:")
    mask_df = df[
        [
            "vannmiljo_code",
            "sample_date",
            "depth1",
            "depth2",
            "NO3_µg/l",
            "Tot-N_µg/l",
        ]
    ].copy()

    for col in ["NO3_µg/l", "Tot-N_µg/l"]:
        mask_df[col].fillna(0, inplace=True)
        mask_df[col] = pd.to_numeric(
            mask_df[col].astype(str).str.strip("<").str.replace(",", ".")
        )
    mask = mask_df["NO3_µg/l"] > mask_df["Tot-N_µg/l"]
    mask_df = mask_df[mask]

    if len(mask_df) > 0:
        print("The following samples have nitrate greater than total nitrogen:")
        print(mask_df)
    else:
        print("    Done.")

    return None


def check_ral_ilal_lal(df):
    """Check RAl - ILAl = LAl.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    print("\nChecking Al fractions:")
    mask_df = df[
        [
            "vannmiljo_code",
            "sample_date",
            "depth1",
            "depth2",
            "RAl_µg/l",
            "ILAl_µg/l",
            "LAl_µg/l",
        ]
    ].copy()
    mask_df.dropna(subset="LAl_µg/l", inplace=True)

    for col in ["RAl_µg/l", "ILAl_µg/l", "LAl_µg/l"]:
        mask_df[col].fillna(0, inplace=True)
        mask_df[col] = pd.to_numeric(
            mask_df[col].astype(str).str.strip("<").str.replace(",", ".")
        )
    mask_df["LAl_Calc_µg/l"] = (mask_df["RAl_µg/l"] - mask_df["ILAl_µg/l"]).round(1)
    mask_df["LAl_µg/l"] = mask_df["LAl_µg/l"].round(1)
    mask = mask_df["LAl_Calc_µg/l"] != mask_df["LAl_µg/l"]
    mask_df = mask_df[mask]

    if len(mask_df) > 0:
        print("The following samples have LAl != RAl - ILAl:")
        print(mask_df)
    else:
        print("    Done.")

    return None


def convert_units_to_vannmiljo(df, par_df, lab):
    """Convert to VM par names and units.

    Args:
        df:     Dataframe of sumbitted water chemistry data
        par_df: Dataframe of reference parameters
        lab:    Str. Name of lab submitting data

    Returns:
        Dataframe in converted units.
    """
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

    return df


def read_historic_data(file_path, st_yr=2012, end_yr=2020):
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
            # usecols="A:I,Q:U,W", # For use with Vannmiljø files exported before July 2021
            # usecols="A:J,R:W,Y",  # Compatible with Vannmiljø layout (August 2021  - August 2022)
            usecols="A:J,R:T,V,X:Y,AA",  # Compatible with Vannmiljø layout (August 2022  - onwards)
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
        
        # Subset to date range
        df = df.query(f"'{st_yr}-01-01' <= sample_date <= '{end_yr}-12-31'")

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


def handle_duplicates(df, dup_csv, action="drop"):
    """ """
    assert action in ("drop", "average"), "'action' must be either 'drop' or 'average'."

    key_cols = [
        "vannmiljo_code",
        "sample_date",
        # "lab",
        "depth1",
        "depth2",
        "par_unit",
    ]
    dup_df = df[
        df.duplicated(
            key_cols,
            keep=False,
        )
    ].sort_values(key_cols)
    dup_df.to_csv(dup_csv, index=False)

    if action == "average":
        df = (
            df.groupby(key_cols)
            .aggregate(
                {
                    "flag": "first",
                    "value": "mean",
                }
            )
            .reset_index()
        )
        past_action = "averaged"
    else:
        # Drop
        df.drop_duplicates(subset=key_cols, keep=False, inplace=True)
        past_action = "dropped"

    print(
        f"\nThere are {len(dup_df)} duplicated records (same station_code-date-depth-parameter, but different value).\n"
        f"These will be {past_action}.\n"
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


def read_data_from_sqlite(lab, year, qtr, version):
    """Convenience function for reading all water chemistry data (historic and new)
        from the database.

    Args:
        lab:     Str. Name of lab
        year:    Int. Year of interest
        qtr:     Int. In range [1, 4]. Quarter to read
        version: Int. Version of file to read

    Returns:
        Tuple of dataframes (stn_df, wc_df)
    """
    # Connect to database
    fold_path = f"../../output/{lab.lower()}_{year}_q{qtr}_v{version}"
    db_path = os.path.join(fold_path, "kalk_data.db")
    eng = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)

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
