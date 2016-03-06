import math
import random
from random import shuffle

class Domino:
    
    def buy(self,hand, n, pieces):
        i = 0
        while i<n:
            hand.append(pieces[i])
            i=i+1
        del pieces[0:n]
        return hand

    #recebe estado do jogo, retorna ações possíveis
    def possibleActions(self,state,player):
        status = state[0]
        if(player =="p1"):
            hand = state[1]
        else:
            hand = state[2]
        l_end = state[4]
        r_end = state[5]
        actions = []
        index = -1

        if(l_end==r_end==-1):
            for piece in hand:
                index +=1
                actions.append((piece[0],piece[1],"left",index))
            return actions

        for piece in hand:
            index +=1
            #peça dupla
            if(piece[0]==piece[1]):
                if(piece[0]==l_end):
                    actions.append((piece[1],"left",index))
                elif(piece[1]==r_end):
                    actions.append((piece[0],"right",index))
                continue
            if(piece[0]==l_end):
                actions.append((piece[1],"left",index))
                if(l_end==r_end): #evitar duplicacao de mesmas ações na esq e dir
                    continue
            if(piece[1]==l_end):
                actions.append((piece[0],"left",index))
                if(l_end==r_end):
                    continue
            if(piece[0]==r_end):
                actions.append((piece[1],"right",index))
                if(l_end==r_end):
                    continue
            if(piece[1]==r_end):
                actions.append((piece[0],"right",index))
                if(l_end==r_end):
                    continue
        '''
        pos 2 e 3 no actions se referem a nova ponta na mesa:
        exemplo: campo 1-5 , mão : (1,2),(5,5)
        nesse caso a peça (1,2) se encaixa no lado esquerdo, sendo
        a nova ponta esquerda o 2. A representação será: (0,1), pois
        0 é a posição da tupla na mão, e o 1 representa a posição na tupla,
        que no caso é o direito

        '''
        return actions

    def termination(self,state):#se a partida ja terminou
        status = state[0]
        p1_hand = state[1]
        p2_hand = state[2]
        l_end = state[4]
        r_end = state[5]
        if (status == 3):
            return True  
        return False

    def reward(self,state,player):#recompensa por estar nesse estado
        #em caso de vitoria
        status = state[0]

        if(status == 1):
            return 0
        if(status == 3):
            p1_hand = state[1]
            p2_hand = state[2]
            lowest_piece = 12
            for piece in p1_hand:
                value = piece[0]+piece[1]
                if(value < lowest_piece):
                    lowest_piece = value
            for piece in p2_hand:
                value = piece[0]+piece[1]
                if(value < lowest_piece):
                    state[0] = 5 #player 2 venceu tendo a menor peça no block
                    if(player == "p1"):
                        return -5 #recompensa negativa ao p1 pois perdeu
                    else:
                        return +5 #recompensa positiva ao p2 pois venceu
            state[0] = 4
            if(player == "p1"):
                return +5 #recompensa negativa ao p1 pois venceu
            else:
                return -5 #recompensa positiva ao p2 pois perdeu

            #evitar recalcular menor peça
        elif(status == 4):
            if(player == "p1"):
                return +5 #recompensa negativa ao p1 pois venceu
            else:
                return -5 #recompensa positiva ao p2 pois perdeu
        elif(status == 5):
            if(player == "p1"):
                return -5 #recompensa negativa ao p1 pois perdeu
            else:
                return +5 #recompensa positiva ao p2 pois venceu

    def startGame(self):
        status = 1 #1=in progress; 2=one player blocked;3=two players blocked;4/5=p1 won/p2 won
        pieces = [(x,y) for x in range(7) for y in range(x,7)]
        random.shuffle(pieces)
        p1_hand = self.buy([],7,pieces)
        p2_hand = self.buy([],7,pieces)
        field = []
        l_end = -1
        r_end = -1
        state = [status, p1_hand, p2_hand, field, l_end, r_end]
        return state

    def playGame(self,state,action,player): 
        status = state[0]
        if(player =="p1"):
            hand = state[1]
        else:
            hand = state[2]
            
        field = state[3]
        l_end = state[4]
        r_end = state[5]

        if(action is None):#foi bloqueado
            if(status == 2):
                state[0] = 3
            elif(status == 1):
                state[0] = 2
            return state

        if(l_end==r_end==-1):
            p_index = action[3]
            orientation = action[2]
        else:
            p_index = action[2]
            orientation = action[1]

        if status==1:
            p = hand[p_index]
            field.append(p)
            hand.remove(p)
            if (l_end==-1 and r_end==-1):
                l_end, r_end = p
            elif (l_end==p[0] and orientation == "right"):#ori e o lado desejado a manter na ponta
                l_end=p[1]
            elif (l_end==p[1] and orientation == "left"):
                l_end=p[0]
            elif (r_end==p[0] and orientation == "right"):
                r_end=p[1]
            elif (r_end==p[1] and orientation == "left"):
                r_end=p[0]
                
        if(player =="p1"):
            state[1] = hand
        else:
            state[2] = hand
        state[3] = field
        state[4] = l_end
        state[5] = r_end
        return state

