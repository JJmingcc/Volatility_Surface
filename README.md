# Volatility Surface

This project visualizes a 3D implied volatility surface for options on any stock ticker symbol. It allows users to explore how implied volatility varies with strike price, moneyness, and time to expiration. This tool is ideal for analyzing option pricing and understanding volatility behavior.

## Features

- **Flexible Ticker Symbol**: Enter any stock ticker to analyze its implied volatility surface.
- **Configurable Inputs**:
  - **Risk-Free Rate**: Input a custom risk-free rate to reflect current market conditions.
  - **Dividend Yield**: Automatically fetched from market data or adjustable for scenario testing.
  - **Strike Price Filter**: Set minimum and maximum strike price filters as a percentage of the spot price.
  - **Y-Axis Selection**: Choose between strike price or moneyness for the Y-axis on the volatility surface.
- **3D Volatility Surface Plot**:
  - X-axis: Time to expiration
  - Y-axis: Strike price or moneyness
  - Z-axis (color-coded): Implied volatility, providing a heatmap of volatility levels.

## Visualization

The implied volatility surface is represented as a 3D plot, with higher volatility areas highlighted in warmer colors. This plot allows users to visualize volatility skews and smiles, which are essential for option pricing and risk management.


## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/volatility-surface.git
   cd volatility-surface

2. Install Required Packages: Make sure you have Python 3 installed. Then, install the required Python packages:
   ```bash
   pip install -r requirements.txt

3. Run the Application: If you're using a Jupyter Notebook, launch the notebook:
   jupyter notebook

4. Data Source: The model retrieves option data and market data (spot price, dividend yield, etc.) from financial APIs (e.g., Yahoo Finance). Make sure you have API    access.

## How it works


1. Data Collection: The application fetches option chain data for the selected ticker, including spot price, strike prices, time to expiration, and current option      prices.

2. Implied Volatility Calculation: Using the Black-Scholes model, the tool calculates implied volatility by iteratively solving for volatility based on the option      market price.

3. 3D Plot Generation: The calculated implied volatilities are plotted as a 3D surface with strike price (or moneyness), time to expiry, and implied volatility.

## Use Cases

 1. Option Pricing and Hedging: Analyze volatility to understand option price behavior under various market conditions.
    
 2. Market Sentiment Analysis: Use volatility skews to gauge market sentiment and the perceived risk of price movements.
    
 3. Scenario Testing: Adjust dividend yield and risk-free rate inputs to test how changes impact the volatility surface.

## Future Enhancements

  1. Integrate additional option pricing models (e.g., binomial tree) for non-European options.
     
  2. Allow users to save and export the generated volatility surface.
     
  3. Implement real-time data streaming for live updates.

## License

  This project is open-source and available under the MIT License.

  Created by GeorgeDros
