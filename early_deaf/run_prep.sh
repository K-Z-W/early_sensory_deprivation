#!/bin/bash 

#SBATCH -J p3rd_deaf
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/Deafness/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/p3rd_deaf.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/p3rd_deaf.err 
#SBATCH -c 2
#SBATCH -a 18,53

echo "------------------------------------------------" 
echo "Slurm Job ID: $SLURM_JOB_ID" 
echo "Run on host: "`hostname`
echo "Operating system: "`uname -s`
echo "Username: "`whoami`
echo "Started at: "`date`
echo "------------------------------------------------" 

if [ ${SLURM_ARRAY_TASK_ID} -lt 10 ]; then sjname=sub-0${SLURM_ARRAY_TASK_ID}; else sjname=sub-${SLURM_ARRAY_TASK_ID}; fi

img_prep=/gpfs3/well/margulies/users/anw410/conts/my_imgs/fmriprep_v24.1.1.simg
dir_data=/gpfs3/well/margulies/users/anw410/data/Deafness/bids
dir_outp=/gpfs3/well/margulies/users/anw410/data/Deafness/output
dir_work=/gpfs3/well/margulies/users/anw410/data/Deafness/wd
lis_surf=/gpfs3/well/margulies/users/anw410/conts/tryout/license.txt
dir_temp=/gpfs3/well/margulies/users/anw410/conts/my_imgs/template
#dir_temp=/gpfs3/well/margulies/users/anw410/data/Deafness/scps/template/${sjname}
#mkdir -p ${dir_temp}

export SINGULARITYENV_TEMPLATEFLOW_HOME=/home/fmriprep/.cache/templateflow

singularity run --cleanenv --writable-tmpfs --containall \
    -B ${dir_data}:/bids \
    -B ${dir_outp}:/out \
    -B ${dir_work}:/tmp \
    -B ${lis_surf}:/opt/licence.txt \
    -B ${dir_temp}:/opt/templateflow \
    ${img_prep} /bids /out participant -w /tmp \
    --participant-label ${sjname} \
    --skip_bids_validation \
    --dummy-scans 5 \
    --cifti-output 91k \
    --fs-license-file /opt/licence.txt \
    --me-t2s-fit-method curvefit 