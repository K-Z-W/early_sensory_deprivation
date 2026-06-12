#!/bin/bash 

#SBATCH -J g5_AOV
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/blindness/serious_2nd/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/blindness/serious_2nd/scps/log/g5_perm.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/blindness/serious_2nd/scps/log/g5_perm.err
#SBATCH -c 1
#SBATCH -a 1-50

echo "------------------------------------------------" 
echo "Slurm Job ID: $SLURM_JOB_ID" 
echo "Run on host: "`hostname`
echo "Operating system: "`uname -s`
echo "Username: "`whoami`
echo "Started at: "`date`
echo "------------------------------------------------" 

source /gpfs3/well/margulies/users/anw410/conts/my_imgs/v_py_env_3-9/v_act.sh

# d=/gpfs3/well/margulies/users/anw410/data/blindness/serious_2nd/stats/angle.npy
# d=/gpfs3/well/margulies/users/anw410/data/blindness/serious_2nd/stats/magni.npy
d=/gpfs3/well/margulies/users/anw410/data/blindness/serious_2nd/stats/g5z.npy

# s=/gpfs3/well/margulies/users/anw410/data/blindness/serious_2nd/stats/perm_th
# s=/gpfs3/well/margulies/users/anw410/data/blindness/serious_2nd/stats/perm_rd
s=/gpfs3/well/margulies/users/anw410/data/blindness/serious_2nd/stats/perm_grad/g5

python /gpfs3/well/margulies/users/anw410/data/blindness/serious_2nd/scps/stat_01_anova.py $d $s 100 g5z ${SLURM_ARRAY_TASK_ID} 