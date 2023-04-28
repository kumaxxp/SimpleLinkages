import pybullet as p

physicsClient = p.connect(p.GUI)
p.setGravity(0,0,-10)
#planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0,0,1]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
#boxId = p.loadURDF("./test5/test5_description/urdf/test5.xacro",cubeStartPos, cubeStartOrientation)

obUids = p.loadMJCF("./test5/test5_description/package.xml")
humanoid = obUids[1]

