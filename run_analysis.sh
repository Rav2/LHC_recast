#!/bin/bash

echo "#--- Start of run_analysis.sh ---#"
wdir=`pwd`
analysis_main=$wdir'/analyses/analysis_main.py'

tag=`echo $1 | sed -e "s/\.lhco//"`
lhco_path=$wdir/result/$tag.lhco
eff_out=$wdir/result/$tag.eff

if [[ -e $eff_out ]]; then
    rm -f $eff_out
fi

python $analysis_main $lhco_path | tee $eff_out
ls -ltr $eff_out

echo "#--- End of run_analysis.sh ---#"
