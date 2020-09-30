import pandas as pd
import numpy as np
import warnings


def get_par_unit_mappings():
    """Get dataframe mapping parameters and units as reported by Vestfold Lab and Eurofins
        to those used in Vannmiljø.

    Args:
        None

    Returns:
        Dataframe.
    """
    df = pd.read_excel(
        r"../data/parameter_unit_mapping.xlsx",
        sheet_name="vestfoldlab_to_vannmiljo",
        keep_default_na=False,
    )

    return df


def read_data_template(file_path, sheet_name="Ark1", lab="VestfoldLAB AS"):
    """Read lab data from the agreed template. An example of the template is here:

            ../data/vestfold_lab_data_to_2020-08-31.xls

        Also converts units and parameter names to match those in Vannmiljø.

    Args:
        file_path:  Raw str. Path to Excel template
        sheet_name: Str. Name of sheet to read
        lab:        Str. Name of lab

    Returns:
        Dataframe.
    """
    # Read data
    par_df = get_par_unit_mappings()

    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        skiprows=1,
        usecols="C,G,I:AB",
        header=None,
    )

    # Parse header
    header = df[:2]
    df = df[2:]
    first = header.loc[1].tolist()[:2]
    pars = header.loc[0].tolist()[2:]
    units = header.loc[1].tolist()[2:]
    pars_units = [f"{par}_{unit}" for par, unit in zip(pars, units)]
    df.columns = first + pars_units

    df.rename(
        {"Lokalitets-ID": "vannmiljo_code", "Prøvedato": "sample_date"},
        inplace=True,
        axis="columns",
    )

    # Parse dates
    df["sample_date"] = pd.to_datetime(df["sample_date"], format="%d.%m.%Y")

    # Get pars of interest
    cols = [
        f"{par}_{unit}"
        for par, unit in zip(par_df["vestfold_lab_name"], par_df["vestfold_lab_unit"])
    ]
    df = df[["vannmiljo_code", "sample_date"] + cols]

    # Melt to long format
    df = pd.melt(df, id_vars=["vannmiljo_code", "sample_date"], var_name="par_unit")
    df.dropna(subset=["value"], inplace=True)
    df["value"] = pd.to_numeric(df["value"])

    df["lab"] = lab
    df["depth1"] = np.nan
    df["depth2"] = np.nan
    df["flag"] = np.nan

    # Convert to VM par names and units
    par_df["par_unit"] = par_df["vestfold_lab_name"] + "_" + par_df["vestfold_lab_unit"]
    par_df["vm_par_unit"] = par_df["vannmiljo_id"] + "_" + par_df["vannmiljo_unit"]

    df = pd.merge(
        df,
        par_df[["par_unit", "vm_par_unit", "vl_to_vm_conv_fac"]],
        how="left",
        on="par_unit",
    )

    df["value"] = df["value"] * df["vl_to_vm_conv_fac"]

    # Tidy up
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
            usecols="A:I,Q:U,W",
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
