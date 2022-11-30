# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision "shell",
    inline: 'sudo apt-get update -qy&&sudo apt-get install mininet -qy&&sudo sed -i "s/\(security\.ubuntu\.com\|mirrors\.kernel\.org\)/old-releases\.ubuntu\.com/g" /etc/apt/sources.list&&sudo apt-get install bwm-ng python-matplotlib -qy'
end
