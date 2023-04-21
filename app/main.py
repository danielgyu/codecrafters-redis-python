import asyncio

from .parser import parse
from .executor import execute

async def _handle_read(reader: asyncio.StreamReader) -> str | None:
    print(f"redis-server | reading...")
    data = await reader.read(1024)
    if not data:
        return None

    print(f"handle_read | request_data: {data=}")
    command = parse(data)
    if not command:
        print("handle_read | data is none")
        return None

    return execute(command)


async def _handle_write(
    writer: asyncio.StreamWriter,
    data: str,
) -> None:
    if data == "NONE":
        response = b"$-1\r\n"
    else:
        response = b"+" + data.encode() + b"\r\n"

    print(f"redis-server | sending response: {data=}")
    writer.write(response)
    await writer.drain()


async def _handle_request(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    finished = False
    while not finished:
        response_data = await _handle_read(reader)
        if response_data is not None:
            await _handle_write(writer, response_data)
        else:
            finished = True
            print(f"redis-server | finished")


async def main():
    server_socket = await asyncio.start_server(
        _handle_request,
        "localhost",
        6379,
        reuse_port=True,
    )

    async with server_socket:
        print("redis-server | start server")
        await server_socket.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
