from .BidirectionalIterator import BidirectionalIterator

class ConstBidirectionalIterator[T]:
    def __init__(self, container: list[T], reverse: bool = False):
        self._container = container
        self._reverse = reverse
        if reverse:
            self._index = len(container) - 1 if container else -1
        else:
            self._index = 0 if container else -1

    def __iter__(self):
        return self

    def __next__(self) -> T:
        if self._index < 0 or self._index >= len(self._container):
            raise StopIteration
        value = self._container[self._index]
        if self._reverse:
            self._index -= 1
        else:
            self._index += 1
        return value

    def prev(self) -> T:
        if self._reverse:
            if self._index + 1 >= len(self._container):
                raise StopIteration
            self._index += 1
            return self._container[self._index]
        else:
            if self._index <= 0:
                raise StopIteration
            self._index -= 1
            return self._container[self._index]

    def __eq__(self, other: "ConstBidirectionalIterator | BidirectionalIterator") -> bool:
        if not hasattr(other, '_container'):
            return False
        return (
            self._container is other._container and
            self._index == other._index and
            self._reverse == other._reverse
        )

    def __ne__(self, other: "ConstBidirectionalIterator | BidirectionalIterator") -> bool:
        return not self.__eq__(other)