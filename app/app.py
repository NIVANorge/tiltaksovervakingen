import streamlit as st

import subpages.check
import subpages.home

PAGES = {
    "Home": subpages.home,
    "Check data": subpages.check,
}


def main():
    """Main function of the app."""
    st.title("Tiltaksovervåkingen QC app")
    st.sidebar.image(r"./app/images/niva-logo.png", use_column_width=True)
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()


if __name__ == "__main__":
    main()
