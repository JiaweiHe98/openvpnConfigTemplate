import os
import subprocess

# get current ip
p = subprocess.Popen(['curl', 'ifconfig.me'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
stdout, stderr = p.communicate()

default_ip = stdout.decode('utf-8')

IP = input(f'Please input your remote IP (default {default_ip}): ')

if IP == '':
    IP = default_ip

PORT = input('Please input your port (default 1194): ')

try:
    PORT = int(PORT)
except:
    PORT = 1194

PROTO = input('Please input your protocol (tcp or udp default udp): ')

if PROTO not in ('tcp', 'udp'):
    PROTO = 'udp'

DEV = input('Please input your device (tap or tun default tun): ')

if DEV not in ('tap', 'tun'):
    DEV = 'tun'

def cmd(command):
    os.system(command)
    
SYS = input('Please input your server system (mac, win, or linux default linux)')

if SYS not in ('mac', 'win', 'linux'):
    SYS = 0
elif SYS == 'mac' or SYS == 'linux':
    SYS = 0
else:  
    SYS = 1
    
if SYS == 1:
    win_settings = '''
data-ciphers AES-256-CBC
data-ciphers-fallback AES-256-CBC
'''
else:
    win_settings = ''
    
# download easy-rsa
if not os.path.exists('easy-rsa'):
    cmd('git clone https://github.com/OpenVPN/easy-rsa.git')

# change dir
os.chdir('./easy-rsa/easyrsa3')

# init pki
p = subprocess.Popen(['./easyrsa', 'init-pki'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

stdout, stderr = p.communicate(input=b'yes\nyes\n')

print(stdout.decode('utf-8'))


# gen ca
p = subprocess.Popen(['./easyrsa', 'build-ca', 'nopass'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

stdout, stderr = p.communicate(input=b'\n')

print(stdout.decode('utf-8'))

# gen server
p = subprocess.Popen(['./easyrsa', 'build-server-full', 'server', 'nopass'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

stdout, stderr = p.communicate(input=b'yes\n')

print(stdout.decode('utf-8'))

# gen client
p = subprocess.Popen(['./easyrsa', 'build-client-full', 'client', 'nopass'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

stdout, stderr = p.communicate(input=b'yes\n')

print(stdout.decode('utf-8'))

# gen dh
cmd('./easyrsa gen-dh')

# go back
os.chdir('../../')

# make directory for certs and keys
cmd('rm -rf generatedFiles')

cmd('mkdir generatedFiles')

# gen key
cmd('openvpn --genkey --secret ./generatedFiles/secret.key')

# move things
cmd('cp easy-rsa/easyrsa3/pki/ca.crt ./generatedFiles/')
cmd('cp easy-rsa/easyrsa3/pki/private/ca.key ./generatedFiles/')
cmd('cp easy-rsa/easyrsa3/pki/private/client.key ./generatedFiles/')
cmd('cp easy-rsa/easyrsa3/pki/private/server.key ./generatedFiles/')
cmd('cp easy-rsa/easyrsa3/pki/issued/client.crt ./generatedFiles/')
cmd('cp easy-rsa/easyrsa3/pki/issued/server.crt ./generatedFiles/')
cmd('cp easy-rsa/easyrsa3/pki/dh.pem ./generatedFiles/')

# create config
with open('server.ovpn', 'w') as f:
    with open('./generatedFiles/ca.crt', 'r') as temp:
        ca = temp.read()[:-1]
    
    with open('./generatedFiles/server.crt', 'r') as temp:
        cert = temp.read()
        cert = '-----BEGIN CERTIFICATE-----\n' + cert.split('-----BEGIN CERTIFICATE-----')[1][:-1]
        
    with open('./generatedFiles/server.key', 'r') as temp:
        key = temp.read()[:-1]
        
    with open('./generatedFiles/dh.pem', 'r') as temp:
        dh = temp.read()[:-1]
        
    with open('./generatedFiles/secret.key', 'r') as temp:
        tls = temp.read()[:-1]
    
    config = f'''
port {PORT}
proto {PROTO}
dev {DEV}
topology subnet
server 10.8.0.0 255.255.255.0
client-to-client
keepalive 10 120
key-direction 0
cipher AES-256-CBC{win_settings}
persist-key
persist-tun
status openvpn-status.log
verb 3
{'explicit-exit-notify 1' if PROTO == 'udp' else ''}
<ca>
{ca}
</ca>
<cert>
{cert}
</cert>
<key>
{key}
</key>
<dh>
{dh}
</dh>
<tls-crypt>
{tls}
</tls-crypt>
'''
    
    f.write(config)
    
# client config
with open('client.ovpn', 'w') as f:    
    with open('./generatedFiles/client.crt', 'r') as temp:
        cert = temp.read()
        cert = '-----BEGIN CERTIFICATE-----\n' + cert.split('-----BEGIN CERTIFICATE-----')[1][:-1]
        
    with open('./generatedFiles/client.key', 'r') as temp:
        key = temp.read()[:-1]
    
    config = f'''
client
dev {DEV}
proto {PROTO}
remote {IP} {PORT}
persist-key
persist-tun
remote-cert-tls server
auth SHA512
cipher AES-256-CBC
key-direction 1
verb 3

<ca>
{ca}
</ca>
<cert>
{cert}
</cert>
<key>
{key}
</key>
<tls-crypt>
{tls}
</tls-crypt>
'''
    
    f.write(config)

print('----------------------------------------')
print('OK!')
