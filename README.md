
# NI_GPIB_ENET_Py3
Python3 scripts to set up and communicate with the obsolete NI GPIB-ENET (not GPIB-ENET/100 OR 1000).

## Set up IP address

The NI GPIB-ENET uses the obsolete **Reverse-ARP(RARP)** protocol for setting up the IP address (when switch-5 is **OFF**).
The protocol works on Layer 2 (Data link layer), which means we cannot read/write the raw packets via Python3's builtin module `socket` on Windows. But it's doable on Linux. Please refer to https://www.cloudshark.org/captures/c6729d0fc558 for the details of the request/reply packets.

#### Example raw packets
Just an example, in my case

| Item  | MAC Addr | IP | IP(hex) |
| ------------- | ------------- | ------------- | ------------- |
| PC  | 90-B1-1C-9B-B1-E9 | 192.168.3.1  | C0 A8 03 01 |
| GPIB-ENET | 00-80-2F-FF-09-94 | 192.168.3.2 | C0 A8 03 02 |

The RARP reply packet to be sent to GPIB-ENET
```
00 80 2F FF 09 94|90 B1 1C 9B B1 E9|80 35|00 01|08 00|06|04|00 04|90 B1 1C 9B B1 E9|C0 A8 03 01|00 80 2F FF 09 94|C0 A8 03 02 
```
* Target MAC (GPIB-ENET) `00 80 2F FF 09 94`
* Sender MAC (PC) `90 B1 1C 9B B1 E9`
* Protocol (RARP) `80 35`
* Hardware (Ethernet) `00 01`
* IPv4 `08 00`
* Hardware size `06`
* Protocol size `04`
* Opcode (reply) `00 04`
* Sender MAC `90 B1 1C 9B B1 E9`
* Sender IP `C0 A8 03 01`
* Target MAC `00 80 2F FF 09 94`
* Target IP `C0 A8 03 02`

### Windows
Please check [libpcap](https://pypi.org/project/libpcap/) for sending the reply packet in Python3.
Alternatively, some traffic generators can be found on [WireShark Wiki](https://gitlab.com/wireshark/wireshark/-/wikis/Tools#traffic-generators).
I used the free [Packet Player](https://www.colasoft.com/packet_player/) from Colasoft to convert the HEX text to `*.cap` then sent it.

### Linux

Please check the [documentation](https://docs.python.org/3/library/socket.html) for `socket` on how to send the reply packet in Python3.
Hint: use `socket(AF_PACKET, SOCK_RAW)`

### Store IP address
When the IP assignment is finished, the READY LED indicator will become steady.
If you want to retain the IP address in the future power cycles, you may turn off the NI GPIB-ENET and turn switch-5 to **ON**.

## Communication

The low-level `libnienet.py` was originally written by [Robert Jordens](mailto:jordens@debian.org). I modified it to work with Python3.

An simple high-level wrapper (`GPIBENET`) over `libnienet.py` can be found in `example_simple_wrapper.py`. Only `read`/`write`/`query` have been implemented. All the input/return 'string's were kept as `bytes`, so please `encode` or `decode` them per your needs.

Example device GPIB address is 16,
```python3
from example_simple_wrapper import GPIBENET
GPIB_ENET_ADDR = '192.168.3.2'
DEV_GPIB_ADDR = 16
dev = GPIBENET(GPIB_ENET_ADDR, DEV_GPIB_ADDR)
print(dev.query(b'*IDN?').encode())
# OUTPUT:
# KEITHLEY INSTRUMENTS INC.,MODEL 2010,0772543,A10  /A02
```

The scripts have met my needs so far, so I have no motivation to improve them any more.
But you are more than welcome to fork/modify it.
