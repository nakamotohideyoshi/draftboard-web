#!/usr/bin/env bash
readonly PG_HBA_CONF="pg_hba.conf"
readonly POSTGRESQL_CONF="postgresql.conf"

readonly PG_HBA_LINE1="host all all 0.0.0.0/0 md5 # VAGRANT"
readonly CONF_FILE_NOT_FOUND1="*** The Postgres pg_hba.conf file was not found!"
readonly CONF_FILE_NOT_FOUND2="*** You need to find that file and make sure it accepts remote connections!" 
readonly CONF_FILE_NOT_FOUND3="*** If pg_hba.conf had been found we would have made sure this line exists: "

readonly POSTGRESQL_LINE1="listen_addresses='*'"

#
####################################################################################
# part 1: modify pg_hba.conf to accept remote connections
####################################################################################

configfile=( $(sudo PGPASSWORD=postgres -u postgres psql -t -P format=unaligned -c 'show hba_file';  ) )
#for (( i=0; i<${#numbers[@]}; i++ )); do echo "${numbers[i]}"; done
#echo

#
# prints the first line of input which should be the pg_hba.conf file, such as:
#     /etc/postgresql/9.3/main/pg_hba.conf
printf "pg_hba.conf filename: 	%s\n" "${configfile[0]}"

#
# if that file cannot be found great! otherwise we have a problem!
#echo "${#configfile[@]}"
echo "-> attempting to modify pg_hba.conf file to allow remote connections (from webservers)"
if [ ${#configfile[@]} == 0 ]; then
	#
	# there was no pg_hba.conf file found - user will have to setup db manually!
	echo "${CONF_FILE_NOT_FOUND1}"
	echo "${CONF_FILE_NOT_FOUND2}"
	echo "${CONF_FILE_NOT_FOUND3}"
	echo "***     ${PG_HBA_LINE1}"

	#
	# we need to exit here
	exit 1

else
	#
	#  1>> FILENAME     #redirect and append stdout to filename
	#echo "steve" 1>> "mytest.txt"
	#lines=( $(sudo grep -ri "# vagrant" /etc/postgresql/9.3/main/pg_hba.conf;  ) )
	lines=( $(sudo grep -ri "${PG_HBA_LINE1}" "${configfile[0]}";  ) )

	#printf "found pg_hba.conf file and lines array len: 	%s\n", "${#lines[@]}"
	if [[ ${#lines[@]} == 0 ]]; then
		#
		# append the PG_HBA_LINE1 to the pg_hba.conf file if it doesnt already have it
		echo "adding this line to pg_hba.conf: 		${PG_HBA_LINE1}"
		echo "${PG_HBA_LINE1}" 1>> "${configfile[0]}"
	fi
fi

#
####################################################################################
# part 2: modify postgresql.conf to listen on '*', which is how part 1 will work
####################################################################################

#
# use the basepath of configfile[0] (which will exist if we get this far in the script)
# vagrant@vagrant-ubuntu-trusty-64:/vagrant$ echo "/etc/postgresql/9.3/main/pg_hba.conf" | sed -e 's/\/[^\/]*$/\//'
# /etc/postgresql/9.3/main/
# vagrant@vagrant-ubuntu-trusty-64:/vagrant$

#
# get the base directory name by lopping off the filename
path=$(echo "${configfile[0]}" | sed -e 's/\/[^\/]*$/\//')
#echo "${path}"

#
# append the postgresql conf file name to the directory name
fullpath="$path$POSTGRESQL_CONF"
#echo $fullpath

#
# edit the postgresql conf to listen on '*'
echo "${POSTGRESQL_LINE1}" 1>> "${fullpath}"
echo "*** Added line to postgresql.conf: ${POSTGRESQL_LINE1}"








