import streamlit as st
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


class TradingLog:
    def __init__(self, username):
        self.username = username
        self.file_path = f"{username}_trading_log.csv"

        if os.path.exists(self.file_path):
            self.df = pd.read_csv(self.file_path)
        else:
            self.df = pd.DataFrame(columns=['Timestamp', 'Action', 'Symbol', 'Quantity', 'Price'])

    def log_trade(self, timestamp, action, symbol, quantity, price):
        new_trade = pd.DataFrame({
            'Timestamp': [timestamp],
            'Action': [action],
            'Symbol': [symbol],
            'Quantity': [quantity],
            'Price': [price]
        })
        self.df = pd.concat([self.df, new_trade], ignore_index=True)

    def save_to_csv(self):
        self.df.to_csv(self.file_path, index=False)

    def display_log(self):
        st.dataframe(self.df)

    def calculate_total_money(self):
        total_money = (self.df[self.df['Action'] == 'Sell']['Quantity'] *
                       self.df[self.df['Action'] == 'Sell']['Price']).sum()
        st.text(f'Total Money: ${total_money:.2f}')

    def calculate_cagr(self):
        sell_prices = self.df[self.df['Action'] == 'Sell']['Price']
        buy_prices = self.df[self.df['Action'] == 'Buy']['Price']
        if not sell_prices.empty and not buy_prices.empty:
            initial_investment = buy_prices.sum()
            final_value = sell_prices.sum()
            years_passed = (pd.to_datetime(self.df['Timestamp']).max() -
                            pd.to_datetime(self.df['Timestamp']).min()).days / 365.25
            cagr = ((final_value / initial_investment) ** (1 / years_passed)) - 1
            st.text(f'CAGR: {cagr:.2%}')


def login():
    st.title('Login')

    username_input = st.text_input('Enter your username:')
    password_input = st.text_input('Enter your password:', type='password')

    if st.button('Login') or st.session_state.logged_in:
        if Authentication.authenticate_user(username_input, password_input):
            st.success('Login successful!')
            st.session_state.logged_in = True
            st.session_state.username = username_input
            st.session_state.trading_log = TradingLog(username_input)
        else:
            st.error('Invalid username or password.')

    st.subheader('Register')
    new_username = st.text_input('New username:')
    new_password = st.text_input('New password:', type='password')

    if st.button('Register'):
        Authentication.create_user(new_username, new_password)
        st.success('Registration successful! You can now login with your new credentials.')


def main_app():
    st.title('Trading Log App - Main Page')

    trading_log = st.session_state.trading_log

    # Get user input for trading activity
    timestamp = st.text_input('Timestamp (e.g., 2023-01-01 12:00:00)')
    action = st.selectbox('Action', ['Buy', 'Sell'])
    symbol = st.text_input('Symbol')
    quantity = st.number_input('Quantity', min_value=1)
    price = st.number_input('Price', min_value=0.01)

    # Log the trading activity
    if st.button('Log Trade'):
        trading_log.log_trade(timestamp, action, symbol, quantity, price)

    trading_log.display_log()

    # Save to CSV
    if st.button('Save to CSV'):
        trading_log.save_to_csv()
        st.success('Trading log saved.')

    # Display total money and CAGR
    trading_log.calculate_total_money()
    trading_log.calculate_cagr()

    # Logout button
    if st.button('Logout'):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.trading_log = None
        st.success('Logout successful!')


def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        main_app()
    else:
        login()


if __name__ == "__main__":
    main()
