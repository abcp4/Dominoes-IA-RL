import random
import numpy
import scipy


class Features:
    numFeatures = 60
    #valida caracteristicas de acordo com o estado submetido e as retorna
    def featureValues(state):
        result =  np.zeros(numFeatures)
        print state

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




size_a, size_b = 16, 16
size_map = size_a * size_b
size_mot = 4
featureWeights = numpy.random.uniform (0.0, 0.0, (size_mot, size_map))

beta = 50.0
features = Features()

for iter in range (10000):
    
    state = dominoes.startGame() 
    act = policyAct (state)                         # take action by a e-greedy policy
    featureVals = features.featuresValue(state)
    val = numpy.dot (featureWeights, featureVals)                     # value before action
    r = 0
    duration = 0
    termination = 0
    while termination == 0:

        duration += 1
        world.act(act)                                  # do selected action
        r = world.reward()                              # read reward
        I_tic = world.sensor()                          # read new state

        
        act_tic = rand_winner (h, beta)                 # choose next action

        act_vec = numpy.zeros (size_mot)
        act_vec[act] = 1.0

        val_tic = numpy.dot (w_mot[act_tic], I_tic)     # value after action
        target = r+ 0.9 * val_tic                     # gamma = 0.9
        delta = target - val                            # prediction error

        w_mot += 0.5 * delta * numpy.outer (act_vec, I) #pra cada peso no array de caracteristicas aplica o gradient descent update

        val = val_tic
        act = act_tic
        
