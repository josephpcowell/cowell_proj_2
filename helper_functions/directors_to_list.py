"""
Functions to help clean up information regarding directors.
"""


def directors_list(directors):
    """
    Separates a string of directors into a list of the separate directors.

    Args:
        directors: A string of directors separated by commas

    Returns:
        A list of directors.
    """
    if "," in directors:
        return [name.strip() for name in directors.split(",")]
    else:
        return [directors]


def remove_paren(directors):
    """
    Takes off aliases that are in parentheses next to a director's name

    Args:
        directors: A list of directors

    Returns:
        The same list of directors, but without aliases in parenthesis.
    """
    dir_list = []
    for director in directors:
        if "(" in director:
            dir_clean = director.split("(")[0].strip()
            dir_list.append(dir_clean)
        else:
            dir_list.append(director)
    return dir_list
