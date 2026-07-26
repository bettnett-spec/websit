import re

with open('platformer.html', 'r') as f:
    content = f.read()

# 1. Add SkeletonUtils and Audio files
content = content.replace(
    '<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>',
    '<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>\n    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/utils/SkeletonUtils.js"></script>'
)

content = content.replace(
    '<!-- SOUND EFFECTS -->',
    '<!-- SOUND EFFECTS -->\n    <audio id="sfx-akm" src="akm.mp3"></audio>'
)

# 2. Add Globals for models and weapon
content = re.sub(
    r"let camera, scene, renderer;\s+let playerMesh;",
    r"let camera, scene, renderer;\n        let playerMesh;\n        let weaponMesh = null;\n        let enemyModel = null;\n        let activeEnemies = [];\n        let raycaster = new THREE.Raycaster();\n        let lastShootTime = 0;\n        let muzzleLight = null;",
    content
)

# 3. Get sfx-akm element
content = content.replace(
    "const sfxWalk = document.getElementById('sfx-walk');",
    "const sfxWalk = document.getElementById('sfx-walk');\n        const sfxAkm = document.getElementById('sfx-akm');"
)

# 4. Initialize GLTFLoader and load models inside init()
init_load_code = """
            // 8. Load Models
            const loader = new THREE.GLTFLoader();
            loader.load('akm.glb', (gltf) => {
                weaponMesh = gltf.scene;
                weaponMesh.scale.set(0.1, 0.1, 0.1);
                weaponMesh.position.set(0.25, -0.4, -0.6); // Relative to camera
                weaponMesh.rotation.y = Math.PI / 2;

                // Add muzzle light
                muzzleLight = new THREE.PointLight(0xffff00, 0, 5);
                muzzleLight.position.set(0, 0.2, -1);
                weaponMesh.add(muzzleLight);

                camera.add(weaponMesh);
            });

            loader.load('enemy.glb', (gltf) => {
                enemyModel = gltf.scene;
                enemyModel.scale.set(0.06, 0.06, 0.06);
            });
"""

content = content.replace(
    "// --- Camera Snap Fix ---",
    init_load_code + "\n\n            // --- Camera Snap Fix ---"
)

# Fix init order so camera is added to scene to make children visible (though perspective camera works without adding if we just want it relative, but for children we should add it)
content = content.replace(
    "camera = new THREE.PerspectiveCamera(85, window.innerWidth / window.innerHeight, 0.1, 1000);",
    "camera = new THREE.PerspectiveCamera(85, window.innerWidth / window.innerHeight, 0.1, 1000);\n            scene.add(camera);"
)

with open('platformer.html', 'w') as f:
    f.write(content)
