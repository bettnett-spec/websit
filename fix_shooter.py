import re

with open('shooter.html', 'r') as f:
    content = f.read()

content = content.replace('new THREE.Vector3().copy(physicsBody.position)', 'new THREE.Vector3(physicsBody.position.x, physicsBody.position.y, physicsBody.position.z)')
content = content.replace('const start = new THREE.Vector3().copy(startCannon);', 'const start = new THREE.Vector3(startCannon.x, startCannon.y, startCannon.z);')
content = content.replace('const end = new THREE.Vector3().copy(endCannon);', 'const end = new THREE.Vector3(endCannon.x, endCannon.y, endCannon.z);')
content = content.replace('e.debugMesh.position.copy(e.body.position);', 'e.debugMesh.position.set(e.body.position.x, e.body.position.y, e.body.position.z);')
content = content.replace('e.debugMesh.quaternion.copy(e.body.quaternion);', 'e.debugMesh.quaternion.set(e.body.quaternion.x, e.body.quaternion.y, e.body.quaternion.z, e.body.quaternion.w);')
content = content.replace('e.mesh.position.copy(e.body.position);', 'e.mesh.position.set(e.body.position.x, e.body.position.y, e.body.position.z);')
content = content.replace('e.mesh.quaternion.copy(e.body.quaternion);', 'e.mesh.quaternion.set(e.body.quaternion.x, e.body.quaternion.y, e.body.quaternion.z, e.body.quaternion.w);')
content = content.replace('const dist = new THREE.Vector3().copy(e.body.position).distanceTo(new THREE.Vector3().copy(physicsBody.position));', 'const dist = new THREE.Vector3(e.body.position.x, e.body.position.y, e.body.position.z).distanceTo(new THREE.Vector3(physicsBody.position.x, physicsBody.position.y, physicsBody.position.z));')
content = content.replace('const dir = new THREE.Vector3().subVectors(new THREE.Vector3().copy(physicsBody.position), new THREE.Vector3().copy(e.body.position));', 'const dir = new THREE.Vector3().subVectors(new THREE.Vector3(physicsBody.position.x, physicsBody.position.y, physicsBody.position.z), new THREE.Vector3(e.body.position.x, e.body.position.y, e.body.position.z));')
content = content.replace('const dir = new THREE.Vector3().subVectors(new THREE.Vector3().copy(e.body.position), new THREE.Vector3().copy(physicsBody.position));', 'const dir = new THREE.Vector3().subVectors(new THREE.Vector3(e.body.position.x, e.body.position.y, e.body.position.z), new THREE.Vector3(physicsBody.position.x, physicsBody.position.y, physicsBody.position.z));')

with open('shooter.html', 'w') as f:
    f.write(content)
