# Peer-to-Peer Chat Application

## Prerequisites

- Python 3.x
- Required libraries:
  - `socket`
  - `threading`
  - `json`
  - `time`



## Features

- **Peer Discovery:** Automatically connects to mandatory peers on startup.
- **Messaging:** Send and receive real-time messages between peers.
- **Peer Management:** View connected peers and manage connections.
- **Exit Handling:** Notifies connected peers when exiting.



## Getting Started


### Running the Application

1. Open a terminal and navigate to the directory containing the script.
2. Run the application using:
    ```bash
    python main.py
    ```
3. Enter your username and local port number when prompted.


## Menu Options

```
***** Menu *****
1. Send message
2. Query active peers
3. Connect to active peers
0. Quit
```

## How It Works

- The chatbox starts by setting up a server socket to listen for incoming connections on the specified port.
- It then attempts to establish mandatory connections with predefined peers.
- it provides user to :
  - Send messages to other peers by specifying their IP and port.
  - Query a list of active peers.
  - Connect to new peers.
  - Exit gracefully, notifying connected peers of disconnection.



## Team Member name and roll number

- Ruva Kachhia - 230003061
- Aaditya Singh - 230004001
- Anurag Singh - 230002011

## Our team has attempted all the parts and also has attempted bonus question as well