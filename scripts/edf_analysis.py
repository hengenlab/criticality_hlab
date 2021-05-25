try:
    from pyedflib import highlevel
except ImportError:
    raise ImportError('Run command : conda install -c conda-forge pyedflib')
import matplotlib.pyplot as plt
import os.path as op
import glob


edf_dir = '/media/HlabShare/AD_paper/eeg_data_landsness_lucey/SP_data_for_Keith_Hengen/SP022_A1_for_Hengen_03052021/SP022_A_EDF/SP022N1-3/'

# Deal with mac mounts
if not op.exists(edf_dir) and op.isdir(edf_dir):
    edf_dir = edf_dir.replace('media', 'Volumes')
print(edf_dir)
edf_files = glob.glob(edf_dir + '*.edf')

# Loop over edf files
for edf_file in edf_files:
    signals, signal_headers, header = highlevel.read_edf(edf_file)
    fs = signal_headers[0]['sample_rate']
    num_chs = len(signals)
    print("sampling rate is {} and number of channels is {}"
           .format(fs, num_chs))
    for i in range(num_chs):
        plt.subplot(num_chs, 1, i+1)
        plt.plot(signals[0])
    plt.show()
    # break after first file
    break
