import re

with open('shooter.html', 'r') as f:
    content = f.read()

# 1. PointerLockControls fix
content = re.sub(
    r"document\.body\.addEventListener\('click', \(e\) => \{([^}]*?if\(!controls\.isLocked[^}]*?)controls\.lock\(\);([^}]*?)\}\);",
    r"document.body.addEventListener('mousedown', (e) => {\n            e.preventDefault();\1document.body.requestPointerLock();\2});",
    content,
    flags=re.DOTALL
)

# 2. Fire logic
# Remove `isMouseDown = true; checkShoot();` from mousedown
content = re.sub(
    r"document\.addEventListener\('mousedown', \(e\) => \{([\s\S]*?)isMouseDown = true; checkShoot\(\);\s*\}\);",
    r"document.addEventListener('mousedown', (e) => {\1isMouseDown = true;\n        });",
    content
)

# Modify checkShoot to only shoot, not loop, and not check isMouseDown (we'll check it in animate)
# Wait, checkShoot has:
# if (weapon.auto && isMouseDown) {
#    setTimeout(() => checkShoot(), weapon.fireRate);
# }
# We need to remove the setTimeout and rely on animate loop.
content = re.sub(
    r"function checkShoot\(\) \{[\s\S]*?\}\n\n    function shoot",
    r"""function checkShoot() {
        if (!controls.isLocked || isGameOver) return;
        const now = Date.now();
        const weapon = WEAPONS[currentWeaponIdx];

        if (now - lastShootTime > weapon.fireRate) {
            shoot(weapon);
            lastShootTime = now;
        }
    }

    let isMouseJustPressed = false;
    document.addEventListener('mousedown', (e) => {
        if (!gameStarted) return;
        if (e.target.closest('#radio-container') || e.target.closest('#leaderboard-modal') || e.target.closest('#start-screen')) return;
        isMouseDown = true;
        isMouseJustPressed = true;
    });

    function shoot""",
    content
)

# And inside animate(), we evaluate it:
content = re.sub(
    r"requestAnimationFrame\(animate\);\n        const dt = clock\.getDelta\(\);",
    r"""requestAnimationFrame(animate);
        const dt = clock.getDelta();

        if (controls.isLocked && !isGameOver) {
            const weapon = WEAPONS[currentWeaponIdx];
            if (isMouseDown) {
                if (weapon.auto) {
                    checkShoot();
                } else if (isMouseJustPressed) {
                    checkShoot();
                }
            }
            isMouseJustPressed = false;
        }""",
    content
)

# 3. THREE conversion fixes
content = content.replace("new THREE.Vector3().copy(physicsBody.position)", "new THREE.Vector3(physicsBody.position.x, physicsBody.position.y, physicsBody.position.z)")
content = content.replace("new THREE.Vector3().copy(startCannon)", "new THREE.Vector3(startCannon.x, startCannon.y, startCannon.z)")
content = content.replace("new THREE.Vector3().copy(endCannon)", "new THREE.Vector3(endCannon.x, endCannon.y, endCannon.z)")
content = content.replace("camera.position.copy(physicsBody.position)", "camera.position.set(physicsBody.position.x, physicsBody.position.y, physicsBody.position.z)")
content = content.replace("e.debugMesh.position.copy(e.body.position)", "e.debugMesh.position.set(e.body.position.x, e.body.position.y, e.body.position.z)")
content = content.replace("e.debugMesh.quaternion.copy(e.body.quaternion)", "e.debugMesh.quaternion.set(e.body.quaternion.x, e.body.quaternion.y, e.body.quaternion.z, e.body.quaternion.w)")
content = content.replace("e.mesh.position.copy(e.body.position)", "e.mesh.position.set(e.body.position.x, e.body.position.y, e.body.position.z)")
content = content.replace("e.mesh.quaternion.copy(e.body.quaternion)", "e.mesh.quaternion.set(e.body.quaternion.x, e.body.quaternion.y, e.body.quaternion.z, e.body.quaternion.w)")
content = content.replace("new THREE.Vector3().copy(e.body.position)", "new THREE.Vector3(e.body.position.x, e.body.position.y, e.body.position.z)")

with open('shooter.html', 'w') as f:
    f.write(content)
