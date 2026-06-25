import re

with open('platformer.html', 'r') as f:
    content = f.read()

# 1. Update the load callback to spawn queued enemies
# Look for where enemyModel is loaded and add the queue processing logic
content = content.replace(
    'enemyModel = gltf.scene;',
    'enemyModel = gltf.scene;\n                // Process queued enemy spawns\n                for (let pos of enemySpawnQueue) {\n                    const enemyMesh = enemyModel.clone();\n                    enemyMesh.position.set(pos.x, pos.y, pos.z);\n                    scene.add(enemyMesh);\n                    enemies.push({ mesh: enemyMesh, startX: pos.x, startZ: pos.z, phase: Math.random() * Math.PI * 2 });\n                }\n                enemySpawnQueue = [];'
)

# 2. Add enemySpawnQueue to globals
content = content.replace(
    'let enemies = [];\n        let enemyModel = null;',
    'let enemies = [];\n        let enemyModel = null;\n        let enemySpawnQueue = [];'
)

# 3. Update spawnEnemy to either spawn immediately or queue the spawn if not loaded yet
new_spawn_enemy_func = """
        function spawnEnemy(x, y, z) {
            if (!enemyModel) {
                enemySpawnQueue.push({x: x, y: y, z: z});
                return;
            }
            const enemyMesh = enemyModel.clone();
            enemyMesh.position.set(x, y, z);
            scene.add(enemyMesh);
            enemies.push({ mesh: enemyMesh, startX: x, startZ: z, phase: Math.random() * Math.PI * 2 });
        }
"""
# We need to replace the old spawnEnemy function.
old_spawn_enemy_regex = r'function spawnEnemy\(x, y, z\) \{[\s\S]*?\}'
content = re.sub(old_spawn_enemy_regex, new_spawn_enemy_func.strip(), content)


with open('platformer.html', 'w') as f:
    f.write(content)
