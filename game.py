from goAgent import GoAgent
from goEnv import *
from goJudge import *

class Game: #game类既可以单步走，也可以用作复现sgf棋谱
    def __init__(self):
        self.board=GoBoard()
        self.agent=None

    def setAgent(self,agent): #如果需要自动下棋的话，要设置AI
        self.agent=agent
    
    def makeMove(self,move,who):
        self.board.envUpdate(who,move)
    
    def getFrame(self):
        return self.board.toNormalBoard()
    def reset(self):
        self.board=GoBoard()
        self.agent=None
    def setHandicaps(self,b_moves,w_moves): #初始化让子
        if b_moves is not None:
            for i in b_moves:
                self.board.envUpdate(Player.black,i)
        if w_moves is not None:
            for i in w_moves:
                self.board.envUpdate(Player.white,i)
    def runRecap(self,sgf): #只处理sgf里明确输赢的，在调用前判断，这里不再增加判断
        self.setHandicaps(sgf.handicap[0],sgf.handicap[1])
        board_sits_win=[]#记录胜利方棋盘的每一次变化
        board_moves_win=[] #记录棋盘当前形势的下一步
        board_sits_lose=[]#记录失败方棋盘的每一次变化
        board_moves_lose=[]
        for i in sgf.moves:
            if not None in i: #避免pass
                who=i[0]
                if who=='b':
                    player_=Player.black
                elif who=='w':
                    player_=Player.white
                else:
                    pass
                move=i[1]
                if i[0]==sgf.winner:
                    board_sits_win.append(self.getFrame())
                    board_moves_win.append(move)
                else:
                    board_sits_lose.append(self.getFrame())
                    board_moves_lose.append(move)       
                self.makeMove(move,player_)
        if 'b'==sgf.winner :
            winner=np.ones(len(board_moves_win)) #1 for black,-1 for white
            loser=-1*np.ones(len(board_moves_lose))
        elif  'w'==sgf.winner :
            winner=-1*np.ones(len(board_moves_win))
            loser=np.ones(len(board_moves_lose))
        else:
            pass
        #self.reset()
        return board_sits_win,board_moves_win,winner,board_sits_lose,board_moves_lose,loser    
        
