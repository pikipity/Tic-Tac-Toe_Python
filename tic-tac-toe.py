# -*- coding: utf-8 -*-
from copy import deepcopy as dcp

# 1 2 3
# 4 5 6
# 7 8 9

all_pieces=range(1,10)
actual_turn=1

#class player:
#    def __init__(self,turn):
#        self.pieces=[0]*3
#        self.turn=turn
#    def move(self,next_piece):
#        self.pieces=[next_piece, self.pieces[0], self.pieces[1]]
        
def evaluation(first_player_pieces,second_player_pieces,turn):
    # evaluate first player -> turn=1
    # evaluate second player -> turn=-1
    score=[0,0]
    evalue_list=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
    for i in evalue_list:
        if len(set(first_player_pieces)&set(i))==3:
            score[0]+=10
        elif len(set(first_player_pieces)&set(i))==2:
            if len((set(i)-set(first_player_pieces)&set(i))&set(second_player_pieces))==0:
                score[0]+=5
            else:
                score[1]+=5
        elif len(set(first_player_pieces)&set(i))==1:
            if len((set(i)-set(first_player_pieces)&set(i))&set(second_player_pieces))==0:
                score[0]+=1
            else:
                score[0]+=1
            
        if len(set(second_player_pieces)&set(i))==3:
            score[1]+=10
        elif len(set(second_player_pieces)&set(i))==2:
            if len((set(i)-set(second_player_pieces)&set(i))&set(first_player_pieces))==0:
                score[1]+=5
            else:
                score[0]+=5
        elif len(set(second_player_pieces)&set(i))==1:
            if len((set(i)-set(second_player_pieces)&set(i))&set(first_player_pieces))==0:
                score[1]+=1 
            else:
                score[0]+=1
    return (score[0]-score[1])*turn
        
def game_move(first_player_pieces,second_player_pieces,turn, next_piece):
    if turn == 1:
        first_player_pieces=[next_piece,first_player_pieces[0],first_player_pieces[1]]
    else:
        second_player_pieces=[next_piece,second_player_pieces[0],second_player_pieces[1]]
    turn*=-1
    return first_player_pieces,second_player_pieces, turn
        
def negamaxsearch(cfirst_player_pieces,csecond_player_pieces,cturn, depth, possibal_piece=0):
    global all_pieces
    first_player_pieces=dcp(cfirst_player_pieces)
    second_player_pieces=dcp(csecond_player_pieces)
    turn=dcp(cturn)
    if depth<=0:
        return evaluation(first_player_pieces,second_player_pieces,turn), possibal_piece
    else:
        best=-50
        best_move=0
        all_possible_pieces=set(all_pieces)-(set(first_player_pieces)|set(second_player_pieces))
        for possible_piece in all_possible_pieces:
            v_first_player_pieces,v_second_player_pieces, v_turn=game_move(first_player_pieces,second_player_pieces,turn, possible_piece)
            value, best_piece=negamaxsearch(v_first_player_pieces,v_second_player_pieces,v_turn, depth-1, possible_piece)
            value*=-1
            if value>best:
                best=value
                best_move=possible_piece
        return best, best_move
        
def display(first_player_pieces, second_player_pieces):
    second_player_list=['a','b','c']
    displayment='''\n'''
    for i in [[1,2,3],[4,5,6],[7,8,9]]:
        displayment+=''' | '''
        for k in i:
            if k in first_player_pieces:
                first_player_pieces_set=set(first_player_pieces)
                try:
                    first_player_pieces_set.remove(0)
                except:
                    pass
                displayment+='''%s | '''%(len(first_player_pieces_set)-first_player_pieces.index(k))
            elif k in second_player_pieces:
                second_player_pieces_set=set(second_player_pieces)
                try:
                    second_player_pieces_set.remove(0)
                except:
                    pass
                displayment+='''%s | '''%(second_player_list[len(second_player_pieces_set)-second_player_pieces.index(k)-1])
            else:
                displayment+='''_ | '''
        displayment+='''\n'''
    return displayment
    
def judgment(first_player_pieces, second_player_pieces):
    result=0
    evalue_list=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
    for i in evalue_list:
        if len(set(first_player_pieces)&set(i))==3:
            result=1
            break
        if len(set(second_player_pieces)&set(i))==3:
            result=2
            break
    return result

first_player_pieces=[0,0,0]
second_player_pieces=[0,0,0]
preview_step_num=3
print display(first_player_pieces,second_player_pieces)
while 1:    
    if actual_turn==1:
        user_step=input('''| 1 | 2 | 3 |\n| 4 | 5 | 6 |  Input your step:\n| 7 | 8 | 9 |\n --> ''')
        if user_step=='q':
            print "exit"
            break
        elif int(user_step) in list(set(first_player_pieces)|set(second_player_pieces)):
            print "wrong piece"
            break
        elif int(user_step) not in [1,2,3,4,5,6,7,8,9]:
            print "Not correct input"
            break
        first_player_pieces,second_player_pieces, actual_turn=game_move(first_player_pieces,second_player_pieces,actual_turn, user_step)
    else:
        best_score, best_movement=negamaxsearch(first_player_pieces,second_player_pieces,actual_turn, preview_step_num)
        first_player_pieces,second_player_pieces, actual_turn=game_move(first_player_pieces,second_player_pieces,actual_turn, best_movement)
    print display(first_player_pieces,second_player_pieces)
    result=judgment(first_player_pieces,second_player_pieces)
    if result==1:
        print "user win!!"
        break
    elif result==2:
        print "computer win!!"
        break