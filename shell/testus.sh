#!/bin/bash
#title: testus.sh
#author: orangleliu
#date: 2014-08-09
#desc: get current user, if it is root user, tell us it is super user or tell us is a common user

#================
#Function CheckUser
#================

CheckUser()
{
	check_user=`whoami`
	if [ "$check_user" == "root" ]
	then 
		echo "You are $check_user user"
		echo "You are a super amdin"
	else
		echo "You are $check_user user"
		echo "You are a common user"
	fi
}
#================
#Function Main
#================
Main()
{
	CheckUser
}

Main

