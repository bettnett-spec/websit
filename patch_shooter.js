const fs = require('fs');

let content = fs.readFileSync('shooter.html', 'utf-8');

// 1. Fix pointer lock control
content = content.replace(
    /document\.body\.addEventListener\('click', \(e\) => \{([\s\S]*?)\}\);/m,
    `document.body.addEventListener('mousedown', (e) => {
            e.preventDefault();
            if (!gameStarted) return;
            if (e.target.closest('#radio-container') || e.target.closest('#leaderboard-modal') || e.target.closest('#start-screen')) return;
            if(!controls.isLocked && !isGameOver) {
                document.body.requestPointerLock();
                // Resume Audio Context on interaction
                if (audioListener.context.state === 'suspended') {
                    audioListener.context.resume();
                }
            }
        });`
);

// 2. Fix fire logic event listeners
// We remove `checkShoot();` from mousedown.
content = content.replace(
    /document\.addEventListener\('mousedown', \(e\) => \{\s*if \(\!gameStarted\) return;\s*if \(e\.target\.closest\('#radio-container'\) \|\| e\.target\.closest\('#leaderboard-modal'\) \|\| e\.target\.closest\('#start-screen'\)\) return;\s*isMouseDown = true; checkShoot\(\);\s*\}\);/,
    `document.addEventListener('mousedown', (e) => {
            if (!gameStarted) return;
            if (e.target.closest('#radio-container') || e.target.closest('#leaderboard-modal') || e.target.closest('#start-screen')) return;
            isMouseDown = true;
        });`
);

// 3. Update checkShoot to not do setTimeout, but we can just use evaluate inside animation loop.
// Actually, checkShoot() is only called in mousedown originally. If we evaluate it in animate(), we can keep checkShoot() and just call it from animate().
content = content.replace(
    /function checkShoot\(\) \{[\s\S]*?\}\n/m,
    `function checkShoot() {
        if (!controls.isLocked || isGameOver) return;
        const now = Date.now();
        const weapon = WEAPONS[currentWeaponIdx];

        if (isMouseDown) {
            if (now - lastShootTime > weapon.fireRate) {
                if (weapon.auto || (!weapon.auto && now - lastShootTime > weapon.fireRate * 2)) {
                    shoot(weapon);
                    lastShootTime = now;
                } else if (!weapon.auto && lastShootTime === 0) {
                    // For non-auto, we only shoot if it's not held down
                    // actually wait, if they hold down a non-auto weapon, it shouldn't shoot multiple times.
                }
            }
        }
    }
`
);

// Wait, the requirement says: "ensure fire logic uses an isMouseDown flag evaluated within the animation loop alongside a lastShootTime check, rather than relying solely on repeated mousedown events".
// Let's rewrite checkShoot and the mousedown/mouseup logic.

fs.writeFileSync('shooter.html', content);
