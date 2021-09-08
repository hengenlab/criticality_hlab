import numpy as np
from criticality import pvaluenew2 as pv
from criticality import exclude as ex
import matplotlib.pyplot as plt
import seaborn as sns
import os.path as op


def scaling_plots(Result, burst, burstMin, burstMax, alpha, T, tMin, tMax,
                  beta, TT, Sm, sigma, fit_sigma, pltname, saveloc, p_val_b, p_val_t):
    # burst PDF
    burstMax = int(burstMax)
    burstMin = int(burstMin)
    fig1, ax1 = plt.subplots(nrows = 1, ncols = 3, figsize = [10, 6])
    pdf = np.histogram(burst, bins = np.arange(1, np.max(burst) + 2))[0]
    p = pdf / np.sum(pdf)
    ax1[0].plot(np.arange(1, np.max(burst) + 1), p, marker = 'o',
                markersize = 5, fillstyle = 'none', mew = .5,
                linestyle = 'none', color = 'darkorchid', alpha = 0.75)
    ax1[0].plot(np.arange(1, np.max(burst) + 1)[burstMin:burstMax],
                p[burstMin:burstMax], marker = 'o', markersize = 5,
                fillstyle = 'full', linestyle = 'none', color = 'darkorchid',
                alpha = 0.75)
    ax1[0].set_yscale('log')
    ax1[0].set_xscale('log')

    x = np.arange(burstMin, burstMax + 1)
    y = (np.size(np.where(burst == burstMin + 6)[0]) / np.power(burstMin + 6, -alpha)) *\
        np.power(x, -alpha)
    y = y / np.sum(pdf)

    ax1[0].plot(x, y, color = '#c5c9c7')
    ax1[0].set_xlabel('AVsize')
    ax1[0].set_ylabel('PDF(S)')
    ax1[0].set_title('AVsize PDF, ' + str(np.round(alpha, 3)))
    if p_val_b is not None:
        ax1[0].text(10, .1, f'p_val = {p_val_b}')

    # time pdf
    tdf = np.histogram(T, bins = np.arange(1, np.max(T) + 2))[0]
    t = tdf / np.sum(tdf)
    ax1[1].plot(np.arange(1, np.max(T) + 1), t, marker = 'o',
                markersize = 5, fillstyle = 'none', mew = .5,
                linestyle = 'None', color = 'mediumseagreen', alpha = 0.75)
    ax1[1].plot(np.arange(1, np.max(T) + 1)[tMin:tMax], t[tMin:tMax],
                marker = 'o', markersize = 5, fillstyle = 'full',
                linestyle = 'none', color = 'mediumseagreen', alpha = 0.75)
    ax1[1].set_yscale('log')
    ax1[1].set_xscale('log')
    sns.despine()

    x = np.arange(tMin, tMax + 1)
    y = np.size(np.where(T == tMin)) / (np.power(tMin, -beta)) *\
        np.power(x, -beta)
    y = y / np.sum(tdf)
    ax1[1].plot(x, y, color = '#c5c9c7')
    ax1[1].set_xlabel('AVduration')
    ax1[1].set_ylabel('PDF(D)')
    ax1[1].set_title('AVdura PDF, ' + str(np.round(beta, 3)))
    if p_val_t is not None:
        ax1[1].text(10, .1, f'p_val = {p_val_t}')


    # figure out how to plot shuffled data

    # scaling relation
    i = np.where(TT == tMax)  # just getting the last value we use, getting rid of the hard codes
    ax1[2].plot(TT, ((np.power(TT, sigma) / np.power(TT[7], sigma)) * Sm[7]),
                label = 'pre', color = '#4b006e')
    ax1[2].plot(TT, (np.power(TT, fit_sigma[0]) / np.power(TT[7], fit_sigma[0]) * Sm[7]),
                'b', label = 'fit', linestyle = '--', color = '#826d8c')
    ax1[2].plot(TT, Sm, 'o', color = '#fb7d07', markersize = 5, mew = .5,
                fillstyle = 'none', alpha = 0.75)

    locs = np.where(np.logical_and(TT < tMax, TT > tMin))[0]

    ax1[2].plot(TT[locs], Sm[locs], 'o', markersize = 5, mew = .5,
                color = '#fb7d07', fillstyle = 'full', alpha = 1)
    ax1[2].set_xscale('log')
    ax1[2].set_yscale('log')
    ax1[2].set_ylabel('<S>')
    ax1[2].set_xlabel('Duration')
    ax1[2].set_title('Difference = ' + str(np.round(Result['df'], 3)))

    plt.tight_layout()
    plt.legend()
    # plt.savefig(saveloc + "/" + pltname + 'scaling_relations' + '.svg', format='svg')
    savefigpath = op.join(saveloc , pltname + 'scaling_relations' + '.svg')
    print("savefigpath " savefigpath)
    plt.savefig(savefigpath, format='svg')

    return fig1


def AV_analysis(burst, T, flag = 1, bm = 20, tm = 10, nfactor_bm=0, nfactor_tm=0,
                nfactor_bm_tail=0.8, nfactor_tm_tail=1.0, none_fact=40,
                max_time=7200, verbose = True, exclude = False, exclude_burst = 50, 
                exclude_time = 20, exclude_diff_b=20, exclude_diff_t=10, plot=True, pltname='', saveloc=''):
    #print('VERBOSE: ', verbose)

    if bm is None:
        if verbose:
            print('none_fact ', none_fact)
        bm = int(np.max(burst)/none_fact)

    Result = {}
    burstMax, burstMin, alpha = \
        ex.EXCLUDE(burst[burst < np.power(np.max(burst), nfactor_bm_tail)], bm,
                   nfactor=nfactor_bm, verbose = verbose)
    idx_burst = \
        np.where(np.logical_and(burst <= burstMax, burst >= burstMin))[0]
    # print("burst[idx_burst] ", burst[idx_burst])
    # print("idx_burst ", idx_burst)
    if verbose:
        print("alpha ", alpha)
        print("burst min: ", burstMin)
        print("burst max:", burstMax, flush=True)

    Result['burst'] = burst
    Result['alpha'] = alpha
    Result['xmin'] = burstMin
    Result['xmax'] = burstMax

    Result['P_burst'] = None
    Result['EX_b'] = False
    if exclude:
        if burstMin > exclude_burst or (burstMax-burstMin)<exclude_diff_b:
            print(f'This block excluded for burst: xmin {burstMin} diff: {burstMax-burstMin}')
            Result['EX_b'] = True
    
    if flag == 2 and not Result['EX_b']:
        if verbose:
            print("About to do the p val test for burst")
        # pvalue test
        Result['P_burst'], ks, hax_burst, ptest_bmin = \
            pv.pvaluenew(burst[idx_burst], alpha, burstMin, nfactor=nfactor_bm,
                         max_time=max_time, verbose = verbose)

    if tm is None:
        if verbose:
            print('none_fact ', none_fact)
        tm = int(np.max(T)/none_fact)

    # print("tMax, tMin, beta = ex.EXCLUDE(T, tm)")
    # ckbn tMax, tMin, beta = ex.EXCLUDE(T, tm, nfactor=nfactor_tm)
    tMax, tMin, beta = \
        ex.EXCLUDE(T[T < np.power(np.max(T), nfactor_tm_tail)], tm,
                   nfactor=nfactor_tm, verbose = verbose)
    idx_time = np.where(np.logical_and(T >= tMin, T <= tMax))[0]

    if verbose:
        print("beta ", beta)
        print(f'time min: {tMin}')
        print(f'time max: {tMax}', flush=True)

    Result['T'] = T
    Result['beta'] = beta
    Result['tmin'] = tMin
    Result['tmax'] = tMax

    Result['P_t'] = None
    Result['EX_t'] = False
    if exclude:
        if tMin > exclude_time or (tMax-tMin)<exclude_diff_t:
            print(f'This block excluded for time: tmin {tMin} diff: {tMax-tMin}')
            Result['EX_t'] = True

    if flag == 2 and not Result['EX_t'] and not Result['EX_b']:
        if verbose:
            print("About to do the p val test for time")
        # pvalue for time
        Result['P_t'], ks, hax_time, ptest_tmin = \
            pv.pvaluenew(T[idx_time], beta, tMin, nfactor=nfactor_tm,
                         max_time=max_time, verbose=verbose)

    TT = np.arange(1, np.max(T) + 1)
    Sm = []
    for i in np.arange(0, np.size(TT)):
        Sm.append(np.mean(burst[np.where(T == TT[i])[0]]))
    Sm = np.asarray(Sm)
    Loc = np.where(Sm > 0)[0]
    TT = TT[Loc]
    Sm = Sm[Loc]

    # ckbndnt
    fit_sigma = \
        np.polyfit(np.log(TT[np.where(np.logical_and(TT > tMin,
                                                     TT < tMax))[0]]),
                   np.log(Sm[np.where(np.logical_and(TT > tMin,
                                                     TT < tMax))[0]]), 1)
    sigma = (beta - 1) / (alpha - 1)
    if verbose:
        print("fit_sigma ", fit_sigma)
        print("sigma ", sigma, flush=True)


    Result['pre'] = sigma
    Result['fit'] = fit_sigma
    Result['df'] = np.abs(sigma - fit_sigma[0])
    Result['TT'] = TT
    Result['Sm'] = Sm
    Result['burst_cdf'] = None
    Result['time_cdf'] = None
    Result['scaling_relation_plot'] = None 

    if plot:
        fig1 = scaling_plots(Result, burst, burstMin, burstMax, alpha, T,
                             tMin, tMax, beta, TT, Sm, sigma, fit_sigma,
                             pltname, saveloc, Result['P_burst'], Result['P_t'])
        if flag == 2 and not Result['EX_t'] and not Result['EX_b']:
            hax_burst.axes[0].set_xlabel('Size (S)', fontsize=16)
            hax_burst.axes[0].set_ylabel('Prob(size < S)', fontsize=16)
            # hax_burst.savefig(saveloc + "/" + pltname + 'pvalue_burst' + '.svg', format='svg')
            savefigpathb = op.join(saveloc,  pltname + 'pvalue_burst' + '.svg')
            print("savefigpathb " savefigpathb)
            hax_burst.savefig(savefigpathb, format='svg')

            hax_time.axes[0].set_xlabel('Duration (D)', fontsize=16)
            hax_time.axes[0].set_ylabel('Prob(size < D)', fontsize=16)
            # hax_time.savefig(saveloc + "/" + pltname + 'pvalue_time' +  '.svg', format='svg')
            savefigpathb = op.join(saveloc, pltname + 'pvalue_time' + '.svg')
            print("savefigpatht " savefigpatht)
            hax_burst.savefig(savefigpatht, format='svg')
            Result['burst_cdf'] = hax_burst
            Result['time_cdf'] = hax_time
        Result['scaling_relation_plot'] = fig1
        plt.close('all')

    return Result
