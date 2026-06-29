# import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI


def main():
    # get user inputs
    light = get_component("light componnet")
    heavy = get_component("heavy componnet")
    T = get_temperature()
    xD = get_fraction("distillate purity xD")
    xB = get_fraction("buttoms purity xB")
    zF = get_fraction("feed composition purity zF")
    R = get_reflux()
    q = get_q()

    # compute alpha
    alpha = relative_volatility(light, heavy, T)
    print(f"Relative volatility: {alpha}")

    # find feed intersection
    x_int, y_int = feed_intersec(zF, q, R, xD)
    print(f"Feed intersection: {x_int}, {y_int}")

    # find striping line
    for x in np.arange(0.0, 1.0, 0.1):
        print(f"Strippping line: {x}, {stripping_line(x, x_int, y_int, xB)}")


# get user inputs functions
def get_component(role):
    """Prompt for a CoolProp fluid name and validate it is recognized"""
    while True:
        name = input(f"Enter {role} (e.g. Benzene): ").strip()
        try:
            PropsSI("Tcrit", name)
            return name
        except (ValueError, RuntimeError):
            print(
                f"Unknown fluid '{name}'. Try a CoolProp name like Benzene or Toluene."
            )


def get_temperature():
    """Prompt for an absolute temperature in Kelvin (> 0)."""
    while True:
        try:
            T = float(input("Enter a column temperature in K: "))
        except ValueError:
            print("Please enter a number.")
            continue
        if T > 0:
            return T
        print("Temperature must be > 0 K.")


def get_fraction(name):
    """Prompt for a mole fraction strictly between 0 and 1."""
    while True:
        try:
            x = float(input(f"Enter {name}  (0-1): "))
        except ValueError:
            print("Please enter a number.")
            continue
        if 0 < x < 1:
            return x
        print("Mole fraction must be 0 < x < 1.")


def get_reflux():
    """Prompt for the reflux ratio R (>= 0)."""
    while True:
        try:
            R = float(input("Enter a reflux ratio R: "))
        except ValueError:
            print("Please enter a number.")
            continue
        if R >= 0:
            return R
        print("R must be >= 0")


def get_q():
    """Prompt for the feed quality q (q=1 saturated liquid, q=0 saturated vapor)."""
    while True:
        try:
            return float(input("Enter a feed quality q: "))
        except ValueError:
            print("Please enter a number. ")


""" 
Logic functions:
    - Calculate relative volatility (alpha)
    - Calculate equilibrium (y)
    - Calculate rectifying line
    - Find feed intersection
    - Count the total stages
    - Plot diagram
"""


def relative_volatility(light, heavy, T):
    """Return alpha = Psat(light) / Psat(heavy) at given T (K) using CoolProp."""
    psat_light = PropsSI("P", "T", T, "Q", 0, light)
    psat_heavy = PropsSI("P", "T", T, "Q", 0, heavy)
    return psat_light / psat_heavy


def equilibrium_y(x, alpha):
    """Vapor mole fraction in equilibrium with liquid fraction x, given constant volatility."""
    return (alpha * x) / (1 + (alpha - 1) * x)


# operating lines:
def rectifying_line(x, R, xD):
    """y on the rectifying line at liquid fraction x."""
    return (R / (R + 1)) * x + (xD / (R + 1))


def stripping_line(x, x_int, y_int, xB):
    """y on the stripping line at liquid fraction x."""
    slope = (y_int - xB) / (x_int - xB)
    return slope * (x - xB) + xB


def feed_intersec(zF, q, R, xD):
    """Return the (x, y) point where rectifying line and q-line meet
    q-line:         y = q/(q-1) * x - zF/(q-1)  (q != 1)
    rectifying:     y = R/(R+1) * x + xD/(R+1)
    """
    rect_slope = R / (R + 1)
    rect_int = xD / (R + 1)

    # vertical q line at x = zF
    if q == 1:
        x = zF
    else:
        q_slope = q / (q - 1)
        q_int = -zF / (q - 1)
        x = (rect_int - q_int) / (q_slope - rect_slope)
    y = rect_slope * x + rect_int

    return x, y


def count_stages(alpha, xD, zF, q, R):
    """Stepping loop for the staircase, return n amount of stages."""
    ...


def plot_diagram():
    """Draw curves, lines and staircase; save to pdf."""
    ...


if __name__ == "__main__":
    main()
