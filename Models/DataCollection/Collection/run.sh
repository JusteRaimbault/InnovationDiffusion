
cd $HOME/ComplexSystems/InnovationDiffusion/Models/DataCollection/Collection

#echo `which python`
PYTHON=$HOME/anaconda3/bin/python
#SCRIPT=collect.py
SCRIPT=parse.py

RUNNING=`ps -ef | grep "python $SCRIPT" | grep -v "grep" | wc -l`
#echo $RUNNING
TASKS=`cat conf/parameters.csv | grep nruns | awk -F";" '{print $2}'`
#echo $TASKS
TORUN=$((TASKS - RUNNING))
echo $TORUN

for i in `seq 1 $TORUN`
do
    echo "run $i"
    $PYTHON $SCRIPT & disown
done


