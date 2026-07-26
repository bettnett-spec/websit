import re

with open('platformer.html', 'r') as f:
    content = f.read()

# I also need to ensure that when we wipe platforms, we don't wipe the spawn platform immediately if it's the start of the game,
# but `triggerCheckpoint` is only called when we hit a checkpoint platform.
# But wait, when we hit a checkpoint, if we clear all platforms, the player will fall immediately!
# So we shouldn't remove the platform the player is currently standing on (the checkpoint itself).
# Let's fix that.

fixed_memory_logic = """
                // Clean up old platforms and enemies to prevent memory leak
                const oldPlatforms = platforms;
                platforms = [];
                oldPlatforms.forEach(oldP => {
                    if (oldP !== p) {
                        scene.remove(oldP.mesh);
                    } else {
                        platforms.push(oldP); // keep current checkpoint
                    }
                });

                activeEnemies.forEach(e => scene.remove(e));
                activeEnemies = [];
"""

content = content.replace(
    """                // Clean up old platforms and enemies to prevent memory leak
                platforms.forEach(p => scene.remove(p.mesh));
                platforms = [];
                activeEnemies.forEach(e => scene.remove(e));
                activeEnemies = [];""",
    fixed_memory_logic
)

with open('platformer.html', 'w') as f:
    f.write(content)
