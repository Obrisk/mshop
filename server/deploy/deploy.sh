#Auto deploy Nodejs and other packages to prod

curl -sL https://deb.nodesource.com/setup_14.x -o nodesource_setup.sh

sudo bash nodesource_setup.sh

sudo apt install -y nodejs

sudo apt install -y build-essential mysql-server nginx




sudo update-alternatives --set editor /usr/bin/vim.basic

ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N "" -C "$1"


eval "$(ssh-agent -s)"

ssh-add -k ~/.ssh/id_rsa

RSA_KEY=$(cat ~/.ssh/id_rsa.pub)

#More https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

#Sometimes pasting these lines to other editors destroy the spacing encoding and the bash will fail to parse spaces
curl -H "Authorization: token $1" --data '{"title":"EC2-instance-'"$3"'-ID'"$RANDOM"'","key":"'"$RSA_KEY"'"}' https://api.github.com/user/keys

git clone --depth 1 git@github.com:$2/$3.git


sudo npm install nrm -g

nrm use taobao

sudo npm install pm2@latest -g

sudo npm i

pm2 startOrGracefulReload ~/mshop/server/pm2.json

pm2 startup systemd

$(!! 2>&1 >/dev/null | grep 'sudo env')


#sudo mysql
#CREATE DATABASE $3 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;


sudo mysql -u username -p $3 < /home/ubuntu/server/hiolabsDB.sql

sudo cp ~/livejs/nginx.conf /etc/nginx/sites-available/$4

sudo nginx -t && sudo systemctl restart nginx


sudo apt-get update
sudo apt-get install python3-certbot-nginx -y
sudo certbot --noninteractive --agree-tos -d $4.$5 -d www.$4.$5 --register-unsafely-without-email --nginx

