from scapy.all import sniff, TCP, IP
import socket
import os

SERVER_IP = input('enter th ip of vps >> ') 
SERVER_PORT = int(input('enter the port >> '))

def send_to_server(features, attacker_ip):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_IP, SERVER_PORT))
         
        data = f"{features['duration']},{features['src_bytes']},{features['dst_bytes']},{features['count']},{features['srv_count']}"
        client.send(data.encode())
        
        
        response = client.recv(1024).decode()
        
        if response == "BLOCK":
            print(f"!!! ATTACK DETECTED! Blocking IP: {attacker_ip} ...")
            
            os.system(f"sudo iptables -A INPUT -s {attacker_ip} -j DROP")
        
        client.close()
    except Exception as e:
        print(f"Connection Error: {e}")

def process_packet(packet):
    if packet.haslayer(TCP) and packet.haslayer(IP):
        
        attacker_ip = packet[IP].src
        
        features = {
            'duration': 0.0, 
            'src_bytes': len(packet[TCP]),
            'dst_bytes': 0.0,
            'count': 1.0,
            'srv_count': 1.0
        }
        send_to_server(features, attacker_ip)

print("/////STARTING/////")
sniff(filter="tcp", prn=process_packet, store=0)
