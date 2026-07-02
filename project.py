import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI


def main():
    # get user inputs
    light = get_component("light componnet", "Benzene")
    heavy = get_component("heavy componnet", "Toluene")
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

    # count theoretical stages
    try:
        stages = count_stages(alpha, xD, xB, x_int, y_int, R)
    except ValueError as e:
        print(f"Error: {e}")
        return
    print(f"Theoretical stages: {stages}")

    # plot the McCabe-Thiele diagram
    plot_diagram(alpha, xD, xB, x_int, y_int, R)


# get user inputs functions
def get_component(role, example="a valid fluid name"):
    """Prompt for a CoolProp fluid name and validate it is recognized"""
    while True:
        name = input(f"Enter {role} (e.g. {example}): ").strip()
        try:
            PropsSI("Tcrit", name)
            return name
        except ValueError, RuntimeError:
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


def inverse_equilibrium(y, alpha):
    """Liquid mole fraction x in equilibrium with vapor fraction y (inverse of equilibrium_y)."""
    return y / (alpha - (alpha - 1) * y)


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


def count_stages(alpha, xD, xB, x_int, y_int, R):
    """Step off the McCabe-Thiele staircase from (xD, xD) down to xB; return stage count.

    Each iteration: step horizontally to the equilibrium curve (one theoretical stage),
    then vertically down to the rectifying line (above the feed) or stripping line (below).
    """
    MAX_STAGES = 100
    stages = 0
    x, y = xD, xD
    # added precision error handling
    while x > (xB + 1e-9) and stages < MAX_STAGES:
        # horizontal step to the equilibrium curve -> one stage
        x = inverse_equilibrium(y, alpha)
        stages += 1
        # vertical step down to the correct operating line
        if x > x_int:
            y = rectifying_line(x, R, xD)
        else:
            y = stripping_line(x, x_int, y_int, xB)

    # loop only exits at MAX_STAGES without converging if the staircase never reaches xB
    if stages >= MAX_STAGES:
        raise ValueError(
            f"Column did not converge within {MAX_STAGES} stages; check R, q, xD, xB and alpha."
        )
    return stages


def plot_diagram(alpha, xD, xB, x_int, y_int, R):
    """Draw curves, lines and staircase; save to pdf."""
    # equilibrium curve over the full composition range
    x_eq = np.linspace(0, 1, 200)
    y_eq = equilibrium_y(x_eq, alpha)

    # y = x reference (diagonal) line
    x_diag = np.linspace(0, 1, 2)
    y_diag = x_diag

    # rectifying line: from the feed intersection up to (xD, xD)
    x_rect = np.linspace(x_int, xD, 100)
    y_rect = rectifying_line(x_rect, R, xD)

    # stripping line: from (xB, xB) up to the feed intersection
    x_strip = np.linspace(xB, x_int, 100)
    y_strip = stripping_line(x_strip, x_int, y_int, xB)

    fig, ax = plt.subplots()

    ax.plot(x_eq, y_eq, label="Equilibrium curve")
    ax.plot(x_diag, y_diag, "k--", label="y = x")
    ax.plot(x_rect, y_rect, label="Rectifying line")
    ax.plot(x_strip, y_strip, label="Stripping line")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("x (liquid mole fraction)")
    ax.set_ylabel("y (vapor mole fraction)")
    ax.set_title("McCabe-Thiele Diagram")
    ax.legend()

    fig.savefig("mccabe_thiele.pdf")


if __name__ == "__main__":
    main()
