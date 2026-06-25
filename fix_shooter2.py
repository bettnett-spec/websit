import re

with open('shooter.html', 'r') as f:
    content = f.read()

content = content.replace('camera.position.copy(physicsBody.position);', 'camera.position.set(physicsBody.position.x, physicsBody.position.y, physicsBody.position.z);')
content = content.replace('new THREE.Vector3().copy(e.body.position)', 'new THREE.Vector3(e.body.position.x, e.body.position.y, e.body.position.z)')

with open('shooter.html', 'w') as f:
    f.write(content)
