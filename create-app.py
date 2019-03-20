import json
import re

# Load the data.
with open("new_data.json") as f:
    data = f.read()

data = json.loads(data.replace(" NaN", " -1"))

# Load the application script.
with open("app/twitflix-script.js") as f:
    twitflix = f.read()

# Insert the data.
twitflix = twitflix.replace(
    "const _filmData = null;",
    "const _filmData = {};".format(data)
)

# Save the application script.
with open("app/twitflix.js", "w") as f:
    f.write(twitflix)
