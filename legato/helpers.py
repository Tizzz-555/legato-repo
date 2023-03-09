import re
from flask import render_template
from math import log
from datetime import datetime

# Create a datetime object representing the Unix epoch (Jan,1,1970) and store it in the epoch global variable.
epoch = datetime(1970, 1, 1)


# Homage to CS50 finance
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
    # Must include a number
    if not re.search(r'[0-9]', password):
        return False
    # Must include a lowercase letter
    elif not re.search(r'[a-z]', password):
        return False
    # Must include an uppercase letter
    elif not re.search(r'[A-Z]', password):
        return False
    # Must include a symbol
    elif not re.search(r'[!@#$%^&*()_+{}|[\]:"<>,.?/~`-]', password):
        return False
    # Must be longer than 8 characters
    elif len(password) < 8:
        return False
    else:
        return True


def from_now(time_diff):
    # Calculate the minutes dividing total seconds passed from post creation by 60
    minutes = int(time_diff.total_seconds() // 60)

    if minutes < 1:
        return "less than a minute ago"
    # Edge case "minute"
    if minutes == 1:
        return "1 minute ago"
    if minutes > 1 and minutes < 60:
        return f"{minutes} minutes ago"

    # Total minutes divided by 60 == hours
    hours = int(minutes // 60)
    # Edge case "hour"
    if hours == 1:
        return "1 hour ago"
    if hours > 1 and hours < 24:
        return f"{hours} hours ago"

    # Total hours divided by 24 == days
    days = int(hours // 24)
    # Edge case "day"
    if days == 1:
        return "1 day ago"
    if days > 1 and days < 31:
        return f"{days} days ago"

    # Total hours divided by 31 == months
    months = int(days // 31)
    # Edge case "month"
    if months == 1:
        return "one month ago"
    if months > 1 and months < 12:
        return f"{months} months ago"

    # Total months divided by 12 == years
    years = int(months // 12)
    # Edge case "year"
    if years == 1:
        return "1 year ago"
    if years > 1:
        return f"{years} years ago"


''' This is Reddit's hot algorithm to sort post by their rating combined to the date they were created'''


def epoch_seconds(date):
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


def score(ups, downs):
    return ups - downs


def hot(ups, downs, date):
    # Call to score function
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    # Call to epoch_seconds function
    seconds = epoch_seconds(date) - 1134028003
    return round(sign * order + seconds / 45000, 7)
