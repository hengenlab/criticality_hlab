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

    # tic = time.time()
    if n == 1:
        network = cdc(data)
    else:
        # collapse into single array. sum the amount of activity in each bin.
        if ncells == -1:
            network = np.nansum(data, axis=0)
        else:
            network = data.copy()
        # print("network ", network)
        # print("sh network ", network.shape)

    # ckbn doubts why we need data now?
    # why we dont give network and n(number of cells) instead of data as input?
    data = None
    del data
    # toc = time.time()
    # print("bustbefor000 calc took time {} seconds".format(toc-tic))

    # tic = time.time()
    if perc > 0:
        sortN = np.sort(network)
        # print("sortN ", sortN)
        # print("sh sortN ", sortN.shape)
        # print("sortN 25% ", sortN[round(m * perc)-10:round(m * perc)+10])
        # print("sortN mean ", np.mean(sortN), " median ", np.median(sortN))
        # print("sortN uniques ", np.unique(sortN, return_counts=True)[0])
        # print("sortN uniquesc ", np.unique(sortN, return_counts=True)[1])
        # determine the treshold. if perc is .25,
        # then its 25% of network activity essentially
        perc_threshold = sortN[round(m * perc)]
        print("perc_threshold ", perc_threshold)
        sortN = None
        del sortN
    else:
        perc_threshold = 0
        print("perc_threshold ", perc_threshold)

    # print("network ", network[0:30])
    zdata = cdc(network)
    # toc = time.time()
    # print("bustbefor00 calc took time {} seconds".format(toc-tic))

    # tic = time.time()
    # intervals
    zdata[zdata <= perc_threshold] = 0
    # print("zdata 0 ", zdata[0:30])
    # avalanches
    zdata[zdata > perc_threshold] = 1
    # print("zdata 1 ", zdata[0:30])
    zdata = zdata.astype(np.int8)

    # location of intervals
    zeros_loc_zdata = np.where(zdata == 0)[0]
    # print("zeros_loc_zdata ", zeros_loc_zdata[0:30])
    zeros_to_delete = \
        zeros_loc_zdata[np.where(np.diff(zeros_loc_zdata) == 1)[0]]
    # print("zeros_to_delete ", zeros_to_delete[0:30])
    # toc = time.time()
    # print("bustbefor01 calc took time {} seconds".format(toc-tic))
    zeros_loc_zdata = None
    del zeros_loc_zdata

    # tic = time.time()
    # cuts out irrelevant 0s result=>, series of 1s and a single 0 separation
    # z1data = np.delete(zdata, Z[np.where(np.diff(Z) == 1)[0]])
    # 1 0 0 1 :  12  5  6  9 (if perc_threshold = 7)  =>  1 0  1 : 12  6  9
    # in short in a series of zeros last zero index is not deleted
    z1data = np.delete(zdata, zeros_to_delete)
    # print("zdata d ", zdata[0:30])
    # print("z1data ", z1data[0:30])
    # print("network ava ", network[0:30])
    # avalanches = np.delete(network, Z[np.where(np.diff(Z) == 1)[0]])
    avalanches = np.delete(network, zeros_to_delete)
    # print("avalanches ", avalanches[0:30])
    # use a single 0 to separate network activities in each avalanche
    avalanches[z1data == 0] = 0
    # print("avalanches ", avalanches[0:30])

    # location of the intervals
    zeros_loc_z1data = np.where(z1data == 0)[0]
    # print("zeros_loc_z1data ", zeros_loc_z1data[0:30])
    # toc = time.time()
    # print("bustbefor02 calc took time {} seconds".format(toc-tic))

    # Now calculate S and T based on avalanches and z1data
    burst = []
    # tic = time.time()
    for i in np.arange(0, np.size(zeros_loc_z1data) - 1):
        tmp_av = avalanches[zeros_loc_z1data[i] + 1:zeros_loc_z1data[i + 1]]
        tmp_burst = np.sum(tmp_av) - (perc_threshold * len(tmp_av))
        if tmp_burst <= 0:
            raise RuntimeError('Burst value {}, zero/negative'
                               .format(tmp_burst))
        burst.append(tmp_burst)
    # print("burst ", burst[0:30])
    # toc = time.time()
    # print("bust calc took time {} seconds".format(toc-tic))
    tmp_av = None
    del tmp_av

    # tic = time.time()
    # AVduration
    T = np.diff(zeros_loc_z1data) - 1
    # print("T ", T[0:30])
    # Duration should be positive
    # print("T < 0 ", T[T < 0])
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

    # toc = time.time()
    # print("bustaft calc took time {} seconds".format(toc-tic))

    ttoc = time.time()
    print("Time took in get_avalanches is {} seconds".format(ttoc-ttic),
          flush=True)

    # # print variable and sizes
    # local_vars = list(locals().items())
    # for var, obj in local_vars:
    #    print("Variable ", var, " size ", sys.getsizeof(obj), " id ", id(obj))

    return Result
