from .parser import RedisCommand

storage = {}


def execute(command: RedisCommand) -> str | None:
    target_command = command.command
    print(f"redis-server | execute | {target_command=}")

    match target_command:
        case "PREFLIGHT":
            return ""
        case "PING":
            return "PONG"
        case "ECHO":
            return command.get_value()
        case "SET":
            (key, value) = command.get_pair()
            storage[key] = value
            return "OK"
        case "GET":
            key = command.get_value()
            return storage[key]
        case _:
            return None
