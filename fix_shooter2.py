import re

with open('shooter.html', 'r') as f:
    content = f.read()

content = content.replace("enemy.body.position.copy(pos);", "enemy.body.position.set(pos.x, pos.y, pos.z);")
content = content.replace("flash.position.copy(start);", "flash.position.set(start.x, start.y, start.z);")

with open('shooter.html', 'w') as f:
    f.write(content)
