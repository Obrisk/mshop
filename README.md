# Establish development environment under Windows system

## Base

The following software needs to be installed and configured in advance

-[`git`](https://git-scm.com/)-code management tool
-[`nginx`](http://nginx.org/en/download.html)-web server
-[`postgresql`](https://www.postgresql.org/)-Database (It is recommended to install version 10)
-[`node & npm`](https://nodejs.org/en/download/)-npm package management tool
-[`python`](https://www.python.org/downloads/windows/)-It is recommended to install version 3.7.


## PostgreSQL

A database needs to be established to store the data of `camel-store`.

The database used in the document is named `camelstore`, which is owned by user `camelstore`.

> It is recommended to use the application [`pgAdmin`](https://www.pgadmin.org/) to complete the operations of creating new databases and users.

## git

1. Run `git clone https://github.com/gzqichang/camel-store.git --recurse-submodules` to pull this repository locally, remember to add the `--recurse-submodules` parameter.
1. Enter the `camel-store` directory


## nginx

Because `react.js` is used to write the management backend, when debugging admin, `nginx` is needed to distribute static resource requests and api requests.

1. Add the file `camelstore.dev.com.nginx.conf` in the `nginx` configuration folder and write the following:

```
server{
    listen 8080;
    server_name camelstore.dev.com;
    location / {
        proxy_pass $scheme://localhost:8001;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /api/ {
        proxy_pass $scheme://localhost:8000;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
2. Open the `nginx.conf` file with Notepad, and add `include camelstore.dev.com.conf;` in http {} to reference the configuration in the `camelstore.dev.com.conf` file.
3. Use the `nginx -t` command to verify whether the configuration file is correct.
4. Run `nginx` to start nginx, if it is already started, restart `nginx -s reload`.
5. As an administrator, run `echo 127.0.0.1 camelstore.dev.com >> C:\Windows\System32\drivers\etc\hosts` to add the domain name to the hosts file.

    1. You can also open `C:\Windows\System32\drivers\etc\hosts` with Notepad as an administrator, and add a line of configuration `127.0.0.1 camelstore.dev.com` at the end.

## api section

Enter the `api` directory.

1. Run `pip install -U pip setuptools pipenv` to install the upgrade package management tool.

To install various dependencies.

1. Run `pipenv sync` to install the virtual environment.
1. Run `pipenv shell` to enter the virtual environment.
1. Run `django-admin version` to see if it is version 2.2. We currently do not support version 3.0 or higher.

`cd packages` Enter the directory of the dependent package, then enter the `qapi`, `qcache`, `qsmstoken`, and `quser` directories respectively, and run `python setup.py develop` one by one to install the development version.

Next, start configuring the project.

1. `cd conf/settings`
1. `copy local.py.tpl local.py` generates a local configuration environment.
1. Choose your favorite editor, open the `local.py` file, and fill in the `SECRET_KEY` and `DEFAULT_DB` items. Remember to use a random string of dozens of characters in `SECRET_KEY`.
1. Go back to the `api` directory.
1. Run `python manage.py migrate` to create various data tables, and then run
    1. `python manage.py init_staff` creates initial user data
    1. `python manage.py format_groups` to create initial grouping data
    1. `python manage.py updateconfig` to modify the configuration, see the help for related parameters.
    1. `python manage.py wechatconfig` to modify the configuration, see the help for related parameters.
    1. `python manage.py changepassword admin` to modify the password of the previously generated admin account.
1. Run `python manage.py runserver` to run it and see.
    1. Open the browser and visit `http://localhost:8000/api/sitemap/`, if you can see the rest-framework interface, it means that the api is running normally.
    1. Visit again `http://camelstore.dev.com:8080/api/sitemap/`, theoretically, you should be able to see the same page. If it cannot be accessed, it may be that the listening port of `nginx` is not 8080.

The third-party configuration is also in the `local.py` file, see [third-party-config.md) for details.

## admin section

Enter the `admin` directory.

1. Run `npm install` to install the modules that the project depends on. Depending on the network situation, it may take a while.
1. Run `npm start` to run admin,
1. Open the browser, visit `http://camelstore.dev.com:8080/`, you should see the login interface of admin, enter the account password, you can successfully log in.

## wxapp section

Enter the `wxapp` directory.

1. Run `npm install` to install the modules that the project depends on. Depending on the network situation, it may take a while.
1. Run `npm i -g wepy-cli` to arrange scaffolding.
1. Run `npm run build` to compile the `wpy` file.
1. Open the project with `WeChat Developer Tools` (in the `camel-store\wxapp\dist` directory), you can see the applet interface in the simulator.

The default data interface is `http://camelstore.dev.com:8080`, you can find the following statement in the file `src/service/index.js`
```
export const baseUrl ='http://camelstore.dev.com:8080';
```
Modify the value of `baseUrl` to access other interfaces.


At this point, the development environment has been established.



# Deploy under Ubuntu18
## 1. Basic installation
#### 1.1 Update the software source of ubuntu
New ubuntu virtual machine users may need to first replace the source files in `/etc/apt/sources.list` with domestic mirror sources
```
$ sudo apt-get update // Update the installation source (Source)
$ sudo apt-get upgrade // Update installed packages
$ sudo apt-get dist-upgrade // Update installed packages (identify and handle changes in dependencies)
```
#### 1.2 Install database postgresql
Need to build a database to store the data of `camel-store`.
The name of the database agreed in the document is `camelstore`, which is owned by the user `camelstore`.
```
# Install postgresql
$ sudo apt-get install postgresql

# Create database
$ sudo -u postgres psql
# Modify the password of the postgres user
postgres=# ALTER USER postgres WITH PASSWORD'POSTGRES_PASSWORD';

# Create this project's database and its owner
postgres=# create user camelstore with password'YOUR_PASSWORD';
CREATE ROLE
postgres=# create database camelstore owner camelstore;
CREATE DATABASE
```
#### 1.3 Python
`camel-store` requires at least Python 3.6 or higher. Currently 3.6/3.7 are more commonly used. It is recommended to use `pyenv` for python version management, use `pyenv-virtualenv` to create the corresponding virtual environment, use ` pipenv` manages the virtual environment.
Take 3.7.4 as an example here.
```
# Install pyenv
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
$ echo'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
$ echo'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
$ echo'eval "$(pyenv init -)"' >> ~/.bash_profile
$ source .bash_profile

# Install pyenv-virtualenv
$ git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
$ echo'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
$ source .bash_profile

# Some dependency packages that need to be installed before installing python
$ sudo apt-get install libc6-dev gcc
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm

# Install python 3.7.4
$ pyenv install 3.7.4

# Create a virtual environment
$ pyenv virtualenv 3.7.4 camel-store

# At this point, through the command pyenv versions, you should be able to see the downloaded python version and the virtual environment created based on this version

# Install pipenv
$ sudo pip install pipenv
# If you cannot download due to network reasons, you can use domestic sources such as:
$ sudo pip install pipenv -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 2. Project code
#### 2.1 Pull code through git
```
# Install git
$ sudo apt-get install git
```
It is recommended to run `git clone https://github.com/gzqichang/camel-store.git --recurse-submodules` under the directory `/home/ubuntu/project/camel-store/` to pull this repository locally , Remember to add the `--recurse-submodules` parameter.

#### 2.2 Make the project automatically activate the virtual environment
Create the file `.python-version` in the `/home/ubuntu/project/camel-store/` directory, and write the virtual environment name camel-store created in step 1.3 in the file. Whenever you enter this directory, you should be able to automatically activate the virtual environment.

#### 2.3 api section
Enter the api directory.
1. Install dependent libraries:
    1. Run `pipenv sync` to install the virtual environment.
    2. Run `django-admin --version` to check whether the current django version is version 2.2. The project does not yet support django 3.0 and above.
2. Install the local dependency library:
    `cd packages` Enter the directory of dependent packages, and then enter the qapi, qcache, qsmstoken, and quser directories respectively, and run `python3 setup.py develop` one by one to install the development version.
3. Start configuring the project:
    1. `cd conf/settings`
    2. `cp local.py.tpl local.py` generates local configuration environment.
    3. Choose your favorite editor, open the `local.py` file, and fill in the `SECRET_KEY` and `DEFAULT_DB` items. Remember to use a random string of dozens of characters in `SECRET_KEY`.
    4. Go back to the `api` directory.
    5. Run `python3 manage.py check` to test whether there is a problem with the code
    6. Run `python3 manage.py migrate` to create various data tables, and then run
        1. `python3 manage.py init_staff` creates initial user data
        2. `python3 manage.py format_groups` to create initial grouping data
        3. `python3 manage.py updateconfig` to modify the configuration, see the help for related parameters.
        4. `python3 manage.py wechatconfig` Modify the configuration, see the help for related parameters.
        5. `python3 manage.py changepassword admin` to modify the password of the previously generated admin account.
        6. Run `python3 manage.py runserver`, and the program should be able to run.
4. The third-party configuration is also in the `local.py` file, see [third-party-config.md) for details.

#### 2.4 admin section
1. Install the software
```
# Install node.js and npm
$ sudo apt-get install nodejs-legacy
$ sudo apt-get install npm
# Install the module used to manage the version of node.js n
$ sudo npm install -g n
# Install the latest version of node.js through the n module
$ sudo n latest
# Upgrade npm to the latest version
$ sudo npm install npm@latest -g
# View version
$ sudo node -v
$ sudo npm -v
```
2. Enter the admin directory.
    1. Run `npm install` to install the modules that the project depends on. Depending on the network situation, it may take a while.
    2. Run `npm run build`

#### 2.5 Deployment file
###### 2.5.1 Create a configuration file
Create a folder deploy under the `/home/ubuntu/project/camel-store/` directory, and place 3 files `nginx.conf`, `supervisor.conf`, `uwsgi.ini` under the deploy directory.

If the file directory is inconsistent with the document project directory, you need to modify the path by yourself.
The server_name in the nginx.conf file needs to fill in your own SERVER_NAME or HOST.

###### 2.5.2 Soft connection configuration file
This is not to cover the original nginx.conf and supervisor.conf
The naming here is only for the convenience of judging the specific configuration file
```
$ sudo ln -s /home/ubuntu/camel-store/deploy/nginx.conf /etc/nginx/sites-enabled/camel-store.conf
$ sudo ln -s /home/ubuntu/camel-store/deploy/supervisor.conf /etc/supervisor/conf.d/camel-store.conf
```
###### 2.5.3 Start nginx
```
# Install nginx
$ sudo apt-get install nginx
```
1. Run `nginx -t` to verify that the configuration file is correct.
2. Run `sudo service nginx start` to start nginx, if it is already started, to restart nginx, run `sudo nginx -s reload`

###### 2.5.4 Verify uwsgi
Run `uwsgi --ini uwsgi.ini` in the deploy directory. If it runs normally, you can exit with ctrl+c.

###### 2.5.5 Start supervisor
Use supervisor to manage uwsgi process.
```
# Install supervisor
$ sudo apt-get install supervisor
```
Run `sudo supervisorctl reload`

****
At this point, the deployment is basically completed in the ubuntu environment.
