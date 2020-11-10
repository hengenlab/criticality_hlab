import numpy as np
from criticality import tplfit_new as tp
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import time


def pvaluenew(burst, alpha, xmin, nfactor=0,
              max_time=7200):

    '''
    '''

    # not truly the max, cause we pass in the truncated dataset
    xmax = np.max(burst)
    n = np.size(burst)
    cdf = np.cumsum(np.histogram(burst, np.arange(xmin, xmax+2))[0]/n)
    s = np.unique(burst)
    A = 1/np.sum(np.power(s, -alpha))
    fit = np.cumsum(A*np.power(np.arange(xmin, xmax+1), -alpha))
    KS = np.max(np.abs(cdf-fit))

    hfig, hax = plt.subplots(ncols=1, nrows=1)
    sns.despine()
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=13)

    hax.plot(np.arange(xmin, xmax+1), fit, zorder=10000,
             label='Power law CDF', color='#0504aa')
    hax.plot(np.arange(xmin, xmax+1), cdf, zorder=10005,
             label='Experimental CDF', color='#80013f')
    hax.legend()
    hax.set_title('Cumulative Distribution Function', fontsize=12)
    hax.set_xscale('log')
    shape, loc, scale = stats.lognorm.fit(burst, floc=0)

    sns.despine()

    ks = []
    j = 1
    Niter = 1000

    # syn data 10 times size of original
    N = 10 * np.size(burst)

    max_time_start = time.time()
    while j < Niter:
        # print("max_time ", max_time,
        #       "time elapsed ", (time.time() - max_time_start), flush=True)
        if ((time.time() - max_time_start) > max_time):
            raise RuntimeError("Pvalue took more than max_time {} seconds".
                               format(max_time))

        if not j % 200:
            print(str(j) + " loops completed", flush=True)

        syn_data = np.floor((xmin-1/2)*np.power((1-np.random.uniform(0, 1, N)),
                            (1/(1-alpha))) + 1/2)
        # print("1 syn_data", syn_data, " xmin ", xmin)
        syn_data = np.floor(np.heaviside(xmax-syn_data, 1/2) * syn_data)
        syn_data = np.delete(syn_data, np.where(syn_data == 0)[0])
        syn_data = syn_data[0:n]
        idx_syn = np.where(np.logical_and(xmin <= syn_data,
                                          syn_data <= xmax))[0]
        X = syn_data[idx_syn]
        # print("2 syn_data", syn_data, " xmin ", xmin)
        # calculate exponent for surrogated data
        alpha_syn, xmin_syn, ks_syn, Loglike_syn = tp.tplfit(syn_data, xmin,
                                                             nfactor=nfactor)
        a = alpha_syn[0]

        if ((np.abs(a-alpha) <= 0.1) and (a > 1.0)):
            size = np.size(X)
            cdf = np.cumsum(np.histogram(X, np.arange(xmin, xmax+2))[0]/size)
            s = np.unique(X)

            A = 1/np.sum(np.power(s, -alpha))
            fit = np.cumsum(A*np.power(np.arange(xmin, xmax+1), -alpha))
            ks.append(np.max(np.abs(cdf - fit)))
            j = j + 1
            hax.plot(np.arange(xmin, xmax+1), cdf, color='#647d8e',
                     alpha=0.05, linewidth=0.3)

    ks = np.asarray(ks)
    P_value = np.sum(np.sign(ks[ks >= KS]))/Niter

    print('P_value = ' + str(P_value))
    print('KS = ' + str(KS))

    return P_value, ks, hfig, xmin
