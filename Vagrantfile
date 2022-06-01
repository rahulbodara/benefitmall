project = "stack_theme"

Vagrant.configure(2) do |config|

    # vagrant box
    config.vm.box = "ubuntu/bionic64"

    # ports to access the virtual machine
    config.vm.network :forwarded_port, guest: 8000, host: 8000

    # shared folder setup
    config.vm.synced_folder ".", "/home/vagrant/#{project}"

    # SSH agent forwarding
    config.ssh.forward_agent = true

    # provisioning script
    config.vm.provision "shell", path: "provision/provision.sh",
        privileged: false

    config.vm.provider "virtualbox" do |vb|
        # Customize the amount of memory on the VM:
        vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
        vb.memory = "6000"
    end

end