#!/bin/bash 

#SBATCH -J deaf_tfce
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/Deafness/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/tfce_deaf.out  
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/tfce_deaf.err  
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

da=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/hsv/sm6_th_ind_${typ2}.npy
db=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/hsv/sm6_rd_ind_${typ2}.npy

sa=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_tfce/angle/param
sb=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_tfce/angle/non_param
sc=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm_tfce/magni/param
#sd=/gpfs3/well/margulies/users/anw410/data/${typ1}/stat/perm/magni/non_param

python /gpfs3/well/margulies/users/anw410/data/${typ1}/scps/stat_02_comparison_tfce.py $da $sa 100 angle parametric ${SLURM_ARRAY_TASK_ID} 
python /gpfs3/well/margulies/users/anw410/data/${typ1}/scps/stat_02_comparison_tfce.py $da $sb 100 angle nonparametric ${SLURM_ARRAY_TASK_ID} 
python /gpfs3/well/margulies/users/anw410/data/${typ1}/scps/stat_02_comparison_tfce.py $db $sc 100 magni parametric ${SLURM_ARRAY_TASK_ID} 
#python /gpfs3/well/margulies/users/anw410/data/${typ1}/scps/stat_01_two-sample-comparison.py $db $sd 100 magni nonparametric ${SLURM_ARRAY_TASK_ID} 