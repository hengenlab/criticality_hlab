import criticality as cr
import numpy as np
import musclebeachtools as mbt 

cells = np.load('path/to/cells.npy')
good_cells = [cell for cell in cells if cell.quality < 3]

data = mbt.n_spiketimes_to_spikewords(good_cells, binsz=0.04, binarize=1)
R = cr.get_avalanches(data, perc=0.35)

burst = R['S']
T = R['T']


# flag: 1 - DCC, 2 - PValueTest and DCC
# bm: upper limit of xmin
# tm: upper limit of tmin
# nfactor_bm: lower limit of xmin
# nfactor_tm: lower limit of tmin
# nfactor_bm_tail: upper limit of xmax
# nfactor_tm_tail: upper limit of tmax
# none_fact: if bm/tm is None, bm=np.max(burst)/none_fact and tm=np.max(T)/none_fact
# max_time: timeout threshold
# verbose: if True there will be excessive printouts, if False there will be less excessive printouts
# exclude: Boolean, if True then the pvalue will be skipped if certain thresholds are broken (saves time by skipping bad distribtions)
# exclude_burst: if xmin crosses this then pvalue is skipped and EX_b is true
# exclude_time: ^^ same for time
# exclude_diff_b: if xmax-xmin is less than this number then pvalue is skipped and EX_b is true
# exclude_diff_t: ^^ same for time
# plot: if True plots will be outputted
# pltname: what to name the plots
# saveloc: where to save the plots
Result = cr.AV_analysis(burst, T, flag = 1, bm = 20, tm = 10, nfactor_bm=0, nfactor_tm=0,
                nfactor_bm_tail=0.8, nfactor_tm_tail=1.0, none_fact=40,
                max_time=7200, verbose = True, exclude = False, exclude_burst = 50, 
                exclude_time = 20, exclude_diff_b=20, exclude_diff_t=10, plot=True, pltname='test', saveloc='/media/HlabShare/')

dcc = Result['df']
