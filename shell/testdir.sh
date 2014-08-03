#!/bin/bash
#name: testdir.sh
#authro: orangleliu
#date: 2014-08-03
#version: v1.0
#function:  check /tmp/lzz write and read authority and chang it's authority

#===================
TestDir="/tmp/lzz"
#===================
#function -> Chenck_Dir()
#===================
Check_Dir()
{
if [ -d "$TestDir" ]		
then 
		TW=`ls -ld /tmp/lzz/|awk '{print $1}'|sed 's/d//g'|grep 'w'|wc -l`
		TR=`ls -ld /tmp/lzz/|awk '{print $1}'|sed 's/d//g'|grep 'r'|wc -l`
		if [ "$TW" -ne 0 -a "$TR" -ne 0 ]
		then 
				echo "$TestDir can writted and readed !"
		else
				echo "$TestDir can not writted and readed !"
				echo -n "Do you add write and rend authority [Y|N]"
				read tt
				case $tt in 
						Y|y)
						chmod 755 $TestDir
								if [ $? -eq 0 ]
								then 
										echo "add write and read authority ok ...."
								else
										echo "add write add read authority fail...."
										return 1
								fi 
						;;
						N|n)
								return 1
						;;
						*)
								echo "error"
								return 1
						;;
				esac 
		fi 
else
		echo "not have this dir"
		return 1
fi 
}

#======================
#function -> Main()
#=====================
Main()
{
Check_Dir
		if [ $? -eq 1 ]
		then 
				exit 1
		fi
}

Main
