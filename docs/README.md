# MacOS local dev setup

All versions were current at the time of this install. Your mileage might vary if you use a different version

# Laptop
Mac OS X El Capitan 10.11.6
2.6 GHz Intel Core i7
16 GB RAM

# VirtualBox
Install [VirtualBox 5.2.16](https://download.virtualbox.org/virtualbox/5.2.16/VirtualBox-5.2.16-123759-OSX.dmg)

# Ubuntu 16.04
Download and install the [Ubuntu 16.04 image](https://www.osboxes.org/ubuntu/)

After downloading, you will have to unpack the image. At the time of this writing the image is zipped in a .z
format and you can use the [The Unarchiver](https://theunarchiver.com/) to unpack the file. This will unpack
the file in a 64bit folder.

Once the file is unpacked, its time to use the image.

# Create new Virtual Machine
In VirtualBox Manager, go to New and then select Expert Mode
Populate the form as follows:
1. Name: `Ubuntu 16.04`
1. Type: `Linux`
1. Version: `Debian (64-bit)`
1. Memory size: `2048`
1. Hard disk: Choose `Use an existing virtual hard disk file`
1. Browse to select the `.vdi` image. The drop down list should populate and say `Ubuntu 16.04 (64bit).vdi (Normal, 500.00 GB)`
1. Click `Create`

# Start the image
In VritualBox Manager, select the image we just created and click Start (or you can double-click on it)
The Image should start in a few seconds
In the prompt you'll be asked to log in, use the following credentials:
Username: `osboxes.org`
Password: `osboxes.org`

The image is pretty bare bones so you'll want to install some software

# Install packages
1. Update package lists
`sudo apt-get -y update`
1. Install git, python, mysql, nginx
`sudo apt-get -y install git python-pip python-dev mysql-server libpq-dev postgresql postgresql-contrib nginx`
1. Install required libraries
`sudo apt-get -y install build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev`
1. Install virtualbox guest
`sudo apt-get -y install virtualbox-guest-dkms`
1. Update software packages
`sudo apt-get -y upgrade`

If you run into `E: Could not get lock var,lib,dpkg,lock - open (11 Resource temporarily ..)`, run this command to delete
some of the locks: `sudo rm /var/lib/dpkg/lock /var/lib/apt/lists/lock /var/cache/apt/archives/lock` 
After clearing the locks, attempt to re-install the packages.

Reference:
https://www.youtube.com/watch?v=OwXt_mKC1Kk

# Fork the repository
Fork https://github.com/vadim1/area

# Create workspace
`mkdir -p ~/git/forks`
`cd ~/git/forks`
`git clone git@github.com:<your userid>/area.git` (replace <your userid>)
`sudo mv ~/git /var/www`
`ln -s /var/www/git ~/git`

This will clone the project in `area` and put the files in /var/www which will make it easier for nginx to access later.

# Set up your upstream and sync your fork with the upstream
`git remote add upstream git@github.com:vadim1/area.git`
`git pull upstream master`
`git push origin master`

# Install freetype2
The app installs matplotlib which requires freetype. This is not available via normal means so we'll have to install it separately
`sudo add-apt-repository ppa:glasen/freetype2`
`sudo apt-get -y update && sudo apt-get -y install freetype2-demos` (freetype2-demos will install the freetype2 libs)
`sudo apt-get -y install libpng-dev libfreetype6-dev`

References:
* http://ubuntuhandbook.org/index.php/2017/06/install-freetype-2-8-in-ubuntu-16-04-17-04/
* https://askubuntu.com/questions/798343/why-wont-python-pip-install-matplotlib-work
* https://github.com/pypa/pip/issues/5240

# Update numpy
The version might no longer be supported. At the time of this writing it was 1.8.0rc1 which no longer exists. The error could
be: `could not find a version that satisfies the requirement numpy==1.8.0rc1`

# Update scipy
Same story as numpy. The version in question was 0.13.0b1. I kept it to be 0.13.0

# Update pyopenssl
pyopenssl < 0.14 will fail to build with newer versions of openssl. The error would be similar to
`OpenSSL/crypto/crl.c::23: error: static declaration of 'X509_REVOKED_dup' follows non-static declaration`

References:
* https://github.com/pyca/pyopenssl/issues/276

# Comment out pyobjc* if not on MacOS

# Install the application requirements
`rm -rf ~/.cache/pip/`
`pip install --force-reinstall -I -r requirements.txt`

References:
* https://github.com/scrapy/scrapy/issues/2115
* https://stackoverflow.com/questions/33669846/forcing-pip-to-recompile-a-previously-installed-package-numpy-after-switchin

# Install django_debug_toolbar
`pip install django_debug_toolbar --user`

# Create the database
```
CREATE DATABASE psp;
GRANT ALL ON psp.* TO pspuser@'localhost' IDENTIFIED BY '<password>';
FLUSH PRIVILEGES;
```

# Update area/settings.py with the database info
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'psp',
        'USER': 'pspuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}
```

# Update the default nginx config
This will configure an nginx server running on port 80 and reverse proxy everything to
the python server which is running on 0.0.0.0:8000.

```
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	server_name _;

	location = /favicon.ico { access_log off; log_not_found off; }

	location /static {
		alias /var/www/git/forks/area/static;
	}

	location / {
		proxy_redirect off;
		proxy_set_header	Host	$host;
		proxy_set_header	X-Real-IP	$remote_addr;
		proxy_set_header	X-Forwarded-For	$proxy_add_x_forwarded_for;
		proxy_pass	http://0.0.0.0:8000/;
	}
}
```

# Run the migration script
```
./manage.py migrate
```

# Run the static assets script
```
./manage.py collecstatic
```

# Start the server
```
./manage.py runserver 0.0.0.0:8000
```
