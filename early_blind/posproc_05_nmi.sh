#!/bin/bash 

#SBATCH -J NMId2sc
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/NMId2sc.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/NMId2sc.err
#SBATCH -c 1
#SBATCH -a 1-18

echo "------------------------------------------------" 
echo "Slurm Job ID: $SLURM_JOB_ID" 
echo "Run on host: "`hostname`
echo "Operating system: "`uname -s`
echo "Username: "`whoami`
echo "Started at: "`date`
echo "------------------------------------------------" 

source /gpfs3/well/margulies/users/anw410/conts/my_imgs/v_py_env_3-9/v_act.sh

dir_ts=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/ts_sm/d2/ctrl
dir_sv=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/NMI_extra/d2/sc

label=sub-ctrl
if [ ${SLURM_ARRAY_TASK_ID} -lt 10 ]; then sjname=${label}0${SLURM_ARRAY_TASK_ID}; else sjname=${label}-${SLURM_ARRAY_TASK_ID}; fi
echo ${sjname}

fil_ts=${dir_ts}/${sjname}_sm4.npy

python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/ebps/posproc_05_nmi.py ${fil_ts} ${dir_sv} d2_sc_${sjname}