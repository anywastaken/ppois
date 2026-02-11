# social_network/search/Search.py

from abc import ABC, abstractmethod



class Search(ABC):

    @abstractmethod
    def search(self, query: str, limit: int = 10) -> list:

        pass

    @abstractmethod
    def search_by_id(self, item_id: int):

        pass

    def _validate_query(self, query: str) -> str:
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")
        return query.strip().lower()