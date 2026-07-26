import re

with open('platformer.html', 'r') as f:
    content = f.read()

# 1. Add mousedown for shooting
shoot_logic = """
            document.addEventListener('mousedown', (e) => {
                if (!isLocked || !weaponMesh) return;

                const now = Date.now();
                if (now - lastShootTime < 200) return; // Fire rate limit
                lastShootTime = now;

                // Muzzle flash
                if (muzzleLight) {
                    muzzleLight.intensity = 2;
                    setTimeout(() => muzzleLight.intensity = 0, 50);
                }

                // Recoil
                weaponMesh.position.z += 0.05;
                setTimeout(() => { weaponMesh.position.z -= 0.05; }, 80);

                // SFX
                if(sfxAkm) {
                    sfxAkm.currentTime = 0;
                    sfxAkm.play().catch(e => {});
                }

                // Raycast
                raycaster.setFromCamera(new THREE.Vector2(0, 0), camera);
                const intersects = raycaster.intersectObjects(activeEnemies, true);

                if (intersects.length > 0) {
                    let hit = intersects[0].object;
                    let enemyGroup = null;
                    while(hit) {
                        if (hit.userData && hit.userData.isEnemy) {
                            enemyGroup = hit;
                            break;
                        }
                        hit = hit.parent;
                    }

                    if (enemyGroup) {
                        scene.remove(enemyGroup);
                        activeEnemies = activeEnemies.filter(e => e !== enemyGroup);
                    }
                }
            });
"""

content = content.replace(
    "document.addEventListener('pointerlockchange', pointerLockChange);",
    "document.addEventListener('pointerlockchange', pointerLockChange);\n" + shoot_logic
)

# 2. Add collision check in animate/physics
# Let's add it in animate(), after checkPhysics(dt);
collision_logic = """
            // Enemy collision and bounding box update
            const playerPos = playerMesh.position;
            const playerRadius = 0.5; // Approx
            for (let i = 0; i < activeEnemies.length; i++) {
                const enemy = activeEnemies[i];
                enemy.userData.boundingBox.setFromObject(enemy);

                // Simple distance check
                const dx = playerPos.x - enemy.position.x;
                const dy = playerPos.y - enemy.position.y;
                const dz = playerPos.z - enemy.position.z;
                const distSq = dx*dx + dy*dy + dz*dz;

                if (distSq < 1.5) { // 1.5 units squared
                    respawn('death');
                    break; // Prevent multiple triggers
                }
            }
"""

content = content.replace(
    "updateAnimation(time);",
    "updateAnimation(time);\n" + collision_logic
)

with open('platformer.html', 'w') as f:
    f.write(content)
