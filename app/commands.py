import time

class RedisCommand():
    def __init__(self):
        self.command = ""
        self._keys = []
        self._values = []

    def set_values(self, values: list[str]) -> None:
        self._values = values

    def get_value(self) -> str:
        return self._values[0]

    def get_key(self) -> str:
        raise NotImplementedError()

    def get_expiry_in_unix_timestamp(self) -> str | None:
        raise NotImplementedError()

    def get_key_value(self) -> tuple[str, str]:
        raise NotImplementedError()


class PreflightCommand(RedisCommand):
    def __init__(self):
        super().__init__()
        self.command = "PREFLIGHT"

class PingCommand(RedisCommand):
    def __init__(self):
        super().__init__()
        self.command = "PING"


class EchoCommand(RedisCommand):
    def __init__(self):
        super().__init__()
        self.command = "ECHO"


class GetCommand(RedisCommand):
    def __init__(self):
        super().__init__()
        self.command = "GET"

    def get_value(self):
        return self._values[0]


class SetCommand(RedisCommand):
    def __init__(self):
        super().__init__()
        self.command = "SET"
        self._options = []
        self._expiry_in_milliseconds = None

    def get_key_value(self) -> tuple[str, str]:
        return self._values[0], self._values[1]

    def get_expiry_in_unix_timestamp(self) -> str | None:
        return str(self._expiry_in_milliseconds)

    def set_values(self, values: list[str]) -> None:
        self._values = values[0:2]

        if len(values) == 2:
            return
        
        for idx, value in enumerate(values[2:], 2):
            match value.upper():
                case "PX":
                    expire_after_in_ms = (float(values[idx+1]) // 1000)
                    now = time.time()
                    self._expiry_in_milliseconds = now + float(expire_after_in_ms)
