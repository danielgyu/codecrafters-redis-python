# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    conn, addr = server_socket.accept() # wait for client
    print(f"accepted connection from {addr}")

    while data := conn.recv(1024):
        print(f"received {data}")

        conn.send(b"+PONG\r\n")
        print("sent pong response")


if __name__ == "__main__":
    main()
