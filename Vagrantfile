# frozen_string_literal: true

Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu2404"
  config.vm.box_version = ENV.fetch("VAGRANT_BOX_VERSION", "4.3.12")
  config.vm.hostname = "ansible-portfolio-demo"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "ansible-portfolio-demo"
    vb.memory = 2048
    vb.cpus = 2
  end

  config.vm.provision "shell", privileged: true, inline: <<-SHELL
    set -eu
    apt-get update -qq
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-venv
    python3 -m venv /opt/ansible-venv
    /opt/ansible-venv/bin/pip install --disable-pip-version-check ansible-core==2.17.13
    /opt/ansible-venv/bin/ansible-galaxy collection install \
      -r /vagrant/collections/requirements.yml \
      -p /vagrant/.cache/ansible/collections
  SHELL

  config.vm.provision "ansible_local" do |ansible|
    ansible.install = false
    ansible.ansible_playbook_command = "/opt/ansible-venv/bin/ansible-playbook"
    ansible.config_file = "ansible.cfg"
    ansible.inventory_path = "inventories/local/hosts.yml"
    ansible.playbook = "playbooks/site.yml"
    ansible.limit = "all"
  end
end
