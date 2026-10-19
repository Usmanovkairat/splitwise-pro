"""Repository contract and isolated in-memory implementation."""
from copy import deepcopy
from typing import Protocol

class Repository(Protocol):
    def list(self, collection: str, group_id: str | None = None) -> list[dict]: ...
    def get(self, collection: str, resource_id: str) -> dict | None: ...
    def save(self, collection: str, value: dict) -> dict: ...
    def delete(self, collection: str, resource_id: str) -> None: ...
    def delete_group(self, group_id: str) -> None: ...

class MemoryRepository:
    def __init__(self):
        self.data = {k: {} for k in ('groups','members','expenses','settlements')}
    def list(self, collection, group_id=None):
        return deepcopy([v for v in self.data[collection].values() if group_id is None or v['group_id'] == group_id])
    def get(self, collection, resource_id):
        return deepcopy(self.data[collection].get(resource_id))
    def save(self, collection, value):
        self.data[collection][value['id']] = deepcopy(value)
        return deepcopy(value)
    def delete(self, collection, resource_id):
        del self.data[collection][resource_id]
    def delete_group(self, group_id):
        for name in ('expenses','settlements','members'):
            for row in self.list(name,group_id):
                self.delete(name,row['id'])
        self.delete('groups',group_id)
