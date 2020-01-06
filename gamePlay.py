from goAgent import GoAgent
from goEnv import *
from goJudge import *
import os
import time


#board=GoBoard()
#agent=GoAgent(Player.black)
#move=agent.chooseMove('R',board)
#agent.doMove(move,board)
#board.printBoard()
COLS = 'ABCDEFGHJKLMNOPQRST'
def to_stone(string):
    if string!= "resign"  and string!="pass":
        c=COLS.index(string[0])
        r=int(string[1:])
        return (r,c)
    elif string=="resign":
        return (-10,-10)
    else:
        return (-5,-5)


def main():
    board=GoBoard()
    boardBlack = GoBoard()
    boardWhite = GoBoard()
    agent_b=GoAgent(Player.black)
    agent_w=GoAgent(Player.white)
    #os.system('cls')
    board.printBoard()
    whosTurn=Player.black
    player_next=whosTurn
    game_state=GameState.g_continue
    count=0
    while game_state==GameState.g_continue:
        count+=1
        time.sleep(.3)        
        if whosTurn==Player.black:
            '''人工输入
            move=input('-- ') #A1
            move=to_stone(move.strip())
            '''
            move=agent_b.chooseMove('M',boardBlack)
        else:
            move=agent_w.chooseMove('M',boardWhite)
            '''
            move=input('-- ') #A1
            move=to_stone(move.strip())
            '''
        '''
        
        if not GoJudge.isLegalMove(board,move,whosTurn):
            continue
        '''

        if GoJudge.has_opponent(board,move,whosTurn):
            if whosTurn == Player.black:
                boardBlack.envUpdate(Player.white,move)
            elif whosTurn == Player.white:
                boardWhite.envUpdate(Player.black,move)
            continue

        [game_state,player_next]=GoJudge.NextState(whosTurn,move,board)
        board.envUpdate(whosTurn,move)
        if whosTurn == Player.black:
            boardBlack.envUpdate(Player.black, move)
        elif whosTurn == Player.white:
            boardWhite.envUpdate(Player.white, move)

        if game_state!=GameState.g_over and game_state!=GameState.g_resign:
            #os.system('cls')
            board.printBoard()
            #print(board.toNormalBoard())
            whosTurn=player_next
            print(whosTurn)
        #print(board.findVacancy())
        '''
        if count%15==0:
            [a,b,c,d,e]=GoJudge.getGameResult(board)
            #print(a,b,c,d,e)
            #print(GoJudge.staticEvaluation(board))
        '''
    if game_state==GameState.g_resign:
        print(player_next,"wins!")
    if game_state==GameState.g_over:
        #print("Need to count!")
        result=GoJudge.getGameResult(board)
        '''
        [a,b,c,d,e]=GoJudge.getGameResult(board)
        print(a,b,c,d,e)
        '''
        #print(result)
        #'''
        if result>0:
            print("black wins")
        elif result<0:
            print("white wins")
        else: #贴7.5目，所以不会平局
            print("ties")
        #'''

if __name__ == '__main__':
    main()