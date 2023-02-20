import re
from flask import render_template


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def validate_password(password):
    """Use regex syntax to validate password"""
    # must include a number
    if not re.search(r'[0-9]', password):
        return False
    # must include a lowercase letter
    elif not re.search(r'[a-z]', password):
        return False
    # must include an uppercase letter
    elif not re.search(r'[A-Z]', password):
        return False
    # must include a symbol
    elif not re.search(r'[!@#$%^&*()_+{}|[\]:"<>,.?/~`-]', password):
        return False
    # must be longer than 8 characters
    elif len(password) < 8:
        return False
    else:
        return True
