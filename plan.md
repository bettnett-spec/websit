1. **Fix Bugs in Shooter Game**
   - Replace uses of `.copy()` with Cannon vectors when setting THREE.Vector3 objects to fix Cannon object copy crashes.
   - Fix pointer lock controls to use `mousedown` and `e.preventDefault()` to prevent text selection and mouse skipping issues.
2. **Upgrade Platformer Game**
   - Import THREE.SkeletonUtils in platformer.html to allow cloning of enemy models properly (`<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/utils/SkeletonUtils.js"></script>`).
   - Load an enemy model (e.g., `enemy.glb`) using `GLTFLoader`.
   - Add a global `ASSETS` variable and store the loaded model.
   - Inside `generateRandomStage()`, add logic to randomly spawn enemies on platforms (cloned using `SkeletonUtils.clone()`).
   - Implement simple enemy AI logic (e.g., moving back and forth on their platform).
   - Add basic combat mechanics (player takes damage or respawns if touching an enemy).
3. **Pre-commit Checks**
   - Run necessary verification (python script checks/screencap).
   - Clean up temporary files.
4. **Submit**
