import re

with open('platformer.html', 'r') as f:
    content = f.read()

# Inside generateRandomStage(), after createPlatform(), we'll occasionally spawn an enemy.
# Let's write a function to spawn an enemy on a platform.
spawn_enemy_func = """
        function spawnEnemy(x, y, z) {
            if (!enemyModel) return;
            const enemy = THREE.SkeletonUtils.clone(enemyModel);
            enemy.position.set(x, y + 0.9, z); // Adjust Y based on enemy scale/origin
            enemy.traverse(child => { if(child.isMesh) { child.castShadow = true; child.receiveShadow = true; } });

            // Add a bounding box for collision (using user data)
            const box = new THREE.Box3().setFromObject(enemy);
            enemy.userData = { isEnemy: true, boundingBox: box };

            scene.add(enemy);
            activeEnemies.push(enemy);
        }
"""

content = content.replace("// Helper function to update camera position", spawn_enemy_func + "\n        // Helper function to update camera position")

# Now inject spawnEnemy inside generateRandomStage.
# We will spawn enemies on the wide platform and step platforms.
content = re.sub(
    r"createPlatform\(curX, curY, curZ, w, 1, d, stageColor\);",
    r"createPlatform(curX, curY, curZ, w, 1, d, stageColor);\n                    if (Math.random() < 0.5) spawnEnemy(curX, curY + 0.5, curZ);",
    content
)

content = re.sub(
    r"createPlatform\(curX, curY, curZ, 2, 1, 2, stageColor\);",
    r"createPlatform(curX, curY, curZ, 2, 1, 2, stageColor);\n                        if (s === steps - 1 && Math.random() < 0.5) spawnEnemy(curX, curY + 0.5, curZ);",
    content
)

with open('platformer.html', 'w') as f:
    f.write(content)
