#!/usr/bin/env bash
# RUN sudo -E bash provision/db_dropcreate.sh

BOLD="\033[1m"
RED="\033[91m"
END="\033[0m"

echo -e "${BOLD}${RED}Dropping database: ${PROJECT_NAME}${END}"
cat << EOF | su - postgres -c psql
-- Drop the Database
DROP DATABASE $PROJECT_NAME;
EOF

source provision/db_create.sh