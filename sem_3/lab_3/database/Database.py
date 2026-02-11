
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

T = TypeVar('T')
ID = TypeVar('ID')


class Database(ABC, Generic[T, ID]):
    def __init__(self):
        self._storage: dict[ID, T] = {}

    @abstractmethod
    def _get_id(self, entity: T) -> ID:
        pass

    def add(self, entity: T) -> None:
        """Добавляет сущность в хранилище."""
        entity_id = self._get_id(entity)
        if entity_id in self._storage:
            from social_network.exceptions.EntityAlreadyExistsException import EntityAlreadyExistsException
            raise EntityAlreadyExistsException(f"Entity with ID {entity_id} already exists")
        self._storage[entity_id] = entity

    def get_by_id(self, entity_id: ID) -> Optional[T]:
        """Возвращает сущность по ID или None."""
        return self._storage.get(entity_id)

    def get_all(self) -> List[T]:
        """Возвращает список всех сущностей."""
        return list(self._storage.values())

    def remove(self, entity_id: ID) -> bool:
        """Удаляет сущность по ID. Возвращает True, если удалена."""
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False

    def exists(self, entity_id: ID) -> bool:
        """Проверяет наличие сущности с данным ID."""
        return entity_id in self._storage