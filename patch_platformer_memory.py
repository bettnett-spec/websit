import re

with open('platformer.html', 'r') as f:
    content = f.read()

# We need to remove old enemies explicitly when we trigger a checkpoint or during stage generation.
# In generateRandomStage(), it just keeps generating forward.
# But platforms array keeps growing.
# Let's clear old enemies when generating a new stage in triggerCheckpoint.

memory_logic = """
                // Clean up old platforms and enemies to prevent memory leak
                platforms.forEach(p => scene.remove(p.mesh));
                platforms = [];
                activeEnemies.forEach(e => scene.remove(e));
                activeEnemies = [];
"""

content = content.replace(
    "p.triggered = true;",
    "p.triggered = true;\n" + memory_logic
)

with open('platformer.html', 'w') as f:
    f.write(content)
