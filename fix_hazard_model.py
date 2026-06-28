import re

with open("platformer.html", "r") as f:
    content = f.read()

# Fix the placement of let hazardModel;
content = content.replace("        let hazardModel = null;", "        // let hazardModel = null;")
content = content.replace("        let hazards = [];", "        // let hazards = [];")

# Define it in Global Variables section
globals_search = """        const PI_2 = Math.PI / 2;

        // --- Global Variables ---"""
globals_replace = """        const PI_2 = Math.PI / 2;

        // --- Global Variables ---
        let hazardModel = null;
        let hazards = [];"""

content = content.replace(globals_search, globals_replace)

with open("platformer.html", "w") as f:
    f.write(content)
