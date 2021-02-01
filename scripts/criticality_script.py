import criticality as cr
import neuraltoolkit as ntk
import musclebeachtools as mbt
import numpy as np

# Load sample binary data which is already binned.
# bin by 1 for model and 1-40 ms for data
data = np.load('/hlabhome/shlabhome/kiranbn/test_crit/criticality_hlab/data/sample_data.npy')

# Define variables
# threshold : 25 % spikes
perc = 0.25

# This goes through your data and
# it finds all avalanches and create two arrays
# and put them to a dict : S size, T duration
r = cr.get_avalanches(data, perc)
burst = r['S']
T = r['T']

# flag 2 = pvalue and dcc, else just dcc
# bm : None=max calulate inside code, model 10, rawdata 10-20
# tm : None=max calulate inside code, model 4, rawdata 2-20
# pltname : plot name
# saveloc : Location to save plots
# burst_shuffled : not enabled, None
# T_shuffle : not enabled, None
# plot_shuffled : not enabled, None
# plot : True
# params = {'flag': 2, 'bm': None, 'tm': None, 'pltname': "test",
# params = {'flag': 1, 'bm': None, 'tm': None, 'pltname': "testmodel",
params = {'flag': 2, 'bm': 10, 'tm': 2, 'pltname': "testmodel",
          'saveloc': '/hlabhome/shlabhome/kiranbn/test_crit/criticality_hlab/data/',
          'burst_shuffled': None, 'T_shuffle': None,
          'plot_shuffled': False, 'plot': True}

# run the code
Result = cr.AV_analysis(burst, T, params, nfactor_bm=4, nfactor_tm=1,
                        nfactor_bm_tail=0.9, nfactor_tm_tail=1.0,
                        none_fact=10, max_time=600)

# check results
if params['flag'] == 2:
    if (Result['P_t'] > 0.05 and Result['P_burst'] > 0.05):
        print('''For this example,
              pvalues for both size and duration distributions
              are larger than 0.05''')
        print('''Null hypothesis could not be rejected.
              Dataset follows power law distribution''')
    else:
        print('''Null hypothesis could be rejected.
              Dataset follows power law distribution''')
print("DCC ", Result['df'])

