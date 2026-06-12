#!/bin/bash 

#SBATCH -J palm_T
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/palmT.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/palmT.err
#SBATCH -c 2
#SBATCH -a 1-9

echo "------------------------------------------------" 
echo "Slurm Job ID: $SLURM_JOB_ID" 
echo "Run on host: "`hostname`
echo "Operating system: "`uname -s`
echo "Username: "`whoami`
echo "Started at: "`date`
echo "------------------------------------------------" 

ml use -a /apps/eb/2020b/skylake/modules/all
module load MATLAB/2021a_Update4

matlab -nojvm -nodisplay -nosplash < /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_palm/stat_02_anova_palm_${SLURM_ARRAY_TASK_ID}.m