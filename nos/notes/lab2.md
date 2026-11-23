NOS LAB2 - setup and work steps

WHY A VM

The lab is Linux kernel modules. You build them against Linux kernel headers and load them with insmod into a Linux kernel.
macOS has a different kernel (XNU). You cannot load the modules there.
Docker does not help. Containers use the kernel of the hidden Docker VM. That kernel has no headers for you.
A bug in a module is a kernel bug. It can stop the full machine. In a VM you only restart the VM.
This Mac is arm64. The image from the course is probably x86_64 and will be very slow here. Use an ARM64 Linux VM. The lab does not depend on x86.


1. SET UP THE VM (UTM)

1. Install UTM:
     brew install --cask utm
2. Download the Ubuntu Server 24.04 LTS ARM64 ISO from ubuntu.com.
3. In UTM: Create a New Virtual Machine > Virtualize > Linux. Select the ISO.
4. Set 4 GB RAM, 2 or more CPU cores, 20 GB disk.
5. Start the VM and install Ubuntu. Select "Install OpenSSH server" in the installer.
6. After the installation, stop the VM, remove the ISO from the CD drive, and start the VM again.
7. In the VM, install the tools:
     sudo apt update
     sudo apt install build-essential git linux-headers-$(uname -r)
8. Find the VM address:
     ip a
9. Connect from the Mac:
     ssh <user>@<address>
10. Stop the VM and clone it in UTM (right-click > Clone). This is your backup.


2. GET THE CODE

1. In the VM, clone the course repository from GitHub (link is on the course page).
2. Clone your own repository in the VM too. Do the work there, then commit and push.
   Do not build on a folder that is shared with the Mac. The build can fail there.


3. WORK CYCLE (same for all tasks)

1. Build the module:
     make
2. Load the module:
     sudo insmod <module>.ko <parameters>
3. Read the kernel log:
     sudo dmesg -w
   Keep this in a second terminal.
4. Make sure that the devices exist:
     ls -l /dev | grep <name>
   If they do not exist, read the load script or the README in the course code.
5. Run the test programs.
6. Remove the module:
     sudo rmmod <module>
7. Change the code and do the cycle again.

If the VM stops responding, restart it. If it does not start, use the clone.


4. LAB2A - poll (3 points)

1. Read the code in lab2a. Find the module parameters for the number of devices and buffers.
2. Build and load the module with more than one device.
3. Write program 1: open all devices for read, wait with poll, read one character, print it.
4. Write program 2: open all devices for write. Each 5 seconds use poll to find the devices that can accept data. Select one at random and write one character.
5. Run the two programs in two terminals. Make sure that program 1 prints what program 2 sends.


5. LAB2B - ioctl (3 points)

1. Read the code in lab2b. It is almost complete. Find the parts that are missing.
2. Make three devices:
     input   - open and write only. Data goes into the input buffer.
     output  - open and read only. Data comes from the output buffer.
     control - open and ioctl only. The ioctl number is the number of bytes to move from the input buffer to the output buffer. Stop when the input buffer is empty or the output buffer is full.
3. Add a timer that starts when the module loads. Each 5 seconds it moves one character from the input buffer to the output buffer.
4. Test: write to the input device, send ioctl to the control device, read from the output device.
5. Test the timer: write to the input device, wait, read from the output device.


6. LAB2C - optional (4 points)

1. Look at the digit before the last digit of your JMBAG.
     even -> message queue
     odd  -> pipe
2. Read the example solution from the course page.
3. Module parameters:
     message queue: maximum number of messages, maximum message size, maximum number of open calls
     pipe: buffer size, maximum number of open calls
4. open: accept only O_RDONLY, O_WRONLY or O_RDWR. All other flags give an error.
   read on a write-only file gives an error. write on a read-only file gives an error.
5. write: give an error if the data is too large. Block if there is no space.
6. read: block if there is no data.
7. Each successful read wakes the first blocked writer. Each successful write wakes the first blocked reader.
8. Write test programs with more than one reader and writer.


7. BEFORE THE HAND-IN

1. Ask if the demonstration is on your laptop or on the lab computers.
2. If it is on the lab computers, find their kernel version. Kernel functions change between versions. Build and test on that version if you can.
3. Hand in early. The points depend on the week.
