#!/usr/bin/env python

import sys
import socket
import getopt
import threading
import subprocess
import os
#import tqdm

target = ""
port = 0

def usage():
    print("Netdog Tool for uploading")
    print()
    print("-p --port  - listen for incoming connections [port]")
    print()
    print("Examples: ")
    print("netdog.py -t 192.168.0.1 -p 8080")
    sys.exit(0)

def run_command(command):
    command = command.rstrip()
    output = ""

    try:
        if command[0:2] == 'cd':
            path = command[3:]
            os.chdir(path)
            output = path
            #path = os.getcwd()
        else:
            command_output = subprocess.run(command,capture_output=True, shell=False)
    except:
        output = "Failed to execute command.\r\n"

    if len(output):
        return bytes(output,'utf-8')
    elif command_output.returncode == 0:
        return command_output.stdout
    else:
        return command_output.stderr

def server_loop():
    global target

    if not target:
        target = socket.gethostname()
    if port == 0:
        usage()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=handler,args=(client_socket,))
        client_thread.start()

def handler(client_socket):
    BUFFER_SIZE = 4096
    while True:
        path = os.getcwd()
        client_socket.send(bytes(f"<netdog:{path}> ",'utf-8'))

        cmd_buffer = ""
        while "\n" not in cmd_buffer:
            data = client_socket.recv(BUFFER_SIZE)
            cmd_buffer += data.decode()
#            print(cmd_buffer)

        response = run_command(cmd_buffer)
        client_socket.send(response)

def main():
    global target
    global port

    try:
        opts,args = getopt.getopt(sys.argv[1:],"ht:p:",["help","target","port"])
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

    server_loop()

if __name__ == '__main__':
    main()
