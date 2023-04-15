import asyncio

from .parser import parse
from .executor import execute

async def _handle_read(reader: asyncio.StreamReader) -> str | None:
    print(f"redis-server | reading...")
    data = await reader.read(1024)
    if not data:
        return None

    print(f"redis-server | request_data: {data=}")
    commands = parse(data)
    return execute(commands)


async def _handle_write(
    writer: asyncio.StreamWriter,
    data: str,
) -> None:
    writer.write(b"+" + data.encode() + b"\r\n")
    await writer.drain()
    print(f"redis-server | sent response: {data=}")


async def _handle_request(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    finished = False
    while not finished:
        response_data = await _handle_read(reader)
        if response_data == "PREFLIGHT":
            await _handle_write(writer, "") 
        elif response_data:
            print(f"redis-server | {response_data=}")
            await _handle_write(writer, response_data)
        else:
            print(f"redis-server | finished")
            finished = True


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
