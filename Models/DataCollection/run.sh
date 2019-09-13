
cd /home/juste/ComplexSystems/InnovationDiffusion/Models/DataProcessing/DataCollection

#echo `which python`
PYTHON=/home/juste/anaconda3/bin/python
SCRIPT=collect.py

RUNNING=`ps -ef | grep "python $SCRIPT" | grep -v "grep" | wc -l`
#echo $RUNNING
TASKS=`cat ../conf/parameters.csv | grep nruns | awk -F";" '{print $2}'`
#echo $TASKS
TORUN=$((TASKS - RUNNING))
echo $TORUN

for i in `seq 1 $TORUN`
do
    echo "run $i"
    $PYTHON $SCRIPT & disown
done


