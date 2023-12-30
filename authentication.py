# authentication.py
import pandas as pd
import os
from hashlib import sha256

USERS_FILE = 'users.csv'

class Authentication:
    @staticmethod
    def create_user(username, password):
        hashed_password = sha256(password.encode()).hexdigest()
        users_df = pd.DataFrame({'Username': [username], 'Password': [hashed_password]})
        if not os.path.exists(USERS_FILE):
            users_df.to_csv(USERS_FILE, index=False)
        else:
            existing_users = pd.read_csv(USERS_FILE)
            if username not in existing_users['Username'].values:
                users_df = pd.concat([existing_users, users_df], ignore_index=True)
                users_df.to_csv(USERS_FILE, index=False)

    @staticmethod
    def authenticate_user(username, password):
        hashed_password = sha256(password.encode()).hexdigest()
        users_df = pd.read_csv(USERS_FILE)
        user_row = users_df[users_df['Username'] == username]
        if not user_row.empty and user_row['Password'].iloc[0] == hashed_password:
            return True
        return False
