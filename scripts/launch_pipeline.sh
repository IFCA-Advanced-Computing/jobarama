#!/bin/bash

echo "Job-O-Rama Pipeline"

REALUSER=$1
VAR1=$2
FILE=$3

echo " params: $VAR1 $FILE"

cd /gpfs/res_projects/uc00/joborama

TMPDIR=$(pwd)
JOBFILE=$(mktemp --tmpdir=${TMPDIR} --suffix=.cmd)

cat > ${JOBFILE} <<EOF
#!/bin/bash
#@ job_name = job-o-rama
#@ initialdir = .
#@ output = cache/${REALUSER}/jor_%j.out
#@ error = cache/${REALUSER}/jor_%j.err
#@ total_tasks = 1
#@ wall_clock_limit = 10:00

date

echo running fake with ${VAR1}
hostname
echo Calculating lines/words in file
wc ${FILE}

echo Calculating md5sum in file
md5sum ${FILE}

date

EOF

mnsubmit ${JOBFILE}

rm ${JOBFILE}
