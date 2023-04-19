from dataclasses import dataclass

from .time_util import get_current_epoch_in_ms
from .parser import RedisCommand

storage = {}


@dataclass
class SetStorage:
    value: str
    expiry: str | None


def execute(command: RedisCommand) -> str | None:
    target_command = command.command
    print(f"execute | {target_command=}")

    match target_command:
        case "PREFLIGHT":
            return ""

        case "PING":
            return "PONG"

        case "ECHO":
            return command.get_value()

        case "SET":
            (key, value) = command.get_key_value()
            expiry_in_ms = command.get_expiry_in_unix_timestamp()
            storage[key] = SetStorage(
                value=value,
                expiry=expiry_in_ms,
            )
            return "OK"

        case "GET":
            key = command.get_value()
            set_storage = storage[key]

            if set_storage.expiry != 'None':
                now = get_current_epoch_in_ms()
                if str(now) >= set_storage.expiry:
                    return "$-1\r\n"

            return set_storage.value

        case _:
            return None
