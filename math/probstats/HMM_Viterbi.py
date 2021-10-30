import numpy as np
from numpy.core.fromnumeric import argmax

def HMM_Viterbi(seqA, seqB, seqR):
    """If seqA implies seqB, find the most likely sequence
    from factors in seqA that result in sequence seqR composed
    from factors of seqB"""
    factA = sorted(list(set(seqA)))
    factB = sorted(list(set(seqB)))
    factAMap = dict((factA[i], i) for i in range(len(factA)))
    factBMap = dict((factB[i], i) for i in range(len(factB)))
    tranAMat = np.zeros((len(factA), len(factA)))
    tranBMat = np.zeros((len(factA), len(factB)))

    counts = countAppearances(factAMap, seqA)

    # compute transition matrix
    for i in range(len(seqA)-1):
        tranAMat[factAMap[seqA[i]]][factAMap[seqA[i+1]]] += 1
    for i in range(len(seqB)):
        tranBMat[factAMap[seqA[i]]][factBMap[seqB[i]]] += 1
    tranAMat /= counts[:,None]
    tranBMat /= counts[:,None]
    return viterbi(factB, factA, counts/counts.sum(), seqR, tranAMat, tranBMat)


    
def countAppearances(factMap, seq):
    count = np.zeros(len(factMap.keys()))
    for s in seq:
        count[factMap[s]] += 1
    return count

def viterbi(O, S, Pi, Y, A, B):
    """
    O - observation space [ o1, o2, ..., oN ]
    S - state space [ s1, s2, ..., sK ]
    Pi - array of initial probabilities [ pi1, pi2, ..., piK ]
    Y - sequence of observations [ y1, y2, ..., yT ]
    A - transition matrix of states of size K x K
    B - emission matrix of states to observations of size K x N
    """
    k = len(S)
    t = len(Y)
    A = np.array(A)
    B = np.array(B)
    T1 = np.zeros((k, t))
    T2 = np.zeros((k, t))
    T1[:,0] = B[:,O.index(Y[0])] * Pi
    for j in range(1, t):
        for i in range(k):
            o = O.index(Y[j])
            c = T1[:,j-1] * A[:,i] * B[i, o]
            T1[i, j] = np.max(c)
            T2[i, j] = argmax(c)

    # print("T1")
    # printMatrix(T1)
    # print("T2")
    # printMatrix(T2)

    z = argmax(T1[:,-1])
    print(T1[:,-1])
    print("Z", z)
    x = [ S[z] ]
    for j in range(t-1, 0, -1):
        z = int(T2[z, j])
        x = [ S[z] ] + x
    return x, max(T1[:, -1])

def printMatrix(M):
    for i in range(M.shape[0]):
        print(" ".join([ "%.3f" %v for v in M[i] ]))


if __name__ == "__main__":
    # seqA = list("cabbaaabbbddaa")
    # seqB = list("22121100001221")
    # seqR = list("12101")

    # x, p = HMM_Viterbi(seqA, seqB, seqR)    
    

    # obs = ["normal", "cold", "dizzy"]
    # states = ["Healthy", "Fever"]
    # Pi = [ 0.6, 0.4 ]
    # A = [ 
    #     [ 0.7, 0.3 ],
    #     [ 0.4, 0.6 ]
    # ]
    # B = [
    #     [ 0.6, 0.4, 0.1 ],
    #     [ 0.1, 0.3, 0.6 ]
    # ]
    # Y = [ "normal", "cold", "dizzy" ]

    obs = [ "Bob", "ate", "the", "fruit" ]
    states = [ "n", "v", "d" ]
    A = [
        [ .1, .8, .1 ],
        [ .1, .1, .8 ],
        [ .8, .1, .1 ]
    ]
    B = [ 
        [ 0.9, .05, .05, .9 ],
        [ .05, .9, .05, .05 ],
        [ .05, .05, .9, .05 ]
    ]
    Pi = [ .9, .05, .05 ]
    Y = [ "Bob", "ate", "the", "fruit" ]
    x, p = viterbi(obs, states, Pi, Y, A, B)

    print(x)
    print(f"{round(p*100, 2)}%")