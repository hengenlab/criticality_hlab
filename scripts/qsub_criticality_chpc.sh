#!/bin/bash
#PBS -N jqsub_spkint
#PBS -l nodes=1:ppn=1,walltime=2:0:00

# Make sure ncpus in spikeinterface_currentall.py is same as ppn
# Please change BASEDIR
BASEDIR=/scratch/khengen_lab/env_for_criticality/criticality_hlab/scripts/
OUTDIR=/scratch/khengen_lab/env_for_criticality/criticality_hlab/scripts/

# Get name for log file
JOBID=`echo ${PBS_JOBID} | cut -c1-12`
output_name=${PBS_JOBNAME}_${JOBID}.log

# Load modules
module purge all
module load gcc-4.7.2
module load opencv

# Activate conda
. /scratch/khengen_lab/anaconda3/etc/profile.d/conda.sh
conda activate criticality

# do exports
export HDF5_USE_FILE_LOCKING=FALSE
export PYTHONPATH=/scratch/khengen_lab/git/:$PYTHONPATH

cd $BASEDIR
python  $BASEDIR/criticality_script.py &> $OUTDIR/$output_name
