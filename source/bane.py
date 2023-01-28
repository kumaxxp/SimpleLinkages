from sympy import symbols, diff, Matrix, lambdify
from sympy.physics.mechanics import dynamicsymbols
from sympy.physics.mechanics import ReferenceFrame, Point, Particle
from sympy.physics.mechanics import LagrangesMethod, Lagrangian

# https://ss1.xrea.com/penguinitis.g1.xrea.com/study/system_control/regulator.html

t = symbols("t")
z1, z2, f1, f2 = dynamicsymbols("z1 z2 f1 f2")
m1, m2, c1, c2, k1, k2 = symbols("m1 m2 c1 c2 k1 k2")
q = Matrix([z1, z2])

N = ReferenceFrame("N")

p1 = Point("p1")
v1 = z1.diff(t)
p1.set_vel(N, v1*N.x)
pa1 = Particle("pa1", p1, m1)
pa1.potential_energy = k1*z1**2/2 + k2*(z2 - z1)**2/2

p2 = Point("p2")
v2 = z2.diff(t)
p2.set_vel(N, v2*N.x)
pa2 = Particle("pa2", p2, m2)

F = c1*v1**2/2 + c2*(v2 - v1)**2/2
fc1 = -F.diff(v1)
fc2 = -F.diff(v2)

fl = [(p1, (f1 + fc1)*N.x), (p2, (f2 + fc2)*N.x)]

L = Lagrangian(N, pa1, pa2)
LM = LagrangesMethod(L, q, forcelist = fl, frame = N)

LM.form_lagranges_equations()
As, Bs, u = LM.linearize(q_ind=q, qd_ind=q.diff(t), A_and_B=True)

import numpy as np

m1n = 1.
m2n = 1.
c1n = 0.5
c2n = 0.5
k1n = 0.2
k2n = 0.2

As_func = lambdify((m1, m2, c1, c2, k1, k2), As, modules="numpy")
A0 = As_func(m1n, m2n, c1n, c2n, k1n, k2n)

Bs_func = lambdify((m1, m2), Bs, modules="numpy")
B0 = Bs_func(m1n, m2n)

C = [0., 1., 0., 0.]
x0 = [0.5, 1., 0., 0.]

dt = 0.1
end_time = 10.
t = np.linspace(0., end_time, int(end_time/dt) + 1)

print(t)

from scipy import signal
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()

#sys = signal.lti(A0, B0, C, D)
sys = signal.lti(A0, B0, C)
t, y, x = signal.lsim(sys, 0., t, x0)

plt.plot(t, x[:, 0], label="$x_1$")
plt.plot(t, x[:, 1], label="$x_2$")
plt.plot(t, x[:, 2], label="$x_3$")
plt.plot(t, x[:, 3], label="$x_4$")
plt.xlim(0., end_time)
plt.xlabel("t")
plt.ylabel("x")
plt.legend()
plt.show()
