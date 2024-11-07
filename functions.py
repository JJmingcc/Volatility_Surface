from enum import Enum
from dataclasses import dataclass
from scipy.optimize import newton, brentq
from datetime import datetime
import scipy.stats as si
import numpy as np
from scipy.stats import norm

def newton_vol_call_div(S, K, T, C, r, q, sigma):
    
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    fx = S * np.exp(-q * T) * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0) - C
    
    vega = (1 / np.sqrt(2 * np.pi)) * S * np.exp(-q * T) * np.sqrt(T) * np.exp((-si.norm.cdf(d1,0.0, 1.0) ** 2) * 0.5)
    
    tolerance = 0.000001
    x0 = sigma
    xnew  = x0
    xold = x0 - 1
        
    while abs(xnew - xold) > tolerance:
    
        xold = xnew
        xnew = (xnew - fx - C) / vega
        
        return abs(xnew)


class OptionType(Enum):
    CALL = 1
    PUT = 2

@dataclass
class BlackScholes:
    type: OptionType
    spot: float
    exercise: float
    years: float
    volatility: float
    risk_free_rate: float
    dividend_yield: float

    @property
    def d1(self) -> float:
        a = np.log(self.spot / self.exercise)
        b = (self.risk_free_rate - self.dividend_yield + ((self.volatility**2) / 2)) * self.years
        c = self.volatility * np.sqrt(self.years)
        return (a + b) / c

    @property
    def d2(self) -> float:
        return self.d1 - self.volatility * np.sqrt(self.years)

    def price(self) -> float:
        N = norm.cdf
        discount = np.exp(-self.risk_free_rate * self.years)
        presentE = self.exercise * discount
        Nd1 = N(self.d1)
        Nd2 = N(self.d2)

        if self.type == OptionType.CALL:
            return self.spot * np.exp(-self.dividend_yield * self.years) * Nd1 - presentE * Nd2

        elif self.type == OptionType.PUT:
            return presentE * (1 - Nd2) - self.spot * np.exp(-self.dividend_yield * self.years) * (1 - Nd1)

        raise Exception("Unknown option type.")

    @property
    def vega(self) -> float:
        return self.spot * norm.pdf(self.d1) * np.sqrt(self.years)

    from scipy.optimize import newton, brentq
    import random

    @staticmethod
    def find_implied_volatility(
        type: OptionType,
        spot: float,
        exercise: float,
        years: float,
        target_price: float,
        risk_free_rate: float,
        dividend_yield: float
    ) -> float:
        model = lambda vol: BlackScholes(
            type=type,
            spot=spot,
            exercise=exercise,
            years=years,
            volatility=vol,
            risk_free_rate=risk_free_rate,
            dividend_yield=dividend_yield
        )
    
        func = lambda vol: model(vol).price() - target_price
        fprime = lambda vol: model(vol).vega
    
        x0 = 0.3
    
        try:
            # Try Newton-Raphson method first
            implied_vol = newton(func=func, fprime=fprime, x0=x0, maxiter=50, tol=1e-5)
    
            # Check if the volatility found is within a reasonable range
            if implied_vol < 0.0001 or implied_vol > 5:
                raise RuntimeError("Implied volatility out of bounds.")
    
            return implied_vol
    
        except RuntimeError as e:
            print(f"Newton-Raphson failed: {e}, switching to Brent's method.")
    
            # Dynamically adjust bounds to find values that bracket a root
            lower_bound = 0.0001
            upper_bound = 1.0
            step = 1.0
    
            for _ in range(10):  # Try expanding the bounds up to 10 times
                try:
                    if func(lower_bound) * func(upper_bound) < 0:
                        # We have found suitable bounds for Brent's method
                        return brentq(func, a=lower_bound, b=upper_bound, maxiter=100)
    
                    # Expand the upper bound if no root is found within current bounds
                    upper_bound += step
                except ValueError:
                    # If func at bounds produces an error, continue expanding
                    upper_bound += step
    
            print(f"Brent's method also failed after expanding bounds.")
            return None  # Return None if no solution found


def calculate_time_to_expiration(expiration_date_str: str) -> float:
    """
    Calculate the time to expiration in years from today.

    Parameters:
    expiration_date_str (str): Expiration date in the format 'YYYY-MM-DD'

    Returns:
    float: Time to expiration in years
    """
    # Parse the expiration date string to a datetime object
    expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d")

    # Get today's date
    current_date = datetime.now()

    # Calculate the number of days to expiration
    days_to_expiration = (expiration_date - current_date).days

    # Convert days to years (use 365 for simplicity)
    T = days_to_expiration / 365.0

    return T

