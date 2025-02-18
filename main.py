import socket
import threading
import json
from time import sleep

connected_clients = []
thread_lock = threading.Lock()
local_port = None
host_socket = None
username = ""
teamname = "ARYANS"


def mandatory_connections():
    mandatory_peers = [("10.206.4.201", 1255), ("10.206.5.228", 6555)]
    for ip, port in mandatory_peers:
        if transmit_message(
            ip, port, "connect", f"<{ip}:{port}> <{teamname}> Mandatory connection"
        ):
            print(f"Mandatory connection sent to {ip}:{port}")
        else:
            print(f"Failed to send mandatory connection to {ip}:{port}")


def init_server():
    global host_socket
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_socket.bind(("0.0.0.0", local_port))
    host_socket.listen(5)
    print(f"Server listening on port {local_port}")
    while True:
        try:
            client_socket, addr = host_socket.accept()
            client_thread = threading.Thread(
                target=client_handler, args=(client_socket,)
            )
            client_thread.start()
        except:
            break


def client_handler(client_socket):
    try:
        data = client_socket.recv(1024).decode()
        if not data:
            return
        message = json.loads(data)
        sender_ip = client_socket.getpeername()[0]
        sender_port = message["sender_port"]
        sender_name = message["sender_name"]
        with thread_lock:
            peer = (sender_ip, sender_port)
            if peer not in connected_clients:
                connected_clients.append(peer)
                print(f"New peer connected: {sender_ip}:{sender_port}")

        if message["type"] == "exit":
            with thread_lock:
                if peer in connected_clients:
                    connected_clients.remove(peer)
                    print(f"Peer {sender_ip}:{sender_port} disconnected")
        elif message["type"] == "message":
            print(
                f"\n[{sender_name} ({sender_ip}:{sender_port})] {message['content']}\n"
            )
        elif message["type"] == "connect":
            print(f"\nConnected to {sender_name} ({sender_ip}:{sender_port})\n")

    except json.JSONDecodeError:
        print("Message received is invalid")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def transmit_message(target_ip, target_port, message_type, content):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((target_ip, target_port))
        message = {
            "type": message_type,
            "content": f"<{target_ip}:{target_port}> <{teamname}> {content}",
            "sender_name": username,
            "sender_port": local_port,
        }
        client_socket.send(json.dumps(message).encode())
        client_socket.close()
        return True
    except Exception as e:
        print(f"Error sending message to {target_ip}:{target_port}: {e}")
        return False


def show_user_menu():
    while True:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query active peers")
        print("3. Connect to active peers")
        print("0. Quit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            target_ip = input("Enter the recipient's IP address: ").strip()
            target_port = int(input("Enter the recipient's port number: ").strip())
            message_content = input("Enter your message: ").strip()
            if transmit_message(target_ip, target_port, "message", message_content):
                print(f"Message sent to {target_ip}:{target_port}")
            else:
                print("Failed to send message")
        elif choice == "2":
            with thread_lock:
                if connected_clients:
                    print("Connected Peers:")
                    for idx, (ip, port) in enumerate(connected_clients, 1):
                        print(f"{idx}. {ip}:{port}")
                else:
                    print("No connected peers")
        elif choice == "3":
            target_ip = input("Enter the peer's IP address to connect: ").strip()
            target_port = int(input("Enter the peer's port number: ").strip())
            if transmit_message(
                target_ip,
                target_port,
                "connect",
                f"<{target_ip}:{target_port}> <{teamname}> Connection request",
            ):
                print(f"Connection request sent to {target_ip}:{target_port}")
            else:
                print("Failed to send connection request")
        elif choice == "0":
            with thread_lock:
                for ip, port in connected_clients.copy():
                    transmit_message(
                        ip, port, "exit", f"<{ip}:{port}> {teamname} Exiting"
                    )
            if host_socket:
                host_socket.close()
            print("Closing the chat box......")
            print("Exiting......")
            break
        else:
            print("Invalid choice")


def main():
    global username, local_port
    username = input("Enter your name: ").strip()
    local_port = int(input("Enter your port number: ").strip())
    server_thread = threading.Thread(target=init_server)
    server_thread.daemon = True
    server_thread.start()
    sleep(1)
    mandatory_connections()
    show_user_menu()


if __name__ == "__main__":
    main()
