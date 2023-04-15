COMMANDS = ("PING", "ECHO")
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

def parse(data: bytes) -> list[RedisCommand]:
    line = data.decode().split("\r\n")[:-1]

    commands = []
    for token in line:
        print(f"redis-server | parse | {token=}")
        if token[0] in TYPE_DEFINER or token in IGNORE:
            continue
        elif token.upper() in COMMANDS:
            commands.append(RedisCommand(token.upper()))
        elif token.isalpha():
            commands[-1].add_value(token)
        else:
            raise Exception("not implemented = ", token)

    print(f"redis-server | {commands=}")
    return commands
