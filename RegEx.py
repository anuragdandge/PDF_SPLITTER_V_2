import re

def check_regex_in_multiline_string(text, pattern):
    """
    Checks if a regex pattern exists anywhere within a multiline string.
    """
    match = re.search(pattern, text, re.MULTILINE)  # Use re.search and re.MULTILINE
    return bool(match)


text = """This is a multiline string.
It contains some random text.
Somewhere in here is the code: CLS/KH 2023/MH/3640985
And some more random text.
"""

pattern = r"[A-Z]{3}/[A-Z]{2}\s?\d{4}/[A-Z]{2}/\d{7}"

if check_regex_in_multiline_string(text, pattern):
    print("Regex pattern found in the string.")
else:
    print("Regex pattern not found.")


# Example with extraction:
match = re.search(pattern,text,re.MULTILINE)
if match:
    print("Match Found:", match.group(0))