import re


def sanitize_path(string):
    pattern = r'(\A/)|(\.\.)'
    replaced_string = re.sub(pattern, '', string)
    if re.search(pattern, replaced_string):
        return sanitize_path(replaced_string)
    return replaced_string
