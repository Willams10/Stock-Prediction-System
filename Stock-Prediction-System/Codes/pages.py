import streamlit as st

def app():
    # Sidebar navigation
    page = st.sidebar.selectbox("Select Page", ["Page 1", "Page 2"])

    # Conditionally render content based on the selected page
    if page == "Page 1":
        st.header("Page 1")
        st.write("Welcome to Page 1.")
        # Add content for Page 1 here
    elif page == "Page 2":
        st.header("Page 2")
        st.write("Welcome to Page 2.")
        # Add content for Page 2 here
    
    
    