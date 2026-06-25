import re

with open('platformer.html', 'r') as f:
    content = f.read()

# 1. Global vars
content = content.replace('let clock;', 'let clock;\n        let enemies = [];\n        let enemyModel = null;\n')

# 2. Loading enemy
# Find createPlayer and add enemy loader right below astolfo loader
load_enemy = """
            const loader2 = new THREE.GLTFLoader();
            loader2.load('enemy.glb', (gltf) => {
                enemyModel = gltf.scene;
                enemyModel.scale.set(0.08, 0.08, 0.08); // Scale enemy appropriately
                enemyModel.traverse(obj => {
                    if (obj.isMesh) {
                        obj.castShadow = true;
                        obj.receiveShadow = true;
                    }
                });
            });
"""
content = content.replace('isPlayerLoaded = true;\n            });', f'isPlayerLoaded = true;\n            }});\n{load_enemy}')


# 3. Modify generateRandomStage to add enemies
# Add a helper function spawnEnemy
spawn_enemy_func = """
        function spawnEnemy(x, y, z) {
            if (!enemyModel) return;
            const enemyMesh = enemyModel.clone();
            enemyMesh.position.set(x, y, z);
            scene.add(enemyMesh);
            enemies.push({ mesh: enemyMesh, startX: x, startZ: z, phase: Math.random() * Math.PI * 2 });
        }
"""
content = content.replace('function generateRandomStage() {', f'{spawn_enemy_func}\n        function generateRandomStage() {{')

# Replace createPlatform calls inside the generation loop to also potentially spawn enemies
content = content.replace("createPlatform(curX, curY, curZ, w, 1, d, stageColor);", "createPlatform(curX, curY, curZ, w, 1, d, stageColor);\n                    if(Math.random() < 0.5) spawnEnemy(curX, curY + 0.5, curZ);")
content = content.replace("createPlatform(curX, curY, curZ, 1.2, 1, len, stageColor);", "createPlatform(curX, curY, curZ, 1.2, 1, len, stageColor);\n                     if(Math.random() < 0.5) spawnEnemy(curX, curY + 0.5, curZ);")
content = content.replace("createPlatform(curX, curY, curZ, 2, 1, 2, stageColor);", "createPlatform(curX, curY, curZ, 2, 1, 2, stageColor);\n                        if(Math.random() < 0.2) spawnEnemy(curX, curY + 0.5, curZ);")

# 4. Animate enemies and handle collisions in checkPhysics or animate
enemy_logic = """
            // Enemy animation and collision
            const playerRadius = 0.4;
            const enemyRadius = 0.5;
            for (let e of enemies) {
                // Bobbing/moving animation
                e.phase += dt * 2;
                e.mesh.position.y += Math.sin(e.phase) * 0.005;
                e.mesh.rotation.y += 0.02;

                // Collision detection
                if (playerMesh && isPlayerLoaded) {
                    const dx = playerMesh.position.x - e.mesh.position.x;
                    const dy = playerMesh.position.y - e.mesh.position.y;
                    const dz = playerMesh.position.z - e.mesh.position.z;
                    const distSq = dx*dx + dy*dy + dz*dz;

                    if (distSq < (playerRadius + enemyRadius) * (playerRadius + enemyRadius)) {
                        respawn('fire'); // Die if touching enemy
                    }
                }
            }
"""
content = content.replace('checkPhysics(dt);', f'{enemy_logic}\n            checkPhysics(dt);')


with open('platformer.html', 'w') as f:
    f.write(content)
