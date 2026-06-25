import re

with open('platformer.html', 'r') as f:
    content = f.read()

# Change background color
content = content.replace('scene.background = new THREE.Color(0x87CEEB);', 'scene.background = new THREE.Color(0x1a1a2e);')
content = content.replace('scene.fog = new THREE.Fog(0x87CEEB, 20, 150);', 'scene.fog = new THREE.Fog(0x1a1a2e, 20, 150);')
content = content.replace('background-color: #87CEEB;', 'background-color: #1a1a2e;')

# Change AmbientLight
content = content.replace('const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);', 'const ambientLight = new THREE.AmbientLight(0xaaaaaa, 0.4);')

# Change DirectionalLight
content = content.replace('const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);', 'const dirLight = new THREE.DirectionalLight(0x8888ff, 0.6);')

with open('platformer.html', 'w') as f:
    f.write(content)
