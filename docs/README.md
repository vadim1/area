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
`sudo apt-get -y update`
`sudo apt-get -y install git python-pip python-dev libpq-dev postgresql postgresql-contrib nginx`
`sudo apt-get -y install build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev`
`sudo apt-get -y upgrade`

If you run into `E: Could not get lock var,lib,dpkg,lock - open (11 Resource temporarily ..)`, run this command to delete
some of the locks: `sudo rm /var/lib/dpkg/lock /var/lib/apt/lists/lock /var/cache/apt/archives/lock` (ref: https://www.youtube.com/watch?v=OwXt_mKC1Kk)

After clearing the locks, attempt to re-install the packages

# Fork the repository
Fork https://github.com/vadim1/area

# Create workspace
`mkdir -p ~/git/forks`
`cd ~/git/forks`
`git clone https://github.com/<your userid>/area.git` (replace <your userid>)

This will clone the project in `area`

# Install freetype2
The app installs matplotlib which requires freetype. This is not available via normal means so we'll have to install it separately
`sudo add-apt-repository ppa:glasen/freetype2`
`sudo apt-get -y update && sudo apt-get -y install freetype2-demos` (freetype2-demos will install the freetype2 libs)
`sudo apt-get -y install libpng-dev libfreetype6-dev`

ref: http://ubuntuhandbook.org/index.php/2017/06/install-freetype-2-8-in-ubuntu-16-04-17-04/
ref: https://askubuntu.com/questions/798343/why-wont-python-pip-install-matplotlib-work
ref: https://github.com/pypa/pip/issues/5240

# Update numpy
The version might no longer be supported. At the time of this writing it was 1.8.0rc1 which no longer exists. The error could
be: `could not find a version that satisfies the requirement numpy==1.8.0rc1`

# Update scipy
Same story as numpy. The version in question was 0.13.0b1. I kept it to be 0.13.0

# Update pyopenssl
pyopenssl < 0.14 will fail to build with newer versions of openssl. The error would be similar to
`OpenSSL/crypto/crl.c::23: error: static declaration of 'X509_REVOKED_dup' follows non-static declaration`

ref: https://github.com/pyca/pyopenssl/issues/276

# Comment out pyobjc* if not on MacOS


# Install the application requirements
`rm -rf ~/.cache/pip/`
`pip install --force-reinstall -I -r requirements.txt`

ref: https://github.com/scrapy/scrapy/issues/2115
ref: https://stackoverflow.com/questions/33669846/forcing-pip-to-recompile-a-previously-installed-package-numpy-after-switchin
