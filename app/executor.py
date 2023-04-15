from .parser import RedisCommand


def execute(commands: list[RedisCommand]) -> str | None:
    if len(commands) == 0:
        print(f"redis-server | execute | preflight")
        return "PREFLIGHT"

    for command in commands:
        match command.command:
            case "PING":
                return "PONG"
            case "ECHO":
                return command.get_value()
            case _:
                return None

    return None
