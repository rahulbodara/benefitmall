[![Requirements Status](https://requires.io/bitbucket/insite_team/benefitmall/requirements.svg?branch=master)](https://requires.io/bitbucket/insite_team/benefitmall/requirements/?branch=master)

# Initial set up of local dev environment #

### 1 - Pull from source control ###

*Pull site from git*

*Connect heroku git:*

```
heroku git:remote --app benefitmall
```


### 2 - Stand up virtual machine ###

*On the command line, in the working folder, type:*

```
vagrant up
```
*NOTE: Errors showing at the end of this process may simply be due to difference between the code and the initial database that was just set up. You can safely ignore these and move on to the next part.*

### 3 - Remote into virtual machine ###

*On the command line, in the working folder, type:*

```
vagrant ssh
```

### 4 - Pull in database and uploaded files ###

*On the command line, on your local machine, type:*

```
heroku pg:backups:capture
heroku pg:backups:download
```

*On the command line, in the virtual machine, type:*

```
python manage.py restore_db
python manage.py restore_media
python manage.py migrate
```

# Run local server #

*If the virtual machine is not currently running, type the following on the command line, in the working directory:*

```
vagrant up
```
*If you are not currently remoted into the virtul machine, type:*
```
vagrant ssh
```

*To run the web server on http://localhost:8000, on the command line, in the virtual machine, type:*

```
python manage.py run
```

# Stop local server #

*On the command line, in the working directory, type:*

```
vagrant halt
```


