def empty_method(value: str):
    pass

def is_number(value: str) -> bool:
    """
    Check if a string can be converted to an integer or float.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False
