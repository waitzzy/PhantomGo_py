#这个类是规则的抽象，规则不需要一个实体，所以使用classmethod就行了
from utilities import *
import numpy as np



class GoJudge(): #裁判类
    @classmethod
    def isLegalMove(cls,board,stone,player): #这里判断围棋规则是否违法,不同的地方规则会有差别，这里使用中国规则
        if stone==(-10,-10) or stone==(-5,-5):
            return True
        #不能下到棋盘外面去
        if not board.isOnBoard(stone):
            return False
        #不允许往已经有子的地方下棋
        if not board.stones.get(stone)==None:
            return False
        #任一一方不允许重复己方已经下过的棋形，不允许自杀
        [noLiberties,zobrist]=board.evaluate(player,stone)
        if noLiberties==0 or (player,zobrist) in board.board_records:
            return False
        return True
    @classmethod    
    def NextState(cls,player_current,move,board): #判断下一手是谁，或者是否已经结束
        #围棋是不会下满棋盘的，所以结束只会是有人投降或者双方都pass
        #先判断棋局是否结束
        if move==(-10,-10):  #投降，返回胜利者          
            return GameState.g_resign,player_current.other()
        elif move==(-5,-5):
            if board.move_records[-1][1]==(-5,-5):
                return GameState.g_over,None #双方都放弃落子，这个时候还不知道谁赢谁输，所以要算一下       
            else:
                return GameState.g_continue,player_current.other()
        else:
            return GameState.g_continue,player_current.other()


    def has_opponent(self,board,stone,player):
        if board.stones.get(stone) == player.other():
            return True;

    @classmethod
    def getGameResult(cls,board):        
        komi=0 #贴目采用中国规则
        blacks=[]
        whites=[]
        black_territory=set()
        white_territory=set()
        neutral_territory=set()
        visited_stones=None
        #results={} #存放空子的地域属于哪个势力，有三种：黑、白、中立
        def findBoarders(board,stone,visited_stones=None):
            boarders=set()
            neighbours=board.getStoneNeighbours(stone)
            for i in neighbours:
                if not board.isOnBoard(i) or i in visited_stones:
                    continue
                if board.stones.get(i)==None:
                    visited_stones.add(i)
                    boarders|=findBoarders(board,i,visited_stones)
                elif board.stones.get(i).becolgings==Player.black:
                    boarders.add(Player.black)
                elif board.stones.get(i).becolgings==Player.white:
                    boarders.add(Player.white)
                else:
                    pass
            return boarders

        #组个点来看
        for i in range(board.height):
            for j in range(board.width):
                if board.stones.get((i,j))==None:
                    if (i,j) in black_territory or (i,j) in white_territory or (i,j) in neutral_territory:
                        continue
                    else:
                        visited_stones={(i,j)}
                        boarders=findBoarders(board,(i,j),visited_stones)
                        if len(boarders) !=1:
                            neutral_territory|=visited_stones
                        else:
                            if Player.black in boarders:
                                black_territory|=visited_stones
                            else:
                                white_territory|=visited_stones
                elif board.stones.get((i,j)).becolgings==Player.black:
                    blacks.append((i,j))
                elif board.stones.get((i,j)).becolgings==Player.white:
                    whites.append((i,j))
                else:
                    pass
        black_counts=len(blacks)+len(black_territory)
        white_counts=len(whites)+len(white_territory)
        return black_counts-(white_counts+komi)
        #return blacks,whites,black_territory,white_territory,neutral_territory
        