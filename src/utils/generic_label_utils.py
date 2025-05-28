def empty_method(value: str):
    pass

def is_not_a_number(value: str) -> bool:
    """
    Check if a string can be converted to an integer or float.
    """
    try:
        float(value)
        return 0
    except ValueError:
        return 1
