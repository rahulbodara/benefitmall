#-------------------------------------------------------------
# CONFIGS
#-------------------------------------------------------------

PROJECT_NAME="stack_theme"
BASE_DIR="/home/vagrant"
PROJECT_DIR="${BASE_DIR}/${PROJECT_NAME}"
REQS_DIR="${PROJECT_DIR}/provision/requirements/base.txt"
VIRTUALENV_DIR="${BASE_DIR}/.virtualenvs"

DB_NAME=$PROJECT_NAME
DB_USER="admin"
DB_PASS="!c0ntr1but3"
OS_USER="vagrant"

PYTHON_3="/usr/bin/python3"

SOFTWARE=(
    "python-pip"
    "expect"
    "python3-dev"
    "postgresql-12"
    "libpq-dev"
     )
LOG_COLOR="\e[1;36m"

#-------------------------------------------------------------
# UTILITIES
#-------------------------------------------------------------
#    SUMMARY:  Logging Utility
#    EXAMPLE:  logit "This is a console log"
#    PARAMETERS:
#       MSG - enter a string that you want logit to log
logit () {
    echo -e "${LOG_COLOR} $1"
}

#-------------------------------------------------------------
# INSTALL SOFTWARE
#-------------------------------------------------------------
# Update to postgres 12
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | sudo tee  /etc/apt/sources.list.d/PostgreSQL.list
#
#
#wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
#echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" | sudo tee -a /etc/apt/sources.list.d/PostgreSQL.list

# INFO: update ubuntu
logit "Updating Ubuntu"
sudo apt-get update
# sudo apt-get upgrade

# install software
for i in "${SOFTWARE[@]}"
do
   logit "Installing $i"
   sudo apt-get install -y $i
done

logit "Installing openjdk-8..."
sudo apt-get -y install openjdk-7-jdk

logit "Installing Elastic Search..."
wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
sudo apt-get update && sudo apt-get install elasticsearch
sudo update-rc.d elasticsearch defaults 95 10
sudo /etc/init.d/elasticsearch start

# INFO: install virtualenvwrapper
logit "Installing virtualenvwrapper"
sudo pip install virtualenvwrapper

#-------------------------------------------------------------
# CONFIGURE VIRTUALENVWRAPPER
#-------------------------------------------------------------

# INFO: configuring .profile
logit "configuring .profile"
sed -i "10i # virtualenvwrapper configuration" /home/vagrant/.profile
sed -i "11i export WORKON_HOME=/home/vagrant/.virtualenvs" /home/vagrant/.profile
sed -i "12i source /usr/local/bin/virtualenvwrapper.sh" /home/vagrant/.profile
sed -i "13i export PROJECT_NAME=${PROJECT_NAME}" /home/vagrant/.profile
sed -i "14i export PROJECT_DIR=${PROJECT_DIR}" /home/vagrant/.profile
sed -i "15i export REQS_DIR=${REQS_DIR}" /home/vagrant/.profile
sed -i "16i export VIRTUALENV_DIR=${VIRTUALENV_DIR}" /home/vagrant/.profile
sed -i "17i export DB_NAME=${DB_NAME}" /home/vagrant/.profile
sed -i "18i export DB_USER=${DB_USER}" /home/vagrant/.profile
sed -i "19i export DB_PASS=${DB_PASS}" /home/vagrant/.profile
sed -i "20i export OS_USER=${OS_USER}" /home/vagrant/.profile

# INFO: relaod .profile
logit "Reloading .profile"
source /home/vagrant/.profile


#-------------------------------------------------------------
# SETUP DATABASE
#-------------------------------------------------------------

# setup database
logit "setting up project database"
expect ${PROJECT_DIR}/provision/expects/set_db.exp ${DB_NAME} ${DB_USER} ${DB_PASS} ${OS_USER}


#-------------------------------------------------------------
# CREATE VIRTUAL ENVIRONMENTS
#-------------------------------------------------------------

# INFO: initialize virtualenvironment - Python 3
logit "Creating ${PROJECT_NAME} Python 3 virtual environment..."
mkvirtualenv -r ${REQS_DIR} --python=${PYTHON_3} ${PROJECT_NAME}3

# setup the python path and django_settings_module
logit "Configuring postactivate hook for virtualenv..."
cat << EOF >> ${VIRTUALENV_DIR}/postactivate
    # django settings
    export PYTHONPATH="$PYTHONPATH:${PROJECT_DIR}"
    export DJANGO_SETTINGS_MODULE="config.settings.dev"
EOF

# remove django_settings_module when user deactivate virtualenv
logit "Configuring postdeactivate hook for virtualenv..."
cat << EOF >> ${VIRTUALENV_DIR}/postdeactivate
    # unset project environment variables
    unset DJANGO_SETTINGS_MODULE
EOF

#-------------------------------------------------------------
# DJANGO SETUP
#-------------------------------------------------------------

# INFO: activate virtualenv
logit "Activate virtual environment"
source ${VIRTUALENV_DIR}/${PROJECT_NAME}3/bin/activate

# INFO: move into django project
logit "Changing ${PROJECT_NAME} folder"
cd ${PROJECT_NAME}

# INFO: log user into virtualenv when they ssh into VM
logit "Configuring .bashrc"
cat << EOF >> /home/vagrant/.bashrc
    # login to virtualenv
    workon ${PROJECT_NAME}3
    # project directory
    cd ${PROJECT_DIR}
    export PYTHONDONTWRITEBYTECODE=1
EOF

# INFO: move into django project
logit "Changing to ${PROJECT_NAME} directory"
cd ${PROJECT_DIR}

logit "Initial data load..."
python manage.py load_initial_data

logit "provisioning complete"
