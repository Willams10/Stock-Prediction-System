import streamlit as st
from streamlit_option_menu import option_menu
import cc, prediction_page, blog, main

st.set_page_config(page_title="MENU")

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        if 'logged_out' in st.session_state and st.session_state['logged_out']:
            st.write("You have been logged out.")
            st.write("Please navigate to login.py to log in again.")
            return  

        # Sidebar content
        with st.sidebar:
            user_role = self.get_user_role()
            menu_options = ['Exchange', 'Prediction', 'Blog']
            menu_icons = ['cash-coin', 'robot', 'collection']

            if user_role == 'admin':
                menu_options.append('Admin')
                menu_icons.append('chat-fill')

            app = option_menu(
                menu_title='MENU',
                options=menu_options,
                icons=menu_icons,
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

            if st.button('Logout'):
                st.session_state['logged_out'] = True
                st.experimental_rerun()

        if app == "Exchange":
            cc.app()
        elif app == "Prediction":
            prediction_page.app()
        elif app == "Blog":
            blog.main()
        elif app == "Admin" and user_role == 'admin':
            main.main()

    def get_user_role(self):
        return st.session_state.get('user_role', 'user')

if __name__ == '__main__':
    app = MultiApp()
    app.run()
