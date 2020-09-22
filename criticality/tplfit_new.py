import numpy as np
from copy import deepcopy as cdc
import scipy.optimize
# from scipy.stats import powerlaw


def tplfit(burst, limit, nfactor=0):
    """
        this code runs a loop to determine a good minima for your data to fit
        the most ideal powerlaw, it runs from 1 to your boundary and then
        chooses the smallest ks value, the minima at that point
        is your xmin

        only going to use for determining the minima, not anything else
    """
    KS = []
    alpha = []
    Loglike = []
    alpha = []

    # print("burst ", burst, flush=True)
    # print("len burst ", len(burst), flush=True)
    if (len(burst) == 0):
        raise RuntimeError('Error: Burst is empty, tplfit')
    xmax = np.max(burst)

    for indx, xmin in enumerate(np.arange(1+nfactor, limit+1)):
        idx = np.where(np.logical_and(burst >= xmin, burst <= xmax))[0]
        n = np.size(burst[idx])
        s = np.unique(burst[idx])
        # smin = np.min(s)
        # smax = np.max(s)

        LL = lambda x: x*np.sum(np.log(burst[idx])) -\
            n*np.log(1/np.sum(np.power(s, -x)))
        #  scipy.optimize.fmin(func, x0, args=(), xtol=0.0001, ftol=0.0001,
        #                      maxiter=None, maxfun=None, full_output=0,
        #                      disp=1, retall=0, callback=None,
        #                      initial_simplex=None)
        # a = scipy.optimize.fmin(func=LL, x0=2.3, disp=False)
        # es['x'], res['fun'], res['nit'], res['nfev'], res['status']
        a,_ ,_ ,_, lstatus = scipy.optimize.fmin(func=LL, x0=1.0,
                                xtol=0.000001, ftol=0.000001, maxiter=1000,
                                full_output=True,
                                disp=False)
        # print("a ", a)
        if (lstatus != 0):
            raise RuntimeError('Error: scipy.optimize.fmin not successful',
                               lstatus)
        fval = LL(a)
        Loglike.append(-fval)

        cdf = \
            np.cumsum(np.histogram(burst[idx],
                      bins=np.arange(xmin, xmax+2))[0]/n)
        A = 1/(np.sum(np.power(s, -a)))
        alpha.append(a)
        fit = np.cumsum(A*np.power(np.arange(xmin, xmax+1), -a))
        KS.append(np.max(np.abs(cdf-fit)))

    xmin = int(np.where(KS == np.min(KS))[0]) + nfactor
    alpha = alpha[int(np.where(KS == np.min(KS))[0])]
    Loglike = Loglike[int(np.where(KS == np.min(KS))[0])]
    ks = np.min(KS)
    xmin = xmin + 1

    return alpha, xmin, ks, Loglike
