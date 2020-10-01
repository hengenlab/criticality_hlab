import numpy as np
from criticality import tplfit_new as tp
from copy import deepcopy as cdc


def EXCLUDE(burst, setmin, num=1, nfactor=0):

    '''
    Determine both the lower and upper boundaries with a small KS
    '''

    KS = 1
    dKS = 1
    xmin = 1
    loop_indx = 0

    print("burst ", burst)
    print("burst[burst > xmin] ", burst[burst > xmin])
    print("0 ", np.size(burst[burst > xmin]))
    print("1 ", np.sqrt(np.size(burst[burst > xmin])))
    print("2 ", num/np.sqrt(np.size(burst[burst > xmin])))
    while ((KS > np.min([num/np.sqrt(np.size(burst[burst > xmin])), 0.1]))
            and (dKS > 0.0005)):
        loop_indx += 1
        alpha, xmin, ks, Loglike = tp.tplfit(burst, setmin, nfactor=nfactor)
        alpha = alpha[0]
        xmax = np.max(burst)

        z = burst[burst >= xmin]
        n = np.size(z)
        cdf = np.cumsum(np.histogram(z, bins=np.arange(xmin, xmax+2))[0]/n)

        idx = np.where(np.logical_and(xmin <= burst, burst <= xmax))[0]
        s = np.unique(burst[idx])
        A = 1/np.sum(np.power(s, -alpha))
        fit = np.cumsum(A*np.power(np.arange(xmin, xmax+1), -alpha))

        KS_old = cdc(KS)

        KS = np.max(np.abs(cdf - fit))
        dKS = np.abs(KS_old-KS)
        if not loop_indx % 200:
            print("dKS ", dKS)
        burst = burst[burst < np.max(burst)]
        # print("len burst ", len(burst))
        burstMax = np.max(burst)

    print("dKS Final ", dKS)
    burstMin = xmin
    return burstMax, burstMin, alpha
