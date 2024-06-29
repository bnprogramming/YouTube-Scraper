import re


def sanitize_filename(filename):
    """Remove characters that are not allowed in filenames using regex"""
    cleaned_filename = re.sub(r'[^\w\-_. ]', '', filename)
    # Replace spaces with underscores
    cleaned_filename = cleaned_filename.replace(' ', '_')
    return cleaned_filename
