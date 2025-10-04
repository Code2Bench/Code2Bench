import re
import json

modules = {"modules": []}
# The input line
with open("sys_modules.html", "r") as file:
    line = file.read()

    # The regex pattern
    pattern = r"library/(.*)\.html\#module"

    # Find all matches for the pattern in the line
    matches = re.findall(pattern, line)

    # If matches are found, print them
    if matches:
        for match in matches:
            modules["modules"].append(match)
    else:
        print("No match found")

with open("sys_modules.json", "w") as file:
    file.write(json.dumps(modules, indent=4))
