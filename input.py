import math

 
def sun_input():
    """Prompt for user input on sun azimuth and elevation."""

    az, elev = input('Sun: azimuth and elevation [deg]: ').split()
    az_elev = [az, elev]

    # convert user input
    for idx, value in enumerate(az_elev):
        az_elev[idx] = math.radians(float(value))

    return az_elev


def camera_input():
    """Prompt for camera's rotation information."""

    o, p, k = input('Image: omega phi kappa [deg]: ').split()
    opk = [o, p, k]

    # convert user input
    for idx, value in enumerate(opk):
        opk[idx] = math.radians(float(value))

    return opk
