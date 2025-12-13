
class GraphError(Exception):
    """Базовый класс для всех исключений, связанных с графом."""
    pass


class VertexNotExistsError(GraphError):
    """Выбрасывается, если вершина не найдена в графе."""
    pass


class VertexAlreadyExistsError(GraphError):
    """Выбрасывается при попытке добавить вершину, которая уже существует."""
    pass


class EdgeNotExistsError(GraphError):
    """Выбрасывается, если дуга не найдена в графе."""
    pass


class EdgeAlreadyExistsError(GraphError):
    """Выбрасывается при попытке добавить дугу, которая уже существует."""
    pass