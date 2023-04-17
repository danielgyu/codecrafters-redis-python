COMMANDS = ("PING", "ECHO", "SET", "GET")
TYPE_DEFINER = ("+", "-", ":", "$", "*")
IGNORE = ("COMMAND", "DOCS")


class RedisCommand:
    def __init__(self, command: str):
        self.command = command
        self._values = []

    def add_value(self, value: str) -> None:
        self._values.append(value)

    def get_value(self) -> str:
        return self._values[-1]

    def get_pair(self) -> tuple[str, str]:
        return self._values[0], self._values[1]

def parse(data: bytes) -> RedisCommand | None:
    line = data.decode().split("\r\n")[:-1]

    command = None
    for token in line:
        print(f"redis-server | parse | {token=}")
        if token[0] in TYPE_DEFINER:
            continue
        if token in IGNORE:
            return RedisCommand("PREFLIGHT")
        elif token.upper() in COMMANDS:
            command = RedisCommand(token.upper())
        elif token.isalpha():
            assert command
            command.add_value(token)
        else:
            raise Exception(f"not implemented {token=}")

    print(f"redis-server | {command=}")
    return command
