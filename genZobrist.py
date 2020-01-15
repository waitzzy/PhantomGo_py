#这个脚本用来生产zobrist算法用的离散值，执行这个文件，并重定向到zobrist.py文件
import random
from collections import namedtuple
from enum import Enum
MAX63 = 2**63-1 #使用64位长的二进制随机序列
sets=set() # 确保不重复
#棋盘的最大宽度是19*19

class Player(Enum): 
    black=0
    white=1

    def next(self):
        return player.white if self==player.black else player.black




while len(sets)<19*19*3+1: #每个下子位有空，黑，白三种状态
    code=random.randint(0,MAX63)
    sets.add(code)

sets=list(sets)

coords=[]
for row in range(19):
    for col in range(19):
        coords.append((row,col))

players=['None','player.black','player.white'] #None是在棋子被提走时起作用的


print("__all__ = ['HASH_CODE', 'EMPTY_BOARD']")

print('HASH_CODE = {')

i=0
for k in coords:
    for j in players:       
        print(' (%r, %s): %r,' % (k, j, sets[i]))
        i+=1
print('}')

print('EMPTY_BOARD = %d' % (sets[-1]))
