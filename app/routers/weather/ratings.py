def normalize(v: float, l: float, h: float):
    return (v - l) / (h - l)

def get_temp_rating(t: float, ideal=75) -> float:
    """get a rating from 0-1, where 1 is ideal conditions. Rating deteriorates the further
    you get from ideal

    Args:
        t (float): the temp to test
        ideal (int, optional): the ideal temperature. Defaults to 75.

    Returns:
        float: _description_
    """
    if t < 45 or t >= 100:
        return 0.0
    if t < ideal:
        low = 45
        high = ideal
    else:
        low = ideal
        high = 100
    norm = normalize(t, low, high)
    return norm if t < ideal else 1 - norm

def get_wind_rating(w: float, temp: float) -> float:
    """gets the wind rating

    Args:
        s (float): wind value to check (in MPH)
        temp (float): the avg temp (in F)
        ideal (float): the ideal wind (in MPH)

    Returns:
        float: the rating on a 0-1 scale
    """
    if w < 5 and temp >= 85:
        # no wind is not quite ideal, still want a breeze
        return .8
    elif w > 20:
        return 0.0
        
    if temp >= 85: 
        ideal = 10
    else:
        ideal = 5
    high = 20
    low = ideal
    return min(abs(1 - normalize(w, low, high)), 1)

def get_precip_rating(p: float) -> float:
    """gets the precipitation rating, dryer is better

    Args:
        p (float): precipitation value to check (in MM)

    Returns:
        float: the rating on a 0-1 scale
    """
    if p == 0:
        return 1.0
    elif p >= 4:
        return 0
    return 1 - normalize(p, 0, 4)

def get_dew_rating(d: float, temp: float) -> float:
    """gets the dew rating

    Args:
        d (float): dew point value to check (in F)
        temp (float): the avg temp (in F)

    Returns:
        float: the rating on a 0-1 scale
    """
    if temp >= 85 and d >= 60:
        # this is getting muggy, no thanks
        return 0.0
    
    if d <= 40:
        return 1.0

    ideal = 40
    high = 70
    if d <= ideal:
        low = 0
    else:
        low = 40

    return 1 - normalize(d, low, high)