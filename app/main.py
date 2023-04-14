import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        conn, addr = server_socket.accept() # wait for client
        print(f"accepted connection from {addr}")

        while data := conn.recv(1024):
            print(f"received {data}")

            conn.send(b"+PONG\r\n")
            print("sent pong response")


if __name__ == "__main__":
    main()
