# Criticality
---
This version is under debugging and testing, please do not use as production code.

---
![Tests](https://github.com/hengenlab/criticality_hlab/actions/workflows/pytests.yml/badge.svg)

## Installation

### Download Criticality
```
git clone https://github.com/hengenlab/criticality_hlab.git
Enter your username and password  
```

### Using pip
```
cd locationofcriticality_hlab/criticality_hlab/  
pip install .
```
<!--
### Adding to path
#### Windows
My Computer > Properties > Advanced System Settings > Environment Variables >  
In system variables, create a new variable  
    Variable name  : PYTHONPATH  
    Variable value : location where criticality_hlab is located  
    Click OK  


#### Linux
If you are using bash shell  
In terminal open .barshrc or .bash_profile  
add this line  
export PYTHONPATH=/location_of_criticality_hlab:$PYTHONPATH  


#### Mac
If you are using bash shell  
In terminal cd ~/  
then open  .profile using your favourite text editor (open -a TextEdit .profile)  
to add location where criticality_hlab is located add the line below  

export PYTHONPATH=/location_of_criticality_hlab:$PYTHONPATH  
-->



## Test run

```
import criticality as cr
import numpy as np

# Load sample binary data which is already binned.
# bin by 1 for model and 1-40 ms for data
data = np.load('../data/sample_data.npy')

# Define variables
# threshold : 25 % spikes
perc = 0.25

# This goes through your data and
# it finds all avalanches and create two arrays
# and put them to a dict : S size, T duration
r = cr.get_avalanches(data, perc)
# burst = r['S']
# T = r['T']

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
params = {'flag': 1, 'bm': 10, 'tm': 2, 'pltname': "testmodel",
          'saveloc': '/hlabhome/kiranbn/git/criticality_hlab/data/',
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
```
or
```
import criticality as cr
import numpy as np
import sys

data = np.load('spikes_all_369000.npy')
print("sh data ", data.shape)
n_cells = np.load('spikes_all_369000_ncells.npy')
print("n_cells ", n_cells)

# Define variables
# threshold : 25 % spikes
# perc = 0.25

# This goes through your data and
# it finds all avalanches and create two arrays
# and put them to a dict : S size, T duration
r = cr.get_avalanches(data, perc, ncells=n_cells)
print("r['T'] ", r['T'])
print("r['S'] ", r['S'])
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
params = {'flag': 1, 'bm': 10, 'tm': 2, 'pltname': "testmodel",
          'saveloc': '/hlabhome/kiranbn/git/criticality_hlab/data/',
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

```

## References
Please check out the following references for more details:  
```
@article{MA2019,  
author = "Zhengyu Ma and Gina G. Turrigiano and Ralf Wessel and Keith B. Hengen",  
title = "Cortical Circuit Dynamics Are Homeostatically Tuned to Criticality In Vivo",  
journal = "Neuron",  
year = "2019",  
issn = "0896-6273",  
doi = "https://doi.org/10.1016/j.neuron.2019.08.031",  
url = "http://www.sciencedirect.com/science/article/pii/S0896627319307378"  
}
```
