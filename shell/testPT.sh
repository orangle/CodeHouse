#!/bin/bash
#title: testPT.sh
#atuhor: orangleliu
#date: 2014-08-08
#desc: 输入2个参数，第二个位数字，如果正确就打印出来

#=====================
#Function  Check
#=====================
Check()
{
if [ $# -ne 2 ]   #charge params num
then 
	echo "You must input two params"
	return 1
else
	all="$@" #get all input value
	secd=`echo $all|awk '{print $2}'`
	expr 1 + $secd > /dev/null 2>&1
	if [ $? -eq 0 ]
	then 
		echo "$all"
	else
		echo "Sorry age is a number" 
		return 1
	fi
fi
}

#===================
#Function main()
#==================
Main()
{
Check $1 $2
	if [ $? -eq 1 ]
	then 
		exit
	fi
}

Main $1 $2
