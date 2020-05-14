import numpy as np
from goJudge import GoJudge
import threading
import copy
import random
from utilities import *
from goEnv import *
isStopThread=False
import Dboard
import math


class mtctThread(threading.Thread): #蒙特卡罗计算类
    def __init__(self,board,player):
        threading.Thread.__init__(self)
        self.board=board
        self.agent_player=GoAgent(player)
        self.agent_op=GoAgent(player.other())
        self.result = {} #{(0,0):(winNum,numOfRollOuts,advantage)},记录结果
        self.whos = player
        self.visNum = {} #{(0,0):visttimes}
        self.confident = 1.96   #UCB常数
        self.AllvisTime = 0

    def UCT(self,win,vis,Allvis):
        UCTvalue = (win/vis) + self.confident * math.sqrt(math.log(Allvis)/vis)
        return UCTvalue


    def run(self):
        global isStopThread
        while not isStopThread: #新的回合
            
            vacancies=self.board.findVacancy()
            #num=0
            expandFlag  = True
            if expandFlag:
                for j in vacancies:
                    #num+=1
                    self.AllvisTime += 1

                    new_board=copy.deepcopy(self.board) #初始化模拟运行的棋盘
                    whos_turn = self.whos
                    who_win=0

                    if not GoJudge.isLegalMove(new_board,j,self.whos) or not self.agent_player.isPolicyLegal(j,new_board):
                        continue
                    [game_state,player_next]=GoJudge.NextState(whos_turn,j,new_board)
                    new_board.envUpdate(whos_turn,j)
                    if game_state!=GameState.g_over: #模拟下棋不会投降，要么结束要么继续
                        whos_turn=player_next
                    else: #一局结束了,判断输赢
                        who_win=self.agent_player.whoWins(new_board)
                        if who_win==self.whos:
                            win=1
                        else: #平局或者对方赢了
                            win=0
                        record=self.result.get(j)
                        #更新这个位子落点的结果
                        if record == None:
                            self.result[j]=(win,1)
                        else:
                            self.result[j]=(record[0]+win,record[1]+1)
                            continue
                    vacancy=new_board.findVacancy()
                    vacancy_no=len(vacancy)-1
                    #print("AAA",int(vacancy_no*.9))
                    if self.whos == Player.black:
                        param1=3
                    else:
                        param1=4
                    for i in range(min(int(vacancy_no*.9),param1)): #开始下棋，但是不下完,最多模拟3步
                        if whos_turn==Player.black:
                            move=self.agent_player.simulate(new_board)
                        else:
                            move=self.agent_op.simulate(new_board)
                        #print("BBB",who_win)

                        [game_state,player_next]=GoJudge.NextState(whos_turn,move,new_board)
                        #print("XXXXXXXXX",move)
                        new_board.envUpdate(whos_turn,move)


                        if game_state!=GameState.g_over and game_state!=GameState.g_resign:
                            whos_turn=player_next
                        else:
                            [who_win,advantages]=self.agent_player.whoWins(new_board)
                            if who_win==self.whos:
                                win=1
                            else: #平局或者对方赢了
                                win=0
                            record=self.result.get(j)
                            #更新这个位子落点的结果
                            if record== None:
                                self.result[j]=(win,1,advantages)
                            else:
                                self.result[j]=(record[0]+win,record[1]+1,record[2]+advantages)
                                break


                    if who_win==0:
                        #print("DDDDDDDD",j)
                        [who_win,advantages]=self.agent_player.whoWins(new_board)
                        if who_win==self.whos:
                            win=1
                        else:
                            win=0
                        record=self.result.get(j)
                        if record== None:
                            self.result[j]=(win,1,advantages)
                        else:
                            self.result[j]=(record[0]+win,record[1]+1,record[2]+advantages)
        #        print("总模拟次数：", num)    #print("RRRR",j)

            expandFlag = False
            j = (5,5)
            max = 0;
            for child in vacancies:
                # num+=1
                self.AllvisTime += 1
                record = self.result[child]
                if record == None:
                    continue
                UCTvalue = self.UCT(record[0],record[1],self.AllvisTime)
                if max < UCTvalue :
                    j = child

            new_board = copy.deepcopy(self.board)  # 初始化模拟运行的棋盘
            whos_turn = self.whos
            who_win = 0

            if not GoJudge.isLegalMove(new_board, j, self.whos) or not self.agent_player.isPolicyLegal(j,
                                                                                                       new_board):
                continue
            [game_state, player_next] = GoJudge.NextState(whos_turn, j, new_board)
            new_board.envUpdate(whos_turn, j)
            if game_state != GameState.g_over:  # 模拟下棋不会投降，要么结束要么继续
                whos_turn = player_next
            else:  # 一局结束了,判断输赢
                who_win = self.agent_player.whoWins(new_board)
                if who_win == self.whos:
                    win = 1
                else:  # 平局或者对方赢了
                    win = 0
                record = self.result.get(j)
                # 更新这个位子落点的结果
                if record == None:
                    self.result[j] = (win, 1)
                else:
                    self.result[j] = (record[0] + win, record[1] + 1)
                    continue
            vacancy = new_board.findVacancy()
            vacancy_no = len(vacancy) - 1
            # print("AAA",int(vacancy_no*.9))
            if self.whos == Player.black:
                param1 = 3
            else:
                param1 = 4
            for i in range(min(int(vacancy_no * .9), param1)):  # 开始下棋，但是不下完,最多模拟3步
                if whos_turn == Player.black:
                    move = self.agent_player.simulate(new_board)
                else:
                    move = self.agent_op.simulate(new_board)
                # print("BBB",who_win)

                [game_state, player_next] = GoJudge.NextState(whos_turn, move, new_board)
                # print("XXXXXXXXX",move)
                new_board.envUpdate(whos_turn, move)

                if game_state != GameState.g_over and game_state != GameState.g_resign:
                    whos_turn = player_next
                else:
                    [who_win, advantages] = self.agent_player.whoWins(new_board)
                    if who_win == self.whos:
                        win = 1
                    else:  # 平局或者对方赢了
                        win = 0
                    record = self.result.get(j)
                    # 更新这个位子落点的结果
                    if record == None:
                        self.result[j] = (win, 1, advantages)
                    else:
                        self.result[j] = (record[0] + win, record[1] + 1, record[2] + advantages)
                        break

            if who_win == 0:
                # print("DDDDDDDD",j)
                [who_win, advantages] = self.agent_player.whoWins(new_board)
                if who_win == self.whos:
                    win = 1
                else:
                    win = 0
                record = self.result.get(j)
                if record == None:
                    self.result[j] = (win, 1, advantages)
                else:
                    self.result[j] = (record[0] + win, record[1] + 1, record[2] + advantages)
    #        print("总模拟次数：", num)    #print("RRRR",j)


    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return []

def timeDoom():
    global isStopThread
    isStopThread=True


class GoAgent:
    def __init__(self,who):
        self.player=who
        self.KnownList = np.zeros((9,9),dtype='int')

    def PrintInformationSet(self):

        print("当前玩家的信息集:  ",self.player)
        COLS = 'ABCDEFGHJKLMNOPQRST'  # 定义棋盘的列的名称
        STONE_TO_CHAR = {  # 棋盘上的展示的符号
            None: ' . ',
            Player.black: ' x ',
            Player.white: ' o ',
        }
        for row in range(9):
            bump = " " if row > 8 else ""
            line = []
            for col in range(9):
                stone = self.KnownList[8 - row][col]
                if stone == 1:
                    player = Player.black
                    line.append(STONE_TO_CHAR.get(player))
                elif stone == -1:
                    player = Player.white
                    line.append(STONE_TO_CHAR.get(player))
                else:
                    player = None
                    line.append(STONE_TO_CHAR.get(player))
            print('%s%d %s' % (bump, 8 - row, ''.join(line)))
        print('    ' + '  '.join(COLS[:9]))


    def GetPlayerInt(self):
        if self.player == Player.black:
            return 1
        else:
            return -1

    def GetDiff(self):
        sumOfBlack = sum(self.KnownList.flatten() == 1)
        sumOfWhite = sum(self.KnownList.flatten() == -1)
        if self.player == Player.black:
            return int(abs(sumOfBlack - sumOfWhite)) - 1
        else:
            return int(abs(sumOfBlack - sumOfWhite))

    def toMCTBoard(self, NormalBoard): #把board转换成numpy数组，现实中可以理解的样子
        board = GoBoard()
        for i in range(9):
            for j in range(9):
                if NormalBoard[i][j] == 1:
                    board.envUpdate(Player.black,(i,j))
                elif NormalBoard[i][j] == -1:
                    board.envUpdate(Player.white, (i, j))
        return board

    def SampleFromInformationSet(self):
        p = Dboard.GetDistributedBoard()
        states = []
        for i in range(1):
            board = self.toMCTBoard(self.KnownList)
            for j in range(self.GetDiff()):
                flatIdx = np.random.choice(np.array([idx for idx in range(81)]), 1, p=p)
                action_opp = (int(flatIdx / 9), int(flatIdx % 9))
                #row = np.random.randint(0, board.height)
                #col = np.random.randint(0, board.width)
                #int(row)
                #int(col)
                if GoJudge.isLegalMove(board, action_opp, self.player) and self.isPolicyLegal(action_opp, board):
                    board.envUpdate(self.player, action_opp)
            states.append(board)
        return states

    def simulate(self,board):
        vacancy = board.findVacancy()  # 只在空子处挑选落子位
        candidates = random.choices(vacancy, k=10)  # 10个候选落子位
        for i in candidates:
            if GoJudge.isLegalMove(board, i, self.player) and self.isPolicyLegal(i, board):
                return i
        return (-5, -5)


    def chooseMove(self,how):   #选择在棋盘的哪个位子落子
        '''
        if how=='R': #R for random
            episilon=.001 
            if np.random.rand()<=episilon: #千分之一的概率投降
                return (-10,-10)
            for i in range(5): #尝试5次
                row=np.random.randint(0,board.height)
                col=np.random.randint(0,board.width)
                if GoJudge.isLegalMove(board,(row,col),self.player) and self.isPolicyLegal((row,col),board):#判断move是否合法（规则合法+策略合法）
                    return (row,col) #stone
            return (-5,-5) #表示pass这个回合
        '''
        board = self.toMCTBoard(self.KnownList)
        states = self.SampleFromInformationSet()
        mtct_result = {}
        if how=="M": #M for Monte Carlo
            for state in states:
                global isStopThread #每次使用前先初始化
                isStopThread=False
                thread_mtct = mtctThread(state,self.player)
                thread_mtct.setDaemon(True) #父进程结束，子进程就立即结束
                #thread_time= threading.Timer(1,timeDoom)
                thread_time= threading.Timer(1,timeDoom) #每次模拟1秒
                thread_time.start()
                thread_mtct.start()
                thread_time.join()
                thread_mtct.join()
                mtct_result.update(thread_mtct.get_result())
            #print(mtct_result)
            win_rate=[]
            win_advantage=[]
            win_stones=[]
            for i in mtct_result:
                win_stones.append(i)
                win_rate.append(mtct_result[i][0]/mtct_result[i][1])
                win_advantage.append(mtct_result[i][2])
            win_stones=np.array(win_stones)
            win_rate=np.array(win_rate)
            win_advantage=np.array(win_advantage)
            if len(win_advantage) == 0 or len(win_stones) == 0:
                return (-5, -5)
            e=random.random()
            if .5>e:
                moves=win_stones[win_advantage==win_advantage[win_rate==win_rate.max()].max()]
                move=tuple(random.choice(moves.tolist()))
            elif .85>e:
                moves=win_stones[win_rate==win_rate.max()]
                move=tuple(random.choice(moves.tolist()))
            else:
                moves=win_stones[win_advantage==win_advantage.max()]
                move=tuple(random.choice(moves.tolist()))
            if GoJudge.isLegalMove(board,move,self.player) and self.isPolicyLegal(move,board):
                return move
            else:
                return (-5,-5)
            #test----------------------------------------
            '''
            row=np.random.randint(0,board.height)
            col=np.random.randint(0,board.width)
            if GoJudge.isLegalMove(board,(row,col),self.player) and self.isPolicyLegal((row,col),board):#判断move是否合法（规则合法+策略合法）
                return (row,col) 
            else:
                return (-5,-5)
            '''           

    def doMove(self,stone,board): #在棋盘上落子
        if(stone!=(-10,10)): 
            board.envUpdate(self.player,stone) #更新棋盘
            self.KnownList[stone[0],stone[1]] = self.GetPlayerInt()
        else:
            pass            

    def isPolicyLegal(self,move,board): #这里判断根据已知策略是否违法，比如不要堵死自己的眼
        #判断是不是眼位
        neighbours=board.getStoneNeighbours(move)
        is_eye=True
        for i in neighbours:
            if not board.isOnBoard(i):
                continue
            if board.stones.get(i)==None:
                is_eye=False
                break
            elif board.stones.get(i).becolgings != self.player:
                is_eye=False
                break
            elif len(board.stones.get(i).liberties)<=1:
                is_eye=False
                break
            else:
                pass
        if is_eye:
            return False
        return True





    @classmethod
    def staticEvaluation(self,board): #评估当前棋盘的局势,也可用于启发式下棋的参考
        '''
        综合考虑子的数量，气的数量，以及在棋盘的位置与距离
        max_influence和basis都是超参
        '''
        board_array=board.toNormalBoard()
        eval_array=np.zeros(board_array.shape)
        #max_influence=int(min(board.width-1,board.height-1)/3.5) #相隔n子外的棋子影响力<1
        max_influence=2
        #stones_count=board_array.size-board_array[board_array[:]==0].size #计算落子总数
        #max_influence-=int(stones_count/40) #动态调整落子的势力影响范围
        #max_influence=max(max_influence,1)
        basis=2.5 #2.5个子就可以压迫一个对方子
        #黑子用正值势力表示，白子用负值势力表示
        for i in range(eval_array.shape[0]):
            for j in range(eval_array.shape[1]):
                for x in range(board_array.shape[0]):
                    for y in range(board_array.shape[1]):
                        if board_array[x,y]==0:
                            continue
                        #liberties=len(board.stones.get((x,y)).liberties) #考虑子的气的数量                        
                        L=abs(i-x)+abs(j-y)
                        #开始对棋盘分块
                        if (x<=3 or x>=8-3) and (y<=3 or y>=8-3): #4个角
                            if x<=3 and y<=3: # 左下角
                                if i<=x and j<=y: #在子的左下角
                                    max_influence=(x+y)/2+1
                                    basis=3.5
                            elif x<=3 and y>=8-3: # 右下角
                                if i<=x and j>=y: #在子的右下角
                                    max_influence=(x+8-y)/2+1
                                    basis=3.5
                            elif x>=8-3 and y>=8-3: # 右上角
                                if i>=x and j>=y: #在子的右上角
                                    max_influence=(8-x+8-y)/2+1
                                    basis=3.5
                            elif x>=8-3 and y<=3: # 左上角
                                if i>=x and j>=y: #在子的左上角
                                    max_influence=(8-x+y)/2+1
                                    basis=3.5
                            else:
                                pass

                        elif (x<=3 or x>=8-3) or (y<=3 or y>=8-3): #4个边
                            if x<=3: #down
                                if i<=x:
                                    max_influence=x
                                    basis=3
                            elif y>=8-3: #right
                                if j>=y:
                                    max_influence=8-y
                                    basis=3
                            elif x>=8-3: #up
                                if i>=x:
                                    max_influence=8-x
                                    basis=3
                            elif y<=3: #left
                                if j<=y:
                                    max_influence=y
                                    basis=3
                            else:
                                pass
                        else: #中心位置
                            pass #使用默认值
                        #influence=liberties*basis**(max_influence-L)*board_array[x,y]
                        influence=basis**(max_influence-L)*board_array[x,y]
                        eval_array[i,j]+=influence
        return eval_array






    def whoWins(self,board): #判断棋面输赢
        komi=4.5 #贴目采用中国规则
        count_b=0
        count_w=0
        '''
        for i in board.stones:
            if board.stones[i].becolgings==Player.black:
                count_b+=1
            else:
                count_w+=1
        #为了简单，目前仅计算棋盘上的子数
        if count_b>count_w+komi:
            return Player.black
        elif count_b<count_w+komi:
            return Player.white 
        else:#返回谁赢谁输，平局返回None,但是贴了半目，一般不会平局
            return None
        '''
        board_array=self.staticEvaluation(board)
        #count_b=board_array[board_array[:]>=1].size
        count_b=np.sum(board_array[board_array[:]>=1])
        #count_w=board_array[board_array[:]<=-1].size
        count_w=abs(np.sum(board_array[board_array[:]<=-1]))
        if count_b>count_w+komi:
            return Player.black,count_b-count_w
        elif count_b<count_w+komi:
            return Player.white,count_w-count_b
        else: #返回谁赢谁输，平局返回None,但是贴了半目，一般不会平局
            return None,0
                       
