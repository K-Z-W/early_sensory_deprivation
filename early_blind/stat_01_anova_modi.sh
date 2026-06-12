#!/bin/bash 

#SBATCH -J rd_perm_AOV
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/wd
#SBATCH -p long
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/rd_perm.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/rd_perm.err
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

# d=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/angle.npy
# d=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/magni.npy
# da=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/angle.npy
# db=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/magni.npy
# da=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/angle_reg.npy
# db=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/angle_reg_unconstrained.npy
da=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/magni_reg.npy
db=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/magni_reg_unconstrained.npy

# d1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/g1z.npy
# d2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/g2z.npy
# d3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/g3z.npy
# d4=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/g4z.npy
# d5=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/g5z.npy
# d1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/G1.npy
# d2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/G2.npy
# d3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/G3.npy

# d1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/fcz1_combLR.npy
# d2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/fcz2_combLR.npy
# d3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/fcz3_combLR.npy
# d4=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/fcz1_try.npy
# d5=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/fcz2_try.npy
# d6=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/470vls_noFIX/fcz3_try.npy
# d1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/fcz1.npy
# d2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/fcz2.npy
# d3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/fcz3.npy
# d4=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/fcz4.npy

# s=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_th
# s=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_rd
# sa=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_th
# sb=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_rd
# sa=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_reg_th
# sb=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_reg_unconstrained_th
sa=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_reg_rd
sb=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_reg_unconstrained_rd

# s1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_grad/g1
# s2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_grad/g2
# s3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_grad/g3
# s4=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_grad/g4
# s5=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_grad/g5
# s1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_grad/g1
# s2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_grad/g2
# s3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_grad/g3

# s1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_fc_combLR/fc1
# s2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_fc_combLR/fc2
# s3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_fc_combLR/fc3
# s4=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_fc_try/fc1
# s5=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_fc_try/fc2
# s6=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_fc_try/fc3
# s1=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_fc/fc1
# s2=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_fc/fc2
# s3=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_fc/fc3
# s4=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/perm/perm_6grps_fc/fc4

python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $da $sa 100 magni ${SLURM_ARRAY_TASK_ID} 
python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $db $sb 100 magni ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d1 $s1 100 g1z ${SLURM_ARRAY_TASK_ID}
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d2 $s2 100 g2z ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d3 $s3 100 g3z ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d1 $s1 100 fc1z ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d2 $s2 100 fc2z ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d3 $s3 100 fc3z ${SLURM_ARRAY_TASK_ID} 
# python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/stat_01_anova_modi.py $d4 $s4 100 fc4z ${SLURM_ARRAY_TASK_ID} 