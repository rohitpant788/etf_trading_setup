import os
import pandas as pd
import streamlit as st

class TradingLog:
    def __init__(self, username):
        self.username = username
        self.folder_path = "trading_journal"
        self.file_path = os.path.join(self.folder_path, f"{username}_trading_log.csv")

        # Create the folder if it doesn't exist
        os.makedirs(self.folder_path, exist_ok=True)

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
        # Display the trading log
        st.dataframe(self.df)

        # Add a delete button for each trade log entry
        for index, row in self.df.iterrows():
            if st.button(f"Delete Trade {index}", key=f"delete_button_{index}"):
                self.delete_trade(index)

    def delete_trade(self, index):
        # Your delete logic here
        st.write(f"Deleted trade at index {index}")

    def check_delete_button_click(self):
        for index, row in self.df.iterrows():
            if st.button(f"Delete Trade {index}"):
                return index
        return None

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

    def delete_trade(self, index):
        self.df = self.df.drop(index)

