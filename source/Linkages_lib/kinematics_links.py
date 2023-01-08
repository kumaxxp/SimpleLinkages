import math

# kinematics_links クラスは

class kinematics_links:
    def inverse(x, y, l1, l2, l3, l4):
        theta1 = math.atan2(y, x)
        c2 = (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)
        s2 = math.sqrt(1 - c2**2)
        theta2 = math.atan2(s2, c2)
        theta3 = math.atan2(s2, -c2)
        theta4 = math.atan2(y - l1*math.sin(theta1) - l2*math.sin(theta1 + theta2),
                        x - l1*math.cos(theta1) - l2*math.cos(theta1 + theta2))
    
        return theta1, theta2, theta3, theta4

    def forward(theta1, theta2, theta3, theta4, l1, l2, l3, l4):
        x1 = l1 * math.cos(theta1)
        y1 = l1 * math.sin(theta1)
        x2 = x1 + l2 * math.cos(theta1 + theta2)
        y2 = y1 + l2 * math.sin(theta1 + theta2)
        x3 = x2 + l3 * math.cos(theta1 + theta2 + theta3)
        y3 = y2 + l3 * math.sin(theta1 + theta2 + theta3)
        x4 = x3 + l4 * math.cos(theta1 + theta2 + theta3 + theta4)
        y4 = y3 + l4 * math.sin(theta1 + theta2 + theta3 + theta4)
    
        return x4, y4

