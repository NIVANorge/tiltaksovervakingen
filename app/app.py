import streamlit as st

import pages.check
import pages.home

PAGES = {
    "Home": pages.home,
    "Check data": pages.check,
}


def main():
    """Main function of the app."""
    st.title("Tiltaksovervåkingen QC app")
    st.sidebar.image(r"./images/niva-logo.png", use_column_width=True)
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()


if __name__ == "__main__":
    main()
