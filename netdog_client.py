#!/usr/bin/env python
import sys
import socket
import getopt
import os
#import tqdm

target = ""
port = 0
#command = False
#fileupload = ""

def usage():
    print("Netdog Tool")
    print()
    print("Usage: netdog.py -t target_host -p port")
#    print("-u --upload      -upload file to [host]:[port]")
#    print("-c --commandline -access terminal on [host]:[port]")
    print()
    print()
    print("Examples: ")
#    print("netdog_client -t 192.168.0.1 -p 5555 -u /home/vuyani.txt")
    print("netdog_client -t 192.168.0.1 -p 5555")
    sys.exit(0)

#def upload_file(filename):
#    SEPARATOR = "<SEPARATOR>"
#    BUFFER_SIZE = 4096
#    global target
     
#    if not len(target):
#        target = socket.gethostname()
#    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#    try:
#        filesize = os.path.getsize(filename)
#    except:
#        print(f"Path {filename} does not exist or is inaccessible")
#        client.close()

#    try:
#        print(f"[+] Connecting to {target}:{port}")
#        client.connect((target,port))
#        print(f"[+] Connected.")

#        client.send(bytes(f"{filename}{SEPARATOR}{filesize}", 'utf-8'))

#        progress = tqdm.tqdm(range(filesize),f"Sending {filename}",unit="B",unit_scale=True,unit_divisor=1024)

#        with open(file,"rb") as f:
#            while True:
#                bytes_read = f.read(BUFFER_SIZE)

#                if not bytes_read:
#                    break
#                s.sendall(bytes_read)
#                progress.update(len(bytes_read))
#    except:
#        print(f"[+] Exception! Exiting.")
#        client.close()

def cmdline():
    global target
    BUFFER_SIZE = 4096
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    if not len(target):
        target = socket.gethostname()
        if port == 0:
            usage()
    
    try:
        print(f"[+] Connecting to {target}:{port}")
        client.connect((target,port))
        print(f"[+] Connected.")
        
        while True:
            data = ""
            command = ""
            data = client.recv(BUFFER_SIZE)
            prompt = data.decode()
            command = input(prompt)
            command += '\n'
            client.send(bytes(command,'utf-8'))
            
            recv_len = 1
            buffer_info = ""
            while recv_len:
                data = client.recv(BUFFER_SIZE)
                recv_len = len(data)
                buffer_info += data.decode()

                if recv_len < BUFFER_SIZE:
                    break
            
            print(buffer_info)
    except:
        print(f"[+] Exception exiting!")
        client.close()
        
def main():
    global target
    global port

    try:
        opts, args = getopt.getopt(sys.argv[1:],"ht:p:",["help","target","port"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-t","--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    cmdline()


if __name__ == '__main__':
    main()

