#!/bin/bash 

#SBATCH -J th_rd_tfce
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/wd
#SBATCH -p long
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/th_rd_tfce.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/th_rd_tfce.err
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

da=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/angle_reg.npy
db=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/angle_reg_unconstrained.npy
dc=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/magni_reg.npy
dd=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/magni_reg_unconstrained.npy

# d1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/G1.npy
# d2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/G2.npy
# d3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/G3.npy

# d1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/fcz1.npy
# d2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/fcz2.npy
# d3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/fcz3.npy
# d4=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/fcz4.npy

sa=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm_tfce/th/reg
sb=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm_tfce/th_reg_unc
sc=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm_tfce/rd/reg
sd=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm_tfce/rd/reg_unc

# s1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_grad/g1
# s2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_grad/g2
# s3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_grad/g3

# s1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_fc/fc1
# s2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_fc/fc2
# s3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_fc/fc3
# s4=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_fc/fc4

python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_03_anova_tfce.py $da $sa 100 angle_reg ${SLURM_ARRAY_TASK_ID} 
python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_03_anova_tfce.py $db $sb 100 angle_reg_unc ${SLURM_ARRAY_TASK_ID} 
python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_03_anova_tfce.py $dc $sc 100 magni_reg ${SLURM_ARRAY_TASK_ID} 
python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_03_anova_tfce.py $dd $sd 100 magni_reg_unc ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d1 $s1 100 g1z ${SLURM_ARRAY_TASK_ID}
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d2 $s2 100 g2z ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d3 $s3 100 g3z ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d1 $s1 100 fc1z ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d2 $s2 100 fc2z ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d3 $s3 100 fc3z ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d4 $s4 100 fc4z ${SLURM_ARRAY_TASK_ID} 