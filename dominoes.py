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
                actions.append((piece[0],piece[1],index))
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
        if not actions:
            actions.append(None)
        return actions

    def termination(self,state):#se a partida ja terminou
        status = state[0]
        p1_hand = state[1]
        p2_hand = state[2]
        l_end = state[4]
        r_end = state[5]
        if (status >= 3):
            return True  
        return False

    def reward(self,state,player):#recompensa por estar nesse estado
        #em caso de vitoria
        status = state[0]

        if(status == 1 or status == 2):
            return 0
        if(status == 3):
            p1_hand = state[1]
            p2_hand = state[2]
            lighestP1Value = 13
            lighestP2Value = 13
            lighestP1Tile = 13
            lighestP2Tile = 13
            p1_total_value = 0
            p2_total_value = 0
            for piece in p1_hand:
                value = piece[0]+piece[1]
                p1_total_value+=value
            for piece in p2_hand:
                value = piece[0]+piece[1]
                p2_total_value+=value
            if(p1_total_value<p2_total_value):
                state[0] = 4#player 1 venceu tendo a menor mao
                return 5
            elif(p1_total_value>p2_total_value):
                state[0] = 5#player 2 venceu tendo a menor mao
                return -5
            else:#empate
                for piece in p1_hand:
                    if(piece[0]<lighestP1Value):
                        lighestP1Value = piece[0]
                        lighestP1Tile = piece[0]+piece[1]
                    if(piece[1]<lighestP1Value):
                        lighestP1Value = piece[1]
                        lighestP1Tile = piece[0]+piece[1]
                        
                for piece in p2_hand:
                    if(piece[0]<lighestP2Value):
                        lighestP2Value = piece[0]
                        lighestP2Tile = piece[0]+piece[1]
                    if(piece[1]<lighestP2Value):
                        lighestP2Value = piece[1]
                        lighestP2Tile = piece[0]+piece[1]
                        
                if(lighestP1Value<lighestP2Value):
                    state[0] = 4#player 1 venceu tendo o menor valor entre o par das pecas
                    return 5
                elif(lighestP1Value>lighestP2Value):
                    state[0] = 5#player 2 venceu tendo o menor valor entre o par das pecas
                    return -5
                else:
                    if(lighestP1Tile<lighestP2Tile):#menor valor da peça como um todo
                        state[0] = 4
                        return 5
                    else:#nao pode haver empate
                        state[0] = 5
                        return -5

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
        if(status >= 3): #jogo acabou
            return state
        if(player =="p1"):
            hand = state[1]
        else:
            hand = state[2]
            
        field = state[3]
        l_end = state[4]
        r_end = state[5]

        if(action[0] is None):#foi bloqueado
            if(status == 2):
                state[0] = 3
            elif(status == 1):
                state[0] = 2
            return state
        
        if(status == 2): # o oponente foi bloqueado, mas eu tenho peça
            state[0] = 1
        p_index = action[2]  
        if(l_end==r_end==-1):
            orientation = "left"
        else:
            orientation = action[1]
        p = hand[p_index]
        field.append(p)
        hand.remove(p)
        if (l_end==-1 and r_end==-1):
            l_end, r_end = p
        elif (orientation == "right"):#ori e o lado desejado a manter na ponta
            r_end=action[0]
        elif (orientation == "left"):
            l_end=action[0]
                
        if(player =="p1"):
            state[1] = hand
        else:
            state[2] = hand
            
        if(len(hand) ==0): #zerou a mao, acabou o jogo
            state[0] = 3
        state[3] = field
        state[4] = l_end
        state[5] = r_end
        return state

