#!/bin/bash 

typ=Deafness
dir_outp=/gpfs3/well/margulies/users/anw410/data/${typ}/scps/wd
dir_data=/gpfs3/well/margulies/users/anw410/data/${typ}/bids
dir_fast=/gpfs3/well/margulies/users/anw410/data/${typ}/T1_fast

for s in $(seq 60)
do
    if [ ${s} -lt 10 ]; then sjname=sub-0${s}; else sjname=sub-${s}; fi
    echo ${sjname}
    #mv ${dir_outp}/${sjname}* ${dir_fast}/${sjname}/
    #cp ${dir_fast}/${sjname}/${sjname}_T1w_fast_restore.nii.gz ${dir_data}/${sjname}/anat/
    #mv ${dir_data}/${sjname}/anat/${sjname}_T1w.json ${dir_data}/${sjname}/anat/${sjname}_T1w_fast_restore.json
    mv ${dir_data}/${sjname}/anat/${sjname}_T1w_fast_restore.json ${dir_data}/${sjname}/anat/${sjname}_T1w.json
    mv ${dir_data}/${sjname}/anat/${sjname}_T1w_fast_restore.nii.gz ${dir_data}/${sjname}/anat/${sjname}_T1w.nii.gz
done