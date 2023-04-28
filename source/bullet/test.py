import pybullet as p

# 物理シミュレーションの初期化
physicsClient = p.connect(p.GUI)  # GUIを使って描画
p.setGravity(0,0,-10)  # 重力の設定

# 床の作成
planeId = p.createCollisionShape(p.GEOM_PLANE)
p.createMultiBody(0, planeId)

# 立方体の物体の作成
boxId = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.5])
boxStartPos = [0, 0, 1]
boxStartOrientation = p.getQuaternionFromEuler([0,0,0])
boxMass = 1
boxUniqueId = p.createMultiBody(boxMass, boxId, -1, boxStartPos, boxStartOrientation)

import time

# シミュレーションの実行
for i in range(10000):
    p.stepSimulation()
    time.sleep(1./240.)  # シミュレーションのフレームレートを設定

    # 立方体の位置と姿勢を取得
    boxPos, boxOrn = p.getBasePositionAndOrientation(boxUniqueId)

    # 立方体が地面から離れすぎた場合、シミュレーションを終了する
#    if boxPos[2] < 0.5:
#        break

# 物理シミュレーションの終了
p.disconnect()

