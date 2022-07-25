import numpy as np
import pandas as pd
import streamlit as st


def app():
    """Main function for the 'check' page."""
    lab = st.sidebar.selectbox("Select lab:", ["Eurofins", "VestfoldLAB"])
    data_file = st.sidebar.file_uploader("Upload data")

    if data_file:
        with st.spinner("Reading data..."):
            st.header("Raw data")
            st.markdown(
                "The raw data from Excel are shown below. Click the arrows "
                "(top-right of the table) to expand to full-screen."
            )
            st.markdown(f"**File name:** `{data_file.name}`")
            df = read_data_template(data_file, sheet_name="results", lab=lab)
            stn_df = pd.read_excel(
                r"./data/active_stations_2020.xlsx", sheet_name="data"
            )
            st.dataframe(df.astype(str))

        # Begin QC checks
        check_numeric(df)
        check_missing_parameters(df)
        check_greater_than_zero(df)
        check_lod_consistent(df)
        check_stations(df, stn_df)
        check_quarter(df)
        check_duplicates(df)
        st.header("Checking water chemistry")
        check_no3_totn(df)
        check_ral_ilal_lal(df)
        check_lal_ph(df)

    return None


# @st.cache
def get_par_unit_mappings():
    """Get dataframe mapping parameters and units as reported by Vestfold Lab and Eurofins
    to those used in Vannmiljø.

    Args:
        None

    Returns:
        Dataframe.
    """
    df = pd.read_excel(
        r"./data/parameter_unit_mapping.xlsx",
        sheet_name="to_vannmiljo",
        keep_default_na=False,
    )

    return df


# @st.cache
def read_data_template(file_path, sheet_name="results", lab="Eurofins"):
    """Read lab data from the agreed template in 'wide' format. An example of
    the template is here:

            ./data/vestfold_lab_data_to_2020-08-31.xls

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
        usecols="C,D,F,G,I:AD",
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
            "nan_Labreferanse": "labreferanse",
            "nan_Resultatkommentar": "resultatkommentar",
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
    n_errors = 0
    for col in cols:
        if col not in df.columns:
            n_errors += 1
            st.markdown(f" * Column **{col}** is missing from the data file provided.")

    if n_errors > 0:
        st.error(
            "ERROR: The data file is missing some required columns. Please use the "
            "template available here:\n\n"
            "https://github.com/NIVANorge/tiltaksovervakingen/blob/master/data/tiltaksovervakingen_blank_data_template.xlsx"
        )
        st.stop()

    df = df[
        ["vannmiljo_code", "station_name", "sample_date", "depth1", "depth2"]
        + cols
        + ["labreferanse", "resultatkommentar"]
    ]

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
    st.header("Checking for non-numeric data")
    non_num_cols = [
        "vannmiljo_code",
        "station_name",
        "sample_date",
        "labreferanse",
        "resultatkommentar",
    ]
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
            st.markdown(
                f" * Column **{col}** contains non-numeric values: `{non_num_vals}`"
            )

    if n_errors > 0:
        st.error(
            "ERROR: The template contains non-numeric data (see above). Please fix these issues and try again."
        )
        st.stop()
    else:
        st.success("OK!")

    return None


def check_missing_parameters(df):
    """Check that relevant columns in 'df' contain at least some data.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    st.header("Checking for expected parameters")
    col_list = [
        "pH_enh",
        "Kond_ms/m",
        "Alk_mmol/l",
        "Tot-P_µg/l",
        "Tot-N_µg/l",
        "NO3_µg/l",
        "TOC_mg/l",
        "RAl_µg/l",
        "ILAl_µg/l",
        "LAl_µg/l",
        "Cl_mg/l",
        "SO4_mg/l",
        "Ca_mg/l",
        "K_mg/l",
        "Mg_mg/l",
        "Na_mg/l",
        "SIO2_µg/l",
        "ANC_µekv/l",
    ]
    n_errors = 0
    for col in col_list:
        if df[col].isnull().all():
            n_errors += 1
            st.markdown(f" * Column **{col}** does not contain any data.")

    if n_errors == 0:
        st.success("OK!")
    else:
        st.warning("WARNING: Some expected parameters have not been reported.")

    return None


def check_greater_than_zero(df):
    """Check that relevant columns in 'df' contain values greater than zero.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    st.header("Checking for negative and zero values")
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
            st.markdown(
                f" * Column **{col}** contains values less than or equal to zero."
            )

    if n_errors == 0:
        st.success("OK!")
    else:
        st.warning("WARNING: Some measured values are less than or equal to zero.")

    return None


def check_lod_consistent(df):
    """Check that the LOD for each parameter in 'df' is consistent.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    st.header("Checking Limit of Detection (LOD) values")
    n_errors = 0
    for col in df.columns:
        lods = df[df[col].astype(str).str.contains("<")][col].unique()
        if len(lods) > 1:
            n_errors += 1
            st.markdown(f" * Column **{col}** contains multiple LOD values: `{lods}`.")

    if n_errors == 0:
        st.success("OK!")
    else:
        st.warning("WARNING: Some columns have multiple/inconsistent LOD values.")

    return None


def check_stations(df, stn_df):
    """Basic check of station data in 'df' against reference data in 'stn_df'.

    Args:
        df:     Dataframe of sumbitted water chemistry data
        stn_df: Dataframe of reference station details

    Returns:
        None. Problems identified are printed to output.
    """
    st.header("Checking stations")
    n_errors = 0
    if not set(df["vannmiljo_code"]).issubset(set(stn_df["vannmiljo_code"])):
        n_errors += 1
        st.markdown(
            "The following location IDs are not in the definitive station list."
        )
        st.code(set(df["vannmiljo_code"]) - set(stn_df["vannmiljo_code"]))

    # Check station ID have consistent names
    msg = ""
    site_ids = df["vannmiljo_code"].unique()
    for site_id in site_ids:
        true_name = stn_df.query("vannmiljo_code == @site_id")["station_name"].values
        names = df.query("vannmiljo_code == @site_id")["station_name"].unique()

        if len(names) > 1:
            msg += f"\n * **{site_id}** ({true_name[0]}) has names: `{names}`"

    if msg != "":
        n_errors += 1
        st.markdown(
            "The following location IDs have inconsistent names within this template:"
        )
        st.markdown(msg)

    # Check station names have consistent IDs
    msg = ""
    site_names = df["station_name"].unique()
    for site_name in site_names:
        true_id = stn_df.query("station_name == @site_name")["vannmiljo_code"].values
        ids = df.query("station_name == @site_name")["vannmiljo_code"].unique()

        if len(ids) > 1:
            msg += f"\n * **{site_name}** has IDs: `{ids}`"
    if msg != "":
        n_errors += 1
        st.markdown(
            "The following location names have multiple IDs within this template:"
        )
        st.markdown(msg)

    if n_errors == 0:
        st.success("OK!")
    else:
        st.warning(
            "WARNING: The template contains unknown or duplicated station names and/or IDs."
        )

    return None


def check_quarter(df):
    """Check all samples come from the same year quarter.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    st.header("Checking sample dates")
    quarters = df["sample_date"].dt.quarter
    if len(quarters.unique()) > 1:
        st.warning(
            f"WARNING: The file contains samples from several year quarters (quarters: `{quarters.unique()}`)."
        )
    else:
        st.success("OK!")

    return None


def check_no3_totn(df):
    """Highlights all rows where nitrate > TOTN. Emphasises rows where
    NO3 > TOTN and TOC > 5 based on advice from Øyvind G (see e-mail received
    04.05.2022 at 23.23 for details).

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    st.subheader("NO3 and TOTN")
    mask_df = df[
        [
            "vannmiljo_code",
            "sample_date",
            "depth1",
            "depth2",
            "NO3_µg/l",
            "Tot-N_µg/l",
            "TOC_mg/l",
            "labreferanse",
        ]
    ].copy()

    for col in ["NO3_µg/l", "Tot-N_µg/l", "TOC_mg/l"]:
        mask_df[col].fillna(0, inplace=True)
        mask_df[col] = pd.to_numeric(
            mask_df[col].astype(str).str.strip("<").str.replace(",", ".")
        )
    mask = mask_df["NO3_µg/l"] > mask_df["Tot-N_µg/l"]
    mask_df = mask_df[mask]
    mask_df_toc = mask_df[mask_df["TOC_mg/l"] > 5]

    if len(mask_df) > 0:
        st.markdown("The following samples have nitrate greater than total nitrogen:")
        st.dataframe(mask_df)

    if len(mask_df_toc) > 0:
        st.markdown(
            "Of these, the following samples have nitrate greater than total nitrogen **and** TOC > 5 mg/l.\n"
            "This is unlikely to be within instrument error"
        )
        st.dataframe(mask_df_toc)

    if len(mask_df) > 0:
        st.warning(f"WARNING: Possible issues with NO3 and TOTN.")
    else:
        st.success("OK!")

    return None


def check_ral_ilal_lal(df):
    """Check RAl - ILAl = LAl.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    st.subheader("Al fractions")
    mask_df = df[
        [
            "vannmiljo_code",
            "sample_date",
            "depth1",
            "depth2",
            "RAl_µg/l",
            "ILAl_µg/l",
            "LAl_µg/l",
            "labreferanse",
        ]
    ].copy()
    mask_df.dropna(subset="LAl_µg/l", inplace=True)

    for col in ["RAl_µg/l", "ILAl_µg/l", "LAl_µg/l"]:
        mask_df[col].fillna(0, inplace=True)
        mask_df[col] = pd.to_numeric(
            mask_df[col].astype(str).str.strip("<").str.replace(",", ".")
        )
    mask_df["LAl_Expected_µg/l"] = (mask_df["RAl_µg/l"] - mask_df["ILAl_µg/l"]).round(1)
    mask_df["LAl_µg/l"] = mask_df["LAl_µg/l"].round(1)
    mask = mask_df["LAl_Expected_µg/l"] != mask_df["LAl_µg/l"]
    mask_df = mask_df[mask]

    if len(mask_df) > 0:
        st.markdown("The following samples have LAl not equal to (RAl - ILAl):")
        st.dataframe(mask_df)
        st.warning(f"WARNING: Possible issues with the calculation of LAl.")
    else:
        st.success("OK!")

    return None


def check_lal_ph(df):
    """Highlight rows where pH > 6.4 and LAl > 20 ug/l. See e-mail from
    Øyvind G received 04.05.2022 at 23.23 for background.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    st.subheader("LAl and pH")
    mask_df = df[
        [
            "vannmiljo_code",
            "sample_date",
            "depth1",
            "depth2",
            "pH_enh",
            "LAl_µg/l",
            "labreferanse",
        ]
    ].copy()
    mask_df = mask_df[(mask_df["pH_enh"] > 6.4) & (mask_df["LAl_µg/l"] > 20)]
    if len(mask_df) > 0:
        st.markdown(
            "The following samples have LAl > 20 µg/l and pH > 6.4, which is considered unlikely:"
        )
        st.dataframe(mask_df)
        st.warning(f"WARNING: Possible issues with LAl and/or pH.")
    else:
        st.success("OK!")

    return None


def check_duplicates(df):
    """Check for multiple samples at the same location, time and depth.

    Args:
        df: Dataframe of sumbitted water chemistry data

    Returns:
        None. Problems identified are printed to output.
    """
    st.header("Checking duplicates")
    key_cols = [
        "vannmiljo_code",
        "sample_date",
        "depth1",
        "depth2",
    ]
    dup_df = df[
        df.duplicated(
            key_cols,
            keep=False,
        )
    ].sort_values(key_cols)

    dup_df = dup_df[key_cols + ["labreferanse", "resultatkommentar"]]
    n_dups = len(dup_df)
    n_flood = dup_df["resultatkommentar"].str.contains("Flomprøve").sum()
    if n_dups > 0:
        st.markdown(
            f"There are **{n_dups}** duplicated samples.\n"
            f"Of these, **{n_flood}** are marked as 'Flomprøve' in the 'resultatkommentar' column."
        )
        st.dataframe(dup_df)
        st.warning(f"WARNING: Possible duplicate samples identified.")
    else:
        st.success("OK!")
