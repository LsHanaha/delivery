import enum


class OrderStatusEnum(enum.Enum):
    Created = "created"
    Assigned = "assigned"
    Completed = "completed"

    def describe(self) -> str:
        return f"{self.name} has a value of {self.value}"
