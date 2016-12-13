#!/bin/bash

# bearychat svn
# Requires Curl and Subversion Server installed.
# Put this file as "post-commit" with 755 permissions on the hooks directory of your repo

REPO_PATH=$1
REV=$2
LOOK=/usr/bin/svnlook
CURL=/usr/bin/curl

# write your web hook url
URL="https://hook.bearychat.com/=bw9uO/incoming/4db88b3ae9e98735895d234709a7ccb9"

RES=`$LOOK info -r $REV $REPO_PATH`
COMMIT=`echo "$RES" | awk 'BEGIN{RS="\n\n"; FS="\n"} {print $4}'`
USER=`echo "$RES" | awk 'BEGIN{RS="\n\n"; FS="\n"} {print $1}'`
MSG="$REV by $USER: $COMMIT"

JSON="{
	\"text\": \"Subversion\",
	\"attachments\": [
        {
		\"title\": \"Revision\",
		\"text\": \"$REV\",
		\"color\": \"#ffa500\"
		},
		{
		\"title\": \"User\",
		\"text\": \"$USER\",
		\"color\": \"#ffa500\"
		},
		{
		\"title\": \"Changes\",
		\"text\": \"$COMMIT\",
		\"color\": \"#ffa500\"
		}
	]
}"

$CURL -X POST --data "payload=$JSON" $URL
