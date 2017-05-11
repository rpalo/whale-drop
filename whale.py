"""This is an important study into the motion of a Blue
Whale, falling to the Earth from orbit."""

import math

# Assumptions:
# 1. Assume whale is an average blue whale
# 2. Assume whale falls towards earth head on since
#    fluids data is available for this case
# 3. This is a rough calculation.  All constants are approximate.
# 4. Positive Y is away from planet.

# Constants
GRAV_CONSTANT = 6.67384e-11 # [m^3/kg s^2]
EARTH_MASS = 3.5786e7 # [kg]
EARTH_RADIUS = 6.367e6 # [m]
WHALE_MASS = 100000 # [kg]
WHALE_DRAG_COEFF = 0.05 # [unitless]
WHALE_CROSS_AREA = 10 # [m^2] head on, mouth closed
TROPO_ALTITUDE = 11019.1 # [m] Upper limit of troposphere
STRATOS_SPLIT_ALTITUDE = 25098.8 # [m] Upper limit of lower stratosphere

def gravity(altitude):
    """Calculates the force of gravity at a given altitude"""
    distance = altitude + EARTH_RADIUS
    gravity_force = (GRAV_CONSTANT * WHALE_MASS * EARTH_MASS /
                    (distance**2))
    return gravity_force # [N]

# TODO: comment this function and remove constants
def density(altitude):
    """Corrects air density measurement for altitude"""
    altitude_in_feet = altitude * 3.28084 # correct in standard [ft]
    if altitude > STRATOS_SPLIT_ALTITUDE:
        temperature = -205.05 + .00164 * altitude_in_feet # [F]
        pressure = 51.97 * ((temperature + 459.7)/389.98)**(-11.388) # [psf]
    elif altitude > TROPO_ALTITUDE:
        temperature = -70 # [F]
        pressure = 473.1 * math.exp(1.73 - .000048 * altitude_in_feet) # [psf]
    else:
        temperature = 59 - .00356 * altitude_in_feet # [F]
        pressure = 2116 * ((temperature + 459.67)/518.6)**5.256 # [psf]
    
    density = (pressure /
                1718 * (temperature + 459.67)) # [slug/ft^3]
    density *= 515.378818 # convert back to [kg/m^3]
    return density # [kg/m^3]

def drag(altitude, velocity):
    """Calculates aerodynamic drag"""
    drag_force = .5 * WHALE_DRAG_COEFF * density(altitude)
    drag_force *= WHALE_CROSS_AREA
    drag_force *= velocity**2
    if velocity > 0: # Drag always opposes motion
        drag_force *= -1
    return drag_force # [N]

def net_acceleration(altitude, velocity):
    """Sums all forces to calculate a net acceleration for next step."""
    gravity_force = gravity(altitude) # [N]
    drag_force = drag(altitude, velocity) # [N]
    net_force = drag_force - gravity_force # [N]
    acceleration = net_force / WHALE_MASS # [m/s^2]
    return acceleration



    