import cmath
import numpy as np
import math
Effect_Areas = [[0, 1], [0, 2], [0, 3],
    [1, 0], [2, 0], [3, 0],
    [0, -1], [0, -2], [0, -3],
    [-1, 0], [-2, 0], [-3, 0],
    [1, 1], [2, 2],
    [-1, 1], [-2, 2],
    [-1, -1], [-2, -2],
    [1, -1], [2, -2],
    [2, 1], [1, 2],
    [-2, 1], [-1, 2],
    [-2, -1], [-1, -2],
    [2, -1], [1, -2],
]

def GetChessValue(xx,yy):
    ChessValue = 0;
    for para in Effect_Areas:
        if xx + para[0] >= 0 and xx + para[0] < 9 and yy + para[1] >= 0 and yy + para[1] < 9:
            if ((xx + para[0] == 0 or xx + para[0] == 8) and (yy + para[1] == 0 or yy + para[1] == 8)):
                ChessValue = ChessValue + 4 * GetEffectValue(xx + para[0], yy + para[1], xx, yy)
            elif ((xx + para[0] == 0 or xx + para[0] == 8) and (yy + para[1] == 1 or yy + para[1] == 7)):
                ChessValue = ChessValue + 3.5 * GetEffectValue(xx + para[0], yy + para[1], xx, yy)
            elif ((xx + para[0] == 1 or xx + para[0] == 7) and (yy + para[1] == 1 or yy + para[1] == 7)):
                ChessValue = ChessValue + 3 * GetEffectValue(xx + para[0], yy + para[1], xx, yy)
            elif ((xx + para[0] == 1 or xx + para[0] == 7) and (yy + para[1] == 0 or yy + para[1] == 8)):
                ChessValue = ChessValue + 3.5 * GetEffectValue(xx + para[0], yy + para[1], xx, yy)
            else:
                ChessValue = ChessValue + GetEffectValue(xx + para[0], yy + para[1], xx, yy)
    return ChessValue

def GetEffectValue(xx,yy,x,y):
    distance = cmath.sqrt((xx - x) * (xx - x) + (yy - y) * (yy - y))
    if distance == 1:
        return 21
    elif distance == cmath.sqrt(2):
        return 15
    elif distance == 2:
        return 8
    elif distance == cmath.sqrt(5):
        return 5
    elif distance == cmath.sqrt(8):
        return 2
    elif distance == 3:
        return 3
    else:
        return 0




valueBoard = np.array([
[0.0,137.0,166.0,189.0,165.0,189.0,266.0,137.0,0.0,],
[137.0,291.0,322.5,247.0,223.0,247.0,322.5,291.0,137.0,],
[166.0,322.5,291.0,248.0,233.0,248.0,291.0,322.5,266.0,],
[189.0,247.0,248.0,240.0,236.0,240.0,248.0,247.0,189.0,],
[165.0,223.0,233.0,236.0,236.0,236.0,233.0,223.0,165.0,],
[189.0,247.0,248.0,240.0,236.0,240.0,248.0,247.0,189.0,],
[166.0,322.5,291.0,248.0,233.0,248.0,291.0,322.5,166.0,],
[137.0,291.0,322.5,247.0,223.0,247.0,322.5,291.0,137.0,],
[0.0,137.0,166.0,189.0,165.0,189.0,166.0,137.0,0.0,],
])

def GetDistributedBoard():
    sum = 0
    s = []
    for i in range(9):
        for j in range(9):
            valueBoard[i][j] = valueBoard[i][j] / 100;
            sum += math.e ** (0.7 * valueBoard[i][j]);

    for i in range(9):
        for j in range(9):
            s.append((math.e ** (0.7 * valueBoard[i][j]))/sum)

    return s