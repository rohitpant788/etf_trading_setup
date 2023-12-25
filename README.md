# ETF Trading Strategy README

## Overview

This repository contains the code and documentation for an ETF trading strategy based on a 15-minute candlestick timeframe and Supertrend indicators. The strategy aims to optimize capital allocation, enhance profit potential, and actively manage the portfolio.

## Strategy Components

### 1. Timeframe

- 15-minute candlestick timeframe.

### 2. Capital Allocation

- Total capital: $100,000.
- Divide capital into 5 equal parts: $20,000 each.

### 3. Supertrend Indicators

- Two Supertrend indicators with parameters:
  - Indicator 1: ATR, Factor (1,22)
  - Indicator 2: ATR, Factor (4,22)

### 4. Buy Signal

- Buy signal is generated when Supertrend (1,22) signals a "buy."

### 5. Sell Signal

- Sell signal is generated when Supertrend (4,22) signals a "sell."
- Execute sell only if the profit is more than 6%.

### 6. ETF Selection

- On every buy signal, purchase an ETF of Nifty 50.
- Distribute the investment equally among different Nifty 50 ETFs.

### 7. Profit Booking

- Upon a sell signal, sell only one ETF that is in the most profit.

## Example Trade Flow

1. **Buy Signal:**
   - Supertrend (1,22) signals a "buy."
   - Allocate $20,000 to a new Nifty 50 ETF.

2. **Sell Signal:**
   - Supertrend (4,22) signals a "sell."
   - Check if the profit is more than 6%.
   - If yes, sell the ETF that is in the most profit.

3. **Repeat:**
   - Repeat the process for subsequent buy and sell signals.

## Notes

- Backtest the strategy with historical data to evaluate performance.
- Stay updated with market conditions and be aware of potential risks.
- Customize parameters and ETF selection based on personal preferences.

## Files

- `strategy_code.py`: Contains the Python code for implementing the trading strategy.
- `data/`: Directory to store historical price data for backtesting.
- `results/`: Directory to store backtesting results and performance metrics.

## Getting Started

1. Clone this repository to your local machine.
2. Install the required dependencies (e.g., Pandas, NumPy).
3. Run the `strategy_code.py` script to execute the trading strategy.

## License

This project is licensed under the [MIT License](LICENSE).
