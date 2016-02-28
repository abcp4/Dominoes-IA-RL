import random
import numpy
import scipy


class Features:
    numFeatures = 60
    #valida caracteristicas de acordo com o estado submetido e as retorna
    def featureValues(state):
        result =  np.zeros(numFeatures)
        
        return result

def policyAct(state,features):
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
    
    #escolhe a partir dos valores na q-value com de e-greedy
    
    return action

num_features = 60
featureWeights = np.zeros(numFeatures)

beta = 50.0
features = Features()

for iter in range (10000):
    
    state = dominoes.startGame() 
    act = policyAct (state)                         # take action by a e-greedy policy
    featureVals = features.featuresValue(state)
    val = numpy.dot (featureWeights, featureVals)                     # value before action
    r = 0
    duration = 0
    while dominoes.termination() == 0:

        dominoes.act(act)                                  # do selected action
        r = dominoes.reward()                              # read reward

        next_state = dominoes.state()                   # read new state
        next_action = policyAct (state,features)                  # choose next action

        

        new_value = numpy.dot (featureWeights, featureVals)     # value after action
        target = r+ 0.9 * new_value                     # gamma = 0.9
        delta = target - val                            # prediction error

        featureWeights += 0.5 * delta * numpy.outer (act_vec, I) #pra cada peso no array de caracteristicas aplica o gradient descent update

        state = next)state
        val = new_value
        act = next_action
        
