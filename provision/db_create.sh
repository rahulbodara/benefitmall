#!/usr/bin/env bash
# RUN sudo -E bash provision/db_create.sh

BOLD="\033[1m"
GREEN="\033[92m"
END="\033[0m"

echo -e "${BOLD}${GREEN}Creating database: ${PROJECT_NAME}${END}"
cat << EOF | su - postgres -c psql
-- Create the database:
CREATE DATABASE $PROJECT_NAME WITH OWNER=$DB_USER
									LC_COLLATE='en_US.utf8'
									LC_CTYPE='en_US.utf8'
									ENCODING='UTF8'
									TEMPLATE=template0;

EOF