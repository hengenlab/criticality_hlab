# Criticality

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




## Test run

```
import criticality_hlab.criticality as cr
import numpy as np

# Load sample binary data which is already binned.
data = np.load('data/sample_data.npy')
# To run data from mbt, instead of loading data from previous step
# import musclebeachtools as mbt
# time_start = 0
# time_end = 3600*4
# binsize = 20
# neuronlist is output from musclebeachtools (mbt) please see mbt manual
# spks = mbt.getspikes(neuronlist, time_start, time_end)
# data_T = mbt.spiketimes_to_spikewords(spks, time_start, time_end,
#                                       binsize, 1)
# data = data_T.T
# Calculate Avalanche size and duration, (AVsize and AVduration)
# The default threshold is 25 percentile. But we could change it by tuning
# ‘perc’. Make  sure ‘perc’ is in the range from 0 -- 1. When network
# activity is silent most time, should set ‘perc’ = 0, which means threshold
# is zero
r = cr.AV_analysis_BurstT(data, perc=0.25)
x = np.transpose(r['S'])  # x is AVsize
y = r['T']  # y is AVdura
# Avalanche analysis
# including AVsize, AVduration distribution and scaling relation.
# burstM and tM are used to set the limits for lower boundary
# for AVsize and AVduration distributions.
# Result1 only returns exponents and lower/upper bounds limits
# Result2 return pvalue for null hypothesis in addition Result1
# Result3 generate a figure including the distributions
burstM = 10
tM = 2
pltname = "test_data_1"

Result2 = cr.AV_analysis_new(x, y, burstM, tM, pltname, flag=2,
                             saveloc='/hlabhome/kiranbn/git/', plot=True)
print('Pvalue for size distribution is : ' + str(Result2['P_burst']))
print('Pvalue for duration distribution is : ' + str(Result2['P_t']))
# print('Result2 ', Result2)
if (Result2['P_t'] > 0.05 and Result2['P_burst'] > 0.05):
    print('''For this example,
          pvalues for both size and duration distributions
          are larger than 0.05''')
    print('''Null hypothesis could not be rejected.
          Dataset follows power law distribution''')
Result3  = cr.AV_analysis_new(x, y, burstM, tM, pltname, flag=1,
                              saveloc='/hlabhome/kiranbn/git/', plot=True)
print(Result3['df'])
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
