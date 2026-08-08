with open("shooter.html", "r") as f:
    content = f.read()

content = content.replace("camera.position.copy(physicsBody.position);", "camera.position.set(physicsBody.position.x, physicsBody.position.y, physicsBody.position.z);")
content = content.replace("e.debugMesh.position.copy(e.body.position);", "e.debugMesh.position.set(e.body.position.x, e.body.position.y, e.body.position.z);")
content = content.replace("e.debugMesh.quaternion.copy(e.body.quaternion);", "e.debugMesh.quaternion.set(e.body.quaternion.x, e.body.quaternion.y, e.body.quaternion.z, e.body.quaternion.w);")
content = content.replace("e.mesh.position.copy(e.body.position);", "e.mesh.position.set(e.body.position.x, e.body.position.y, e.body.position.z);")
content = content.replace("e.mesh.quaternion.copy(e.body.quaternion);", "e.mesh.quaternion.set(e.body.quaternion.x, e.body.quaternion.y, e.body.quaternion.z, e.body.quaternion.w);")

with open("shooter.html", "w") as f:
    f.write(content)
