import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt

points = np.array([[-1, -1, -1],
                  [1, -1, -1 ]])

Z = points
Z = 10.0*Z
ZZ = 1.2*Z
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

r = 20
ax.set_xlim(-r, r)
ax.set_ylim(-r, r)
ax.set_zlim(-r, r)

verts2 = [[10,0,0],[10,10,10]]
#ax.scatter3D(Z[:,0], Z[:,0])
dat = Poly3DCollection(Z, facecolors='red', linewidths=1, edgecolors='r', alpha=.20)
ax.add_collection3d(dat)
ax.add_collection3d(Poly3DCollection(ZZ, facecolors='red', linewidths=1, edgecolors='r', alpha=.20))



#line1, = plt.plot((10,0,0),(0,10,10))

print(dat)

#plt.show()

plt.ion()

i = 0
while True:
    verts2 = [[10+i*0.1,0,0],[10,10,10]]
    dat.set_verts(verts2)
    i=+1
    
    plt.draw()
    plt.pause(0.05)

# このページを参考に作成中
# https://www.yutaka-note.com/entry/matplotlib_func_anim
# http://naga-tsuzuki.sblo.jp/article/178008842.html
