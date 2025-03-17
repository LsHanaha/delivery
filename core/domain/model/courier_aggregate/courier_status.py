import enum


class CourierStatusEnum(enum.Enum):
    Free = "free"
    Busy = "busy"

    def describe(self) -> str:
        return f"{self.name} has a value of {self.value}"
