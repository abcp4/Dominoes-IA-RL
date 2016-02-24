import random
import numpy
import scipy


class Features:
    numFeatures = 60
    #valida caracteristicas de acordo com o estado submetido e as retorna
    def featureValues(state):
        result =  np.zeros(numFeatures)
        
        return result

def rand_winner (S_from, beta):
    sum = 0.0
    p_i = 0.0
    rnd = numpy.random.random()
    d_r = len (S_from)
    sel = 0

    for i in range (d_r):
        sum += numpy.exp (beta * S_from[i])

    S_target = numpy.zeros (d_r)

    for i in range (d_r):
        p_i += numpy.exp (beta * S_from[i]) / sum

        if  p_i > rnd:
            sel = i
            rnd = 1.1 # out of reach, so the next will not be turned ON

    return sel




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
        next_action = policyAct (state)                  # choose next action

        

        new_value = numpy.dot (featureWeights, featureVals)     # value after action
        target = r+ 0.9 * new_value                     # gamma = 0.9
        delta = target - val                            # prediction error

        featureWeights += 0.5 * delta * numpy.outer (act_vec, I) #pra cada peso no array de caracteristicas aplica o gradient descent update

        state = next)state
        val = new_value
        act = next_action
        
