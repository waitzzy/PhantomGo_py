#解析SGF文件
from sgfmill import sgf #处理SGF version 4 FF[4],python2的话可以用gomill库
import h5py

class sgfPaserSingle: #解析单个sgf文件
    def __init__(self,game=None):
        self.game=game
        self.main_seq=None
        self.size=0
        self.root_node=None
        self.moves=None
        self.handicap=None
        self.winner=None
    def is_legal(self): #判断sgf文件是否是19*19，以及满足一些其他要求
        if self.size!=19:
            return False
        if self.getWinner()!='w' and self.getWinner()!='b': #由于不同棋谱登记的信息不一样，这里为了方便只处理标准的，其实也可以下完棋后由自己来判断，不使用sgf文件里的这个信息
            return False
        return True
    def setFile(self,file_name):
        with open(file_name,"rb") as f:
            self.game=sgf.Sgf_game.from_bytes(f.read())
            self.size=self.game.get_size()
            self.main_seq=self.game.get_main_sequence()
            self.root_node=self.game.get_root()
            self.moves=self.extractMoves()
            self.handicap=self.extractHandi()
            self.winner=self.getWinner()
    def getWinner(self):
        return self.game.get_winner()
    def extractMoves(self):
        moves=[]
        for i in self.main_seq:
            move=i.get_move()
            moves.append(move)
        return moves
    def get_property(self,property):
        if self.root_node.has_property(property):
            return self.root_node.get(property)
        else:
            return None
    def extractHandi(self):
        if not self.game.get_handicap():
            return None,None
        b_moves=self.get_property("AB")
        w_moves=self.get_property("AW")
        return b_moves,w_moves

    
    

