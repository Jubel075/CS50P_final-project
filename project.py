import matplotlib.pyplot as plt
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
    
# get user inputs functions
def get_component(role):
    """Prompt for a CoolProp fluid name and validate it is recognized"""
    while True:
        name = input(f"Enter {role} (e.g. Benzene): ").strip
        try:
            PropsSI("Tcrit", name)
            return name
        except (ValueError, RuntimeError):
            print(f"Unknown fluid '{name}'. Try a CoolProp name like Benzene or Toluene.")
        
        
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
            


if __name__=="__main__":
    main()