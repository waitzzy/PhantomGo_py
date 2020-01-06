
from game import Game
from SGF_Parser.SGF_Parser import sgfPaserSingle
from utility.HDF5 import *
import numpy as np
import glob

game=Game()
parser=sgfPaserSingle()
dir_sgf='./SGF_Parser/sgf_data1/'
dir_npz='./SGF_Parser/npz1/'

'''for test reason
parser.setFile('./SGF_Parser/sgf_data1/kgs-19-2006/2006-02-08-11.sgf')

[b_moves,w_moves]=parser.extractHandi()
game.setHandicaps(b_moves,w_moves) #初始化让棋的子
#print("===============")
#print(game.getFrame())
#print("===============")
moves=parser.extractMoves()
for i in moves:
    if not None in i:
        who=i[0]
        if who=='b':
            who=Player.black
        elif who=='w':
            who=Player.white
        else:
            pass
        move=i[1]        
        #print("===============")
        #print(game.getFrame())
        #print("===============")
        game.makeMove(move,who)
'''
#'''
name_count=0
for i in glob.iglob(dir_sgf+'*/*'):
    print('Processing:',i)
    game=Game()
    parser.setFile(i)
    if parser.is_legal():
        [a,b,w,c,d,l]=game.runRecap(parser)
    np.savez_compressed(dir_npz+'npz_win'+str(name_count),x=np.array(a),y=np.array(b),z=w)
    np.savez_compressed(dir_npz+'npz_lose'+str(name_count),x=np.array(c),y=np.array(d),z=l)
    #print(np.array(b).shape,len(w))    
    name_count+=1 
#'''
'''for test reason
    if name_count==3:
        break
'''
'''for test reason
if parser.is_legal(): #只关心sgf里明确输赢的
    [a,b,w,c,d,l]=game.runRecap(parser)
    
    #game.runRecap(parser)

    #print(np.array(a),np.array(b))
'''
        
    


