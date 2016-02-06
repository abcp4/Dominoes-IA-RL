import math
import random
from random import shuffle


def take_initial_pieces(hand,pieces):
    n = 0
    while(n<7):
        hand.append(pieces[n])
        #print pieces[n]
        n= n+1
    del pieces[0:7]
    return hand
    
    
def play(state,action):
    
    #play
    #action[0] = se é uma jogada, action[1] = peça em si,
    #action[2]= pos da peça na mão
    if(action[0]==1):
        field_pieces = state.pop(2)
        hand = state.pop(0)
        piece = action[1]
        orientation = piece[1]#se é a esq(0) ou dir(1) da peça q importa
        value = piece[0]
        piece_value = value[orientation]
        
        if(len(field_pieces)>0):
            #pega a 1 peça e sua orientação
            first = field_pieces[0]
            first_or = first[1]
            #pega a ultima peça e sua orientação
            last = field_pieces[-1]
            last_or = last[1]
            if(first_or == 2):#existe so 1 peça, os 2 lados importam
                first_or = 0
            if(last_or == 2):
                last_or = 1
            if(piece_value==first[first_or] ):
                hand.remove(piece)
                if(orientation==0):
                    piece[1] = 1
                else:
                    piece[1] = 0
                field_pieces.insert(0,piece)
                
            elif(piece_value == last[last_or]):   
                hand.remove(piece)
                if(orientation==0):
                    piece[1] = 1
                else:
                    piece[1] = 0
                field_pieces.append(piece)
                
        else:
            hand.remove(piece)
            piece[1] = 2 # pra esperar ter dir e esq
            field_pieces.insert(0,piece)
            
    state.insert(1,field_pieces)    
    state.insert(0,hand)  
    return state
        
    #pass

#Start a game of dominoes, shuffling pieces and giving 7 to each player
def initGame():
    status = 1 #1=in progress; 2=player won; 3=draw; 4 = dealer won/player loses
    #peca tem seu valor como tupla, e orientacao,
    #por exem: [(1,0),0] = (1,0) e  [(1,0),1] = (0,1)
    pieces = [[(0,0),0],[(0,1),0],[(0,2),0],[(0,3),0],[(0,4),0],[(0,5),0],[(0,6),0],[(1,1),0],[(1,2),0],[(1,3),0],[(1,4),0],[(1,5),0],[(1,6),0],[(2,2),0],[(2,3),0],[(2,4),0],[(2,5),0],[(2,6),0],[(3,3),0],[(3,4),0],[(3,5),0],[(3,6),0],[(4,4),0],[(4,5),0],[(4,6),0],[(5,5),0],[(5,6),0],[(6,6),0]]
    random.shuffle(pieces)
    player_hand = []
    dealer_hand = []
    player_hand = take_initial_pieces(player_hand,pieces)
    dealer_hand = take_initial_pieces(dealer_hand,pieces)
    field_pieces = []
    #retorna estado do jogo total
    state = [player_hand,dealer_hand,field_pieces,pieces,status]
    return state
