import asyncio


async def _handle_read(reader: asyncio.StreamReader) -> None:
    data = await reader.read(1024)
    print(f"received {data}")


async def _handle_write(writer: asyncio.StreamWriter) -> None:
    writer.write(b"+PONG\r\n")
    await writer.drain()
    print("sent pong response")


async def _handle_request(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    print("start request")
    await _handle_read(reader)
    await _handle_write(writer)
    print("end request\n")


async def main():
    print("Logs from your program will appear here!")

    server_socket = await asyncio.start_server(
        _handle_request,
        "localhost",
        6379,
        reuse_port=True,
    )

    async with server_socket:
        await server_socket.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
