<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Escape the Femboy</title>
    <style>
        body { margin: 0; overflow: hidden; background: #87CEEB; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        
        /* UI Layer */
        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        /* HUD Styles */
        #hud {
            padding: 20px;
            color: #333;
            background: rgba(255, 255, 255, 0.5);
            border-bottom-right-radius: 15px;
            width: fit-content;
        }
        h2 { margin: 0; color: #ff69b4; text-shadow: 1px 1px 0 #fff; }
        p { font-weight: bold; }

        /* Inventory Slots */
        .item-slot {
            display: inline-block;
            width: 60px;
            height: 60px;
            border: 3px solid #fff;
            background: rgba(0,0,0,0.1);
            border-radius: 10px;
            margin-right: 10px;
            text-align: center;
            line-height: 60px;
            font-size: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .item-found { 
            border-color: #ff69b4; 
            background: rgba(255, 105, 180, 0.2); 
            transform: scale(1.1);
        }
        
        /* Messages */
        #message {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #ff007f;
            font-size: 50px;
            font-weight: 900;
            display: none;
            text-shadow: 2px 2px 0 #fff;
            text-align: center;
            background: rgba(255,255,255,0.9);
            padding: 20px 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }

        /* Start Screen */
        #start-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #444;
            pointer-events: auto;
            z-index: 10;
        }
        button {
            padding: 15px 40px;
            font-size: 22px;
            cursor: pointer;
            background: #ff69b4;
            color: white;
            border: none;
            border-radius: 30px;
            margin-top: 20px;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
            transition: transform 0.2s;
        }
        button:hover { transform: scale(1.05); background: #ff1493; }
        
        /* Crosshair */
        #crosshair {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 12px;
            height: 12px;
            background: #333;
            border: 2px solid white;
            border-radius: 50%;
            transform: translate(-50%, -50%);
        }
        #interact-hint {
            position: absolute;
            top: 58%;
            left: 50%;
            transform: translateX(-50%);
            color: #333;
            font-weight: bold;
            font-size: 18px;
            background: rgba(255,255,255,0.8);
            padding: 5px 15px;
            border-radius: 20px;
            display: none;
        }
    </style>
</head>
<body>

    <div id="ui-layer">
        <div id="hud">
            <h2>ESCAPE THE HOUSE</h2>
            <div id="inventory">
                <div id="slot-key" class="item-slot">🔑</div>
                <div id="slot-crowbar" class="item-slot">🔨</div>
                <div id="slot-fuse" class="item-slot">🥤</div>
            </div>
            <p>Find the Key, Hammer, and Drink to unlock the door!</p>
        </div>
    </div>

    <div id="crosshair"></div>
    <div id="interact-hint">Press E to Interact</div>
    <div id="message">GAME OVER</div>

    <div id="start-screen">
        <h1 style="color: #ff69b4; font-size: 4em; margin-bottom: 0;">ESCAPE THE FEMBOY</h1>
        <h3 style="margin-top: 10px;">Don't let him catch you!</h3>
        <p>Gather the items. Unlock the door.</p>
        <p>Controls: WASD to Move | Mouse to Look | E to Interact</p>
        <button id="start-btn">START GAME</button>
    </div>

    <!-- Three.js Libraries -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/PointerLockControls.js"></script>

    <script>
        // --- GAME CONFIGURATION ---
        const PLAYER_SPEED = 0.18;
        const ENEMY_SPEED = 0.11; // Chaser speed
        const INTERACTION_DISTANCE = 5;
        
        // --- SCENE SETUP ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x87CEEB); // Nice Sky Blue
        
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.body.appendChild(renderer.domElement);

        // --- LIGHTING (Bright & Modern) ---
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7); // Bright ambient light
        scene.add(ambientLight);

        const sunLight = new THREE.DirectionalLight(0xffffff, 0.8);
        sunLight.position.set(50, 100, 50);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 2048;
        sunLight.shadow.mapSize.height = 2048;
        scene.add(sunLight);

        // --- LEVEL GENERATION (Modern House) ---
        const walls = [];
        // Floor
        const floorGeometry = new THREE.PlaneGeometry(100, 100);
        const floorMaterial = new THREE.MeshStandardMaterial({ color: 0xe0e0e0 }); // Light gray floor
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        scene.add(floor);

        // Ceiling
        const ceiling = new THREE.Mesh(floorGeometry, new THREE.MeshBasicMaterial({ color: 0xffffff }));
        ceiling.rotation.x = Math.PI / 2;
        ceiling.position.y = 5;
        scene.add(ceiling);

        // Walls Material
        const wallMat = new THREE.MeshStandardMaterial({ color: 0xfff0f5 }); // Lavender Blush

        function createWall(x, z, width, depth, height = 5) {
            const geo = new THREE.BoxGeometry(width, height, depth);
            const wall = new THREE.Mesh(geo, wallMat);
            wall.position.set(x, height / 2, z);
            wall.castShadow = true;
            wall.receiveShadow = true;
            scene.add(wall);
            walls.push(new THREE.Box3().setFromObject(wall));
            return wall;
        }

        // Layout
        createWall(0, -20, 40, 1);
        createWall(0, 20, 40, 1);
        createWall(-20, 0, 1, 40);
        createWall(20, 0, 1, 40);

        // Interior Walls
        createWall(-5, -5, 1, 15);
        createWall(10, 5, 20, 1);
        createWall(-10, 10, 1, 10);
        createWall(5, -10, 10, 1);

        // --- GAME OBJECTS ---
        const objects = [];
        let itemsCollected = { key: false, crowbar: false, fuse: false };
        let gameActive = false;
        let gameOver = false;

        // Player controls
        const controls = new THREE.PointerLockControls(camera, document.body);
        const velocity = new THREE.Vector3();
        const direction = new THREE.Vector3();
        const moveState = { forward: false, backward: false, left: false, right: false };

        // Items
        function spawnItem(type, color, x, z) {
            const geo = new THREE.BoxGeometry(0.5, 0.5, 0.5);
            const mat = new THREE.MeshStandardMaterial({ color: color });
            const item = new THREE.Mesh(geo, mat);
            item.position.set(x, 1, z);
            item.userData = { type: type };
            item.userData.floatOffset = Math.random() * 100;
            scene.add(item);
            objects.push(item);
        }

        spawnItem('key', 0xffd700, -15, 15);    // Gold Key
        spawnItem('crowbar', 0x808080, 15, -15); // Hammer/Crowbar
        spawnItem('fuse', 0xff69b4, -15, -15);   // Pink Drink/Fuse

        // Exit Door
        const doorGeo = new THREE.BoxGeometry(4, 5, 0.5);
        const doorMat = new THREE.MeshStandardMaterial({ color: 0x4B0082 }); // Indigo door
        const exitDoor = new THREE.Mesh(doorGeo, doorMat);
        exitDoor.position.set(0, 2.5, 19.5);
        exitDoor.userData = { type: 'door' };
        scene.add(exitDoor);
        objects.push(exitDoor);

        // --- CHARACTER / ENEMY SETUP ---
        const enemyGroup = new THREE.Group();
        scene.add(enemyGroup);
        let mixer = null; // Animation mixer

        // Placeholder (shown while loading or if loading fails)
        const placeholderGeo = new THREE.CylinderGeometry(0.5, 0.5, 1.8, 16);
        const placeholderMat = new THREE.MeshStandardMaterial({ color: 0xff69b4 }); // Pink placeholder
        const placeholderMesh = new THREE.Mesh(placeholderGeo, placeholderMat);
        placeholderMesh.position.y = 0.9;
        enemyGroup.add(placeholderMesh);
        enemyGroup.position.set(0, 0, -10);

        // --- LOAD YOUR MODEL ---
        const gltfLoader = new THREE.GLTFLoader();
        
        // Ensure this filename matches your upload exactly
        const modelURL = './astolfo_school_uniform.glb'; 

        gltfLoader.load(modelURL, (gltf) => {
            console.log("Model Loaded Successfully!");
            const model = gltf.scene;
            
            // Adjust Scale - Usually models are too big or too small
            // Tweak these numbers if he looks like a giant or an ant
            model.scale.set(1, 1, 1); 
            
            model.traverse((c) => {
                if(c.isMesh) c.castShadow = true;
            });

            // Remove placeholder
            enemyGroup.remove(placeholderMesh);
            
            // Center the model in the group
            model.position.y = 0; 
            enemyGroup.add(model);

            // --- ANIMATION SETUP ---
            // This checks if the file has built-in animations (like walking)
            if(gltf.animations && gltf.animations.length > 0) {
                mixer = new THREE.AnimationMixer(model);
                // Play the first animation found (usually Walk or Idle)
                const action = mixer.clipAction(gltf.animations[0]);
                action.play();
            }

        }, undefined, (error) => {
            console.warn('Model not found. Ensure .glb file is in the same folder.', error);
        });

        // --- INPUT HANDLING ---
        const onKeyDown = (e) => {
            switch(e.code) {
                case 'KeyW': moveState.forward = true; break;
                case 'KeyA': moveState.left = true; break;
                case 'KeyS': moveState.backward = true; break;
                case 'KeyD': moveState.right = true; break;
                case 'KeyE': tryInteract(); break;
            }
        };
        const onKeyUp = (e) => {
            switch(e.code) {
                case 'KeyW': moveState.forward = false; break;
                case 'KeyA': moveState.left = false; break;
                case 'KeyS': moveState.backward = false; break;
                case 'KeyD': moveState.right = false; break;
            }
        };

        document.addEventListener('keydown', onKeyDown);
        document.addEventListener('keyup', onKeyUp);

        document.getElementById('start-btn').addEventListener('click', () => controls.lock());

        controls.addEventListener('lock', () => {
            gameActive = true;
            document.getElementById('start-screen').style.display = 'none';
        });
        controls.addEventListener('unlock', () => {
            if(!gameOver) {
                document.getElementById('start-screen').style.display = 'flex';
                document.getElementById('start-btn').textContent = "RESUME";
                gameActive = false;
            }
        });

        // --- LOGIC ---
        const clock = new THREE.Clock();
        const raycaster = new THREE.Raycaster();

        function tryInteract() {
            raycaster.setFromCamera(new THREE.Vector2(0,0), camera);
            const intersects = raycaster.intersectObjects(objects);

            if (intersects.length > 0 && intersects[0].distance < INTERACTION_DISTANCE) {
                const obj = intersects[0].object;
                
                if (obj.userData.type === 'key') {
                    itemsCollected.key = true;
                    document.getElementById('slot-key').classList.add('item-found');
                    scene.remove(obj);
                } else if (obj.userData.type === 'crowbar') {
                    itemsCollected.crowbar = true;
                    document.getElementById('slot-crowbar').classList.add('item-found');
                    scene.remove(obj);
                } else if (obj.userData.type === 'fuse') {
                    itemsCollected.fuse = true;
                    document.getElementById('slot-fuse').classList.add('item-found');
                    scene.remove(obj);
                } else if (obj.userData.type === 'door') {
                    if (itemsCollected.key && itemsCollected.crowbar && itemsCollected.fuse) {
                        endGame(true);
                    } else {
                        showMessage("Door is locked! Find items.");
                    }
                }
            }
        }

        function updateEnemy(delta) {
            if (!gameActive || gameOver) return;

            const playerPos = camera.position;
            const enemyPos = enemyGroup.position;
            
            const dx = playerPos.x - enemyPos.x;
            const dz = playerPos.z - enemyPos.z;
            const distance = Math.sqrt(dx*dx + dz*dz);

            // Move enemy
            if (distance > 1.2) {
                enemyGroup.position.x += (dx / distance) * ENEMY_SPEED;
                enemyGroup.position.z += (dz / distance) * ENEMY_SPEED;
                enemyGroup.lookAt(playerPos.x, enemyGroup.position.y, playerPos.z);
            }

            // Update Animation
            if (mixer) mixer.update(delta);

            // Catch Condition
            if (distance < 1.5) {
                endGame(false);
            }
        }

        function checkInteraction() {
            raycaster.setFromCamera(new THREE.Vector2(0,0), camera);
            const intersects = raycaster.intersectObjects(objects);
            const hint = document.getElementById('interact-hint');
            
            if (intersects.length > 0 && intersects[0].distance < INTERACTION_DISTANCE) {
                hint.style.display = 'block';
                hint.textContent = intersects[0].object.userData.type === 'door' ? "Unlock Door" : "Pick Up";
            } else {
                hint.style.display = 'none';
            }
        }

        function showMessage(text) {
            const el = document.getElementById('message');
            el.textContent = text;
            el.style.display = 'block';
            setTimeout(() => { if(!gameOver) el.style.display = 'none'; }, 2000);
        }

        function endGame(won) {
            gameActive = false;
            gameOver = true;
            controls.unlock();
            const msg = document.getElementById('message');
            msg.style.display = 'block';
            msg.style.color = won ? '#00cc00' : '#ff007f';
            msg.textContent = won ? "YOU ESCAPED!" : "CAUGHT YOU!";
            
            // Simple auto-reload
            setTimeout(() => location.reload(), 3000);
        }

        function animate() {
            requestAnimationFrame(animate);

            if (gameActive) {
                const delta = clock.getDelta();

                // Physics/Movement
                velocity.x -= velocity.x * 10.0 * delta;
                velocity.z -= velocity.z * 10.0 * delta;

                direction.z = Number(moveState.forward) - Number(moveState.backward);
                direction.x = Number(moveState.right) - Number(moveState.left);
                direction.normalize();

                if (moveState.forward || moveState.backward) velocity.z -= direction.z * 400.0 * delta * PLAYER_SPEED;
                if (moveState.left || moveState.right) velocity.x -= direction.x * 400.0 * delta * PLAYER_SPEED;

                controls.moveRight(-velocity.x * delta);
                controls.moveForward(-velocity.z * delta);
                
                // Boundaries
                if (camera.position.x > 19) camera.position.x = 19;
                if (camera.position.x < -19) camera.position.x = -19;
                if (camera.position.z > 19) camera.position.z = 19;
                if (camera.position.z < -19) camera.position.z = -19;

                // Animate Items (Spinning)
                const time = Date.now() * 0.002;
                objects.forEach(obj => {
                    if (obj.userData.type !== 'door') {
                        obj.rotation.y += 0.02;
                        obj.position.y = 1 + Math.sin(time + obj.userData.floatOffset) * 0.2;
                    }
                });

                updateEnemy(delta);
                checkInteraction();
            }

            renderer.render(scene, camera);
        }

        // Initialize
        camera.position.set(15, 1.6, 15);
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
