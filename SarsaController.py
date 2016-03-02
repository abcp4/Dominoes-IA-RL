import random
import numpy
import scipy


e = 0.01 # epsilon-greedy proportion

num_features = 60
featureWeights = np.zeros(numFeatures)

beta = 50.0
features = Features()


class Features:
    numFeatures = 60
    
    def featureValues(state,action):
        """"
        Características a partir de informações imperfeitas.
            Somente do que é visível a um jogador comum:
                Campo, peças de suas mãos, quantidade de peças do oponente
        """"
        #valida caracteristicas de acordo com o estado submetido e as retorna
        result =  np.zeros(numFeatures)
        
        result[0] = hasOneDouble(state)
        result[1] = blocksMe(state,action)#impossibilita qualquer peça de ser jogada
        result[2] = enableNumActions(state,action,1)
        result[3] = enableNumActions(state,action,2)
        result[4] = enableNumAndMoreActions(state,action,3)#possibilita 3 ou mais peças de serem jogáveis
        for i in range(7):
            #quais peças duplas temos na mão, de 0:0 a 6:6
            result[i] = hasDouble(i)
        
        
        """"
        Características a partir de informações perfeitas.
        Sabe-se da mão do oponente, de toda e qualquer informação necessária
        para se tomar uma decisão
        """"
        
        
        
        return result

def qValue(state,act):
    featureVals = features.featuresValue(state,act)
    val = numpy.dot (featureWeights, featureVals)    # value before action
    return val
        
def eGreedyPicker(actions,state):
    rand = np.random.random_sample()
    bestValue = 0
    if(rand > e):
        for act in actions:
            value = qValue(state,act)
            if(value> bestValue):
                bestValue = value
        choosenAct = bestValue
    else:
        choosenAct = random.choice(actions)
        
    return choosenAct

def policyAct(state):
    """
    Constroi acões possiveis a partir do estado
    Ações são vistas como o que o agente pode 'querer'
    Ex: Pontas: 5 - 5
    Mão: (0,5),(1,2),(5,5),(3,5),(0,2)
    Ações possíveis(que o agente pode querer):
       (0,esq),(5,esq),(3,esq)
    ele pode querer ter um 0 na esquerda, ou um 5 na esquerda, ou um 3 na esquerda
    veja que ele poderia querer ter um 5 do (5,5) na dir, ou o 3 do (3,5) na dir,
    mas isso não influenciaria em nada, então a esquerda é sempre eleita automaticamente.
    Ex2: Pontas 5-0
    Mão:(0,5),(1,2),(5,5),(3,5),(0,2)
    Ações possíveis(que o agente pode querer):
         (0,esq),(5,dir),(3,esq),(2,dir)
    veja que na peça (0,5) teremos 2 ações possiveis, uma para cada ponta, pois dependendo da escolha,
    isso vai influenciar na partida.

    A escolha das ações originalmente era as peças jogáveis em si, (0,5),(5,5),(3,5), mas isso acarretava
    problemas de decisões e duplicações em alguns casos, além de ser 28 ações diferente, sendo que pra
    cada estado possiveis teria que armazenar uma dessas ações.
    Com esse modelo o número de ações possiveis são no máximo 14, sendo que acredito que talvez possa
    ser diminuido. Verificar situações 'espelhos' onde dependendo do arranjo das peças, jogar na esq
    para um arranjo e na dir para outro, deveriam equivaler ao mesmo valor na q-function, mas não o tem.

    """
    SetActions = dominoes.possibleActions(state)
    actions = SetActions[0]
    #escolhe a partir dos valores na q-value com tecnica e-greedy
    choosenAct = eGreedyPicker(actions,state)
    
    return choosenAct


for iter in range (10000):
    
    state = dominoes.startGame() 
    act = policyAct (state)                         # take action by a e-greedy policy
    val = qValue(state,act)
    r = 0
    duration = 0
    while dominoes.termination() == 0:

        dominoes.act(act)                                  # do selected action
        r = dominoes.reward()                              # read reward

        next_state = dominoes.state()                   # read new state
        next_action = policyAct(state)                  # choose next action

        

        new_value = numpy.dot (featureWeights, featureVals)     # value after action
        target = r+ 0.9 * new_value                     # gamma = 0.9
        delta = target - val                            # prediction error

        featureWeights += 0.5 * delta * numpy.outer (act_vec, I) #pra cada peso no array de caracteristicas aplica o gradient descent update

        state = next_state
        val = new_value
        act = next_action
        
