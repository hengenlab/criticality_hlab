#!/bin/bash
#PBS -S /bin/bash
#PBS -N criticality_job_1
#PBS -V
#PBS -l nodes=tyromancer.wustl.edu:ppn=1,walltime=24:00:00


### #PBS -l nodes=1:ppn=1:gpus=1:exclusive_process,walltime=24:00:00


# Make sure ncpus in spikeinterface_currentall.py is same as ppn
# Please change BASEDIR
BASEDIR=/hlabhome/shlabhome/kiranbn/test_crit/criticality_hlab/scripts/
OUTDIR=/hlabhome/shlabhome/kiranbn/test_crit/criticality_hlab/scripts/

# Get name for log file
JOBID=`echo ${PBS_JOBID} | cut -c1-12`
output_name=${PBS_JOBNAME}_${JOBID}.log

# TMP_DIR="/media/Scratch/tmp_${JOBID}"
# TMP_DIR_JSON="/media/Scratch/tmp_json_${JOBID}"
# mkdir $TMP_DIR
# mkdir $TMP_DIR_JSON
# echo "TMP_DIR ", $TMP_DIR
# echo "TMP_DIR_JSON ", $TMP_DIR_JSON

# # NP=$(wc -l $PBS_NODEFILE | awk '{print $1}')
# NP=4
# echo "Total CPU count = $NP"
# echo $PBS_O_SHELL
# export OMP_NUM_THREADS=$NP
# echo $OMP_NUM_THREADS
# export NUM_WORKERS=$NP
# export MKL_NUM_THREADS=$NP
# export NUMEXPR_NUM_THREADS=$NP


# Activate conda
. /hlabhome/shlabhome/opt/anaconda3/etc/profile.d/conda.sh
conda activate criticality

# do exports
export HDF5_USE_FILE_LOCKING=FALSE
export PYTHONPATH=/hlabhome/shlabhome/anaconda/git/:$PYTHONPATH

cd $BASEDIR
python  $BASEDIR/criticality_script.py &> $OUTDIR/$output_name
# rm -rf $TMP_DIR_JSON
# rm -rf $TMP_DIR

# # qdel -W 120 jobid
# cleanup() {
#  echo "Cleaning up temp files:"
#  echo "TMP_DIR " $TMP_DIR
#  rm -rf "$TMP_DIR"
#  exit 1
# }
# trap 'cleanup' 2 9 15
