import re

with open('platformer.html', 'r') as f:
    content = f.read()

# 1. Fix queue ordering
content = content.replace(
    'enemyModel = gltf.scene;\n                // Process queued enemy spawns',
    'enemyModel = gltf.scene;\n                enemyModel.scale.set(0.08, 0.08, 0.08);\n                enemyModel.traverse(obj => {\n                    if (obj.isMesh) {\n                        obj.castShadow = true;\n                        obj.receiveShadow = true;\n                    }\n                });\n                // Process queued enemy spawns'
)
# Now remove the redundant scale logic from after the loader block
redundant_scale = """                enemyModel.scale.set(0.08, 0.08, 0.08); // Scale enemy appropriately
                enemyModel.traverse(obj => {
                    if (obj.isMesh) {
                        obj.castShadow = true;
                        obj.receiveShadow = true;
                    }
                });"""
content = content.replace(redundant_scale, '')

# 2. Fix animation drift
# Add startY to enemy struct
content = content.replace(
    'enemies.push({ mesh: enemyMesh, startX: pos.x, startZ: pos.z, phase: Math.random() * Math.PI * 2 });',
    'enemies.push({ mesh: enemyMesh, startX: pos.x, startY: pos.y, startZ: pos.z, phase: Math.random() * Math.PI * 2 });'
)
content = content.replace(
    'enemies.push({ mesh: enemyMesh, startX: x, startZ: z, phase: Math.random() * Math.PI * 2 });',
    'enemies.push({ mesh: enemyMesh, startX: x, startY: y, startZ: z, phase: Math.random() * Math.PI * 2 });'
)

# Update the animation logic
old_bobbing = """                // Bobbing/moving animation
                e.phase += dt * 2;
                e.mesh.position.y += Math.sin(e.phase) * 0.005;
                e.mesh.rotation.y += 0.02;"""
new_bobbing = """                // Bobbing/moving animation
                e.phase += dt * 2;
                e.mesh.position.y = e.startY + Math.sin(e.phase) * 0.1;
                e.mesh.rotation.y += 0.02;"""
content = content.replace(old_bobbing, new_bobbing)

with open('platformer.html', 'w') as f:
    f.write(content)
