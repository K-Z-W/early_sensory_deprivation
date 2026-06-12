#!/bin/bash 

#SBATCH -D /well/margulies/users/anw410/data/blindness/dataset_4/scps/wd
#SBATCH -p short
#SBATCH -o /well/margulies/users/anw410/data/blindness/dataset_4/scps/logs/gcca_output.out 
#SBATCH -e /well/margulies/users/anw410/data/blindness/dataset_4/scps/logs/gcca_error.err 
#SBATCH -c 4

ml use -a /apps/eb/2020b/skylake/modules/all
module load Python/3.9.5-GCCcore-10.3.0
source /well/margulies/users/anw410/conts/my_imgs/v_py_env_3-9/neurolab-${MODULE_CPU_TYPE}/bin/activate

python /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/posproc_02_gcca.py