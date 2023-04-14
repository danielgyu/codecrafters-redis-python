import asyncio


async def _handle_read(reader: asyncio.StreamReader) -> bool:
    if data := await reader.read(100):
        print(f"received {data}")
        return False
    else:
        return True


async def _handle_write(writer: asyncio.StreamWriter) -> None:
    writer.write(b"+PONG\r\n")
    await writer.drain()
    print("sent pong response")


async def _handle_request(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    finished = False
    while not finished:
        finished = await _handle_read(reader)
        if not finished:
            await _handle_write(writer)


async def main():
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
