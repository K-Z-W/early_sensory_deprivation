#!/bin/bash 

#SBATCH -J deaf_perm
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/Deafness/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/perm_deaf.out  
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/perm_deaf.err  
#SBATCH -c 1
#SBATCH -a 1-50

echo "------------------------------------------------" 
echo "Slurm Job ID: $SLURM_JOB_ID" 
echo "Run on host: "`hostname`
echo "Operating system: "`uname -s`
echo "Username: "`whoami`
echo "Started at: "`date`
echo "------------------------------------------------" 

ml use -a /apps/eb/2020b/skylake/modules/all
source /gpfs3/well/margulies/users/anw410/conts/my_imgs/v_py_env_3-9/v_act.sh

typ1=Deafness
typ2=deaf

# d1=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/stat_clean/th_ind_${typ2}_clean-sm6.npy
# d2=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/stat_clean/rd_ind_${typ2}_clean-sm6.npy

# da=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/stat_clean/g1z_clean-sm6.npy
# db=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/stat_clean/g2z_clean-sm6.npy
# dc=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/stat_clean/g3z_clean-sm6.npy

d3=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/stat_clean/fc_based-on-th_seed-01.npy
d4=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/stat_clean/fc_based-on-th_seed-02.npy
d5=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/stat_clean/fc_based-on-th_seed-03.npy

# s1a=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_clean/th_param
# s1b=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_clean/th_nonparam
# s2a=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_clean/rd
# s2b=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_clean/magni/non_param

# sa=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_clean/grad/g1
# sb=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_clean/grad/g2
# sc=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_clean/grad/g3

s3=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_clean/fc/fc1
s4=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_clean/fc/fc2
s5=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_clean/fc/fc3

# python /gpfs3/well/margulies/users/anw410/data/${typ1}/scps/stat_01_comparison.py $d1 $s1a 100 angle parametric ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/${typ1}/scps/stat_01_comparison.py $d1 $s1b 100 angle nonparametric ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/${typ1}/scps/stat_01_comparison.py $d2 $s2a 100 magni parametric ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/${typ1}/scps/stat_01_comparison.py $db $sd 100 magni nonparametric ${SLURM_ARRAY_TASK_ID} 

python /gpfs3/well/margulies/users/anw410/data/${typ1}/scps/stat_01_comparison.py $d3 $s3 100 fc1z parametric ${SLURM_ARRAY_TASK_ID} 
python /gpfs3/well/margulies/users/anw410/data/${typ1}/scps/stat_01_comparison.py $d4 $s4 100 fc2z parametric ${SLURM_ARRAY_TASK_ID} 
python /gpfs3/well/margulies/users/anw410/data/${typ1}/scps/stat_01_comparison.py $d5 $s5 100 fc3z parametric ${SLURM_ARRAY_TASK_ID} 