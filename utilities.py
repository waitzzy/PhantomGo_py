#基于python引用的特性，将一些公共的类放这里
from enum import Enum



class GameState(Enum): 
    g_over=-1
    g_continue=1
    g_resign=0


class Player(Enum): 
    black=1
    white=-1

    def other(self):
        return Player.white if self==Player.black else Player.black

class StoneString: #将相连的子看作一起，单个的stone也是StoneString
    def __init__(self,player,stones,liberties):
         self.becolgings=player #这串子属于谁
         self.stones=set(stones) #stones=[(0,0),(0,1)]
         self.liberties=set(liberties) #liberties=[(0,0),(1,2)]
    @classmethod
    def merge(cls,str1,str2):
        assert str1.becolgings == str2.becolgings # 必须是同一方的子才能合并，由于代码的逻辑会控制，这里就assert一下，以防万一
        allstones=str1.stones|str2.stones #使用set类的好处
        liberties=(str1.liberties | str2.liberties)-allstones #两组子合并后，新的子占用原来的气的位置
        return StoneString(
            str1.becolgings,
            allstones,
            liberties
        )

class VacancyString:
    def __init__(self,boarders,stones):
        self.boarders={} #边界要么属于白，要么属于黑，就两种
        self.stones=set(stones)
    