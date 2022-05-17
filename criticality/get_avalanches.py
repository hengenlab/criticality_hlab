import numpy as np
from copy import deepcopy as cdc
import time
# import sys


def get_avalanches(data, perc=0.25, ncells=-1):

    '''
    Function that goes through an array of binned spikes and determines
        the avalanch boundaries and properties

    parameters:
        data - array of spike times. one row for each neuron
        perc - threshold for defining an avalanche,
            if network is dominated by silent periods you can use 0
        ncells - default (-1), number of cells calculated from data shape
                 if ncells given expect data to be 1 dimensional
                 np.nansum(data, axis=0)

    returns:
    Result - a dictionary with 2 inputs.
        'S' is the size of each avalanche (number of spikes above threshold)
        'T' is the duration (number of time bins avalanche spanned)
    '''

    # To time the function
    ttic = time.time()

    # num cells, num bins
    if ncells == -1:
        n, m = np.shape(data)
    else:
        n = ncells
        m = np.shape(data)[0]
    print("Data has {} neurons with length {}*binsize".format(n, m))

    if n == 1:
        network = cdc(data)
    else:
        # collapse into single array. sum the amount of activity in each bin.
        if ncells == -1:
            network = np.nansum(data, axis=0)
        else:
            network = data.copy()

    data = None
    del data

    if perc > 0:
        sortN = np.sort(network)
        # determine the treshold. if perc is .25,
        # then its 25% of network activity essentially
        perc_threshold = sortN[round(m * perc)]
        print("perc_threshold ", perc_threshold)
        sortN = None
        del sortN
    else:
        perc_threshold = 0
        print("perc_threshold ", perc_threshold)

    zdata = cdc(network)

    # intervals
    zdata[zdata <= perc_threshold] = 0

    # avalanches
    zdata[zdata > perc_threshold] = 1
    zdata = zdata.astype(np.int8)

    # location of intervals
    zeros_loc_zdata = np.where(zdata == 0)[0]
    zeros_to_delete = \
        zeros_loc_zdata[np.where(np.diff(zeros_loc_zdata) == 1)[0]]
    zeros_loc_zdata = None
    del zeros_loc_zdata

    # cuts out irrelevant 0s result=>, series of 1s and a single 0 separation
    # 1 0 0 1 :  12  5  6  9 (if perc_threshold = 7)  =>  1 0  1 : 12  6  9
    # in short in a series of zeros last zero index is not deleted
    z1data = np.delete(zdata, zeros_to_delete)
    avalanches = np.delete(network, zeros_to_delete)
    # use a single 0 to separate network activities in each avalanche
    avalanches[z1data == 0] = 0

    # location of the intervals
    zeros_loc_z1data = np.where(z1data == 0)[0]

    # Now calculate S and T based on avalanches and z1data
    burst = []
    for i in np.arange(0, np.size(zeros_loc_z1data) - 1):
        tmp_av = avalanches[zeros_loc_z1data[i] + 1:zeros_loc_z1data[i + 1]]
        tmp_burst = np.sum(tmp_av) - (perc_threshold * len(tmp_av))
        if tmp_burst <= 0:
            raise RuntimeError('Burst value {}, zero/negative'
                               .format(tmp_burst))
        burst.append(tmp_burst)
    tmp_av = None
    del tmp_av

    # AVduration
    T = np.diff(zeros_loc_z1data) - 1
    # Duration should be positive
    T = T[T > 0]

    z2data = zdata[0:-1]
    z2data = np.insert(z2data, 0, 0)
    location = np.where(np.logical_and(zdata == 1, z2data == 0))[0]
    location = location[1:-1]

    Result = {
        'S': np.asarray(burst),
        'T': T,
        'loc': location
    }

    ttoc = time.time()
    print("Time took in get_avalanches is {:.2f} seconds".format(ttoc-ttic),
          flush=True)

    return Result
