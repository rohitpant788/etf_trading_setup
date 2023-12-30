# app.py
import pandas as pd
import streamlit as st
from authentication import Authentication
from trading_log import TradingLog


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
    timestamp = st.date_input('Date', value=pd.to_datetime('today').date())
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
