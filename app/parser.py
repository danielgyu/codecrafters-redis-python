from .commands import (
    EchoCommand,
    PreflightCommand,
    PingCommand,
    RedisCommand,
    GetCommand,
    SetCommand,
)

COMMANDS = ("PING", "ECHO", "SET", "GET")
TYPE_DEFINER = ("+", "-", ":", "$", "*")
IGNORE = ("COMMAND", "DOCS")


COMMAND_DICT = {
    "PING": PingCommand,
    "ECHO": EchoCommand,
    "SET": SetCommand,
    "GET": GetCommand,
}


def parse(data: bytes) -> RedisCommand | None:
    line = data.decode().split("\r\n")[:-1]
    print(f"parse | {line=}")

    command_token = line[2].upper()
    print(f"parse | {command_token=}")
    if command_token in IGNORE:
        return PreflightCommand()
    if command_token not in COMMANDS:
        return None

    command = COMMAND_DICT[command_token]()

    values = []
    for token in line[3:]:
        if not token[0] in TYPE_DEFINER:
            values.append(token)

    command.set_values(values)

    return command
