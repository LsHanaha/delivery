import threading

from delivery.core.ports.domain_event_abc import DomainEventABC


class TasksStorage:
    tasks: dict[str, list[DomainEventABC]] | None = None
    _instance = None
    _lock = threading.Lock()

    def __new__(cls) -> "TasksStorage":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def add_task(self, key: str, message: DomainEventABC) -> None:
        if not self.tasks:
            self.tasks = {}
        if not self.tasks.get(key):
            self.tasks[key] = []
        self.tasks[key].append(message)

    def get_tasks_by_key(self, key: str) -> list[DomainEventABC]:
        return self.tasks.get(key, [])
