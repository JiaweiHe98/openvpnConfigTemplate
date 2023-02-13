# openvpnConfigTools

## Cannot Find a Script for Creating VPNs without Forwarding?

This script only generates vpn configs for communicating between private networks. It will not set up ip forward, or push settings to redirect network traffic from the client to the server.

## Tired of generating CA, certificats, private key, Diffie–Hellman parameters, static key with easy-rsa by hand?

This script will help you simplity the work of creating config files between the server and you client.

The script will do:

1. Git clone (Download) easy-rsa from GitHub
1. Set up clean evironment -> `init-pki`
1. Build ca certificate and ca private key -> `build-ca`
1. Create server certificate and private key -> `build-server-full`
1. Create client certificate and private key -> `build-client-full`
1. Generate Diffie–Hellman parameters -> `gen-dh`
1. Generate tls-crypt key (static key) -> `openven --genkey secret`
1. Gathering all the files into one folder
1. Put things together to form config files (server.ovpn, client.ovpn)

## How to Use the Script

- You need python3 ([Intall Python](https://www.python.org/downloads/)) to run the script.
- You need OpenVPN installed on your machine and `openvpn` command shoud be callable from the directory the scrip will run.
- You need OpenVPN 2.5+ to enable `data-ciphers AES-256-GCM`, `data-ciphers-fallback AES-256-GCM` settings. Please follow this [link](https://community.openvpn.net/openvpn/wiki/OpenvpnSoftwareRepos) to update or install the newer version for your OS. **If you don't want to update and OpenVPN says it cannot recognize `data-cipher`, simply remove these two settings in server.ovpn file.**
- Run the script by `python3 generateServerAndClientConfig.py` or `python generateServerAndClientConfig.py`.
- Follow the prompt in the terminal to enter needed information.
- Generated config files will be put in the save directory where the script is run.
- All generated certs and keys will be in `generatedFiles` folder from where you run the script.
- Fire up the vpn server by `openvpn server.ovpn` or `openvpn --config server.ovpn --daemon` to run vpn in daemon.
