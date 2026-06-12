#!/bin/bash 

#SBATCH -J clean
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/Deafness/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/clean.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/clean.err 
#SBATCH -c 4

ml use -a /apps/eb/2020b/skylake/modules/all
module load Python/3.9.5-GCCcore-10.3.0
source /well/margulies/users/anw410/conts/my_imgs/v_py_env_3-9/neurolab-${MODULE_CPU_TYPE}/bin/activate

python /gpfs3/well/margulies/users/anw410/data/Deafness/scps/postproc_00_clean.py
python /gpfs3/well/margulies/users/anw410/data/Synesthesia/scps/postproc_00_clean.py