import streamlit as st
import sqlite3
import hashlib
import subprocess


def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn

def create_table(conn):
    """ Create table for user authentication """
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL
                    )''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def hash_password(password):
    """ Hash a password for storing """
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(conn, username, password, role):
    """ Add a new user to the users table """
    hashed_pwd = hash_password(password)
    sql = ''' INSERT INTO users(username, password, role)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (username, hashed_pwd, role))
    conn.commit()
    return cur.lastrowid

def check_user(conn, username, password):
    """ Check if a user exists and return the role """
    hashed_pwd = hash_password(password)
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, hashed_pwd))
    result = cur.fetchone()
    if result:
        return result[0]
    return None

def execute_script(script_name):
    """ Execute a separate Python script """
    subprocess.run(["streamlit", "run", script_name], check=True)

def login_signup_ui(conn, role):
    """ UI for login and signup """
    tab_login, tab_signup = st.tabs(["Login", "Signup"])

    with tab_login:
        username = st.text_input(f"Username")
        password = st.text_input(f"Password", type='password')
        if st.button(f"Login as {role}"):
            if check_user(conn, username, password) == role:
                st.success(f"Logged in as {role}")
                script_to_run = r'C:\Users\User\Desktop\final project\Codes\home.py' if role == 'user' else r'C:\Users\User\Desktop\final project\Codes\main.py'
                execute_script(script_to_run)
            else:
                st.error("Incorrect Username/Password")
        
    with tab_signup:
        new_username = st.text_input(f"New {role} Username")
        new_password = st.text_input("New Password", type='password')
        if st.button(f"Signup as {role}"):
            add_user(conn, new_username, new_password, role)
            st.success(f"You have successfully created a {role} account")


def main():
    st.markdown("""
        <style>
            .main {
                font-family: 'Helvetica Neue', sans-serif;
                text-align: center;
                background-color: #FFFFF;
                color: #444444;
            }
            .stButton>button {
                width: 150px;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 10px;
                margin: 10px;
            }
            .reportview-container .markdown-text-container {
                font-family: monospace;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("🔐 User and Admin Authentication System")

    database = r"authenticator.db"
    conn = create_connection(database)
    create_table(conn)

    role = st.selectbox("Select Role", ["user", "admin"])
    login_signup_ui(conn, role)
    
    

if __name__ == '__main__':
    main()