from copy import deepcopy

from .iterators.BidirectionalIterator import BidirectionalIterator
from .iterators.ConstBidirectionalIterator import ConstBidirectionalIterator

from .exceptions import (
    VertexNotExistsError,
    VertexAlreadyExistsError,
    EdgeNotExistsError,
    EdgeAlreadyExistsError
)


class DirectedGraphIncidence[T]:
    def __init__(self):
        self._vertices: list[T] = []
        self._edges: list[tuple[int, int]] = []
        self._incidence: list[list[int]] = []  # incidence[v_id][e_id]

    def __deepcopy__(self, memo) -> "DirectedGraphIncidence[T]":
        new_graph = DirectedGraphIncidence[T]()
        new_graph._vertices = deepcopy(self._vertices, memo)
        new_graph._edges = deepcopy(self._edges, memo)
        new_graph._incidence = deepcopy(self._incidence, memo)
        return new_graph

    def clear(self) -> None:
            self._vertices.clear()
            self._edges.clear()
            self._incidence.clear()

    def __del__(self):
        self.clear()

    def empty(self) -> bool:
        return len(self._vertices) == 0

    def __eq__(self, other: "DirectedGraphIncidence") -> bool:
        if not isinstance(other, DirectedGraphIncidence):
            return False
        return self._vertices == other._vertices and self._edges == other._edges

    def __ne__(self, other: "DirectedGraphIncidence") -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: "DirectedGraphIncidence") -> bool:
        if not isinstance(other, DirectedGraphIncidence):
            return NotImplemented
        return len(self._edges) < len(other._edges)

    def __le__(self, other: "DirectedGraphIncidence") -> bool:
        if not isinstance(other, DirectedGraphIncidence):
            return NotImplemented
        return len(self._edges) <= len(other._edges)

    def __gt__(self, other: "DirectedGraphIncidence") -> bool:
        if not isinstance(other, DirectedGraphIncidence):
            return NotImplemented
        return len(self._edges) > len(other._edges)

    def __ge__(self, other: "DirectedGraphIncidence") -> bool:
        if not isinstance(other, DirectedGraphIncidence):
            return NotImplemented
        return len(self._edges) >= len(other._edges)

    def begin_vertices(self) -> BidirectionalIterator[T]:
        return BidirectionalIterator(self._vertices)
    
    def rbegin_vertices(self) -> BidirectionalIterator[T]:
        return BidirectionalIterator(self._vertices, reverse=True)
    
    def const_begin_vertices(self) -> BidirectionalIterator[T]:
        return ConstBidirectionalIterator(self._vertices)
    
    def const_rbegin_vertices(self) -> BidirectionalIterator[T]:
        return ConstBidirectionalIterator(self._vertices, reverse=True)

    def begin_edges(self) -> BidirectionalIterator[tuple[T, T]]:
        edge_values = [(self._vertices[u], self._vertices[v]) for u, v in self._edges]
        return BidirectionalIterator(edge_values)
    
    def rbegin_edges(self) -> BidirectionalIterator[tuple[T, T]]:
        edge_values = [(self._vertices[u], self._vertices[v]) for u, v in self._edges]
        return BidirectionalIterator(edge_values, reverse=True)
    
    def const_begin_edges(self) -> BidirectionalIterator[tuple[T, T]]:
        edge_values = [(self._vertices[u], self._vertices[v]) for u, v in self._edges]
        return ConstBidirectionalIterator(edge_values)
    
    def const_rbegin_edges(self) -> BidirectionalIterator[tuple[T, T]]:
        edge_values = [(self._vertices[u], self._vertices[v]) for u, v in self._edges]
        return ConstBidirectionalIterator(edge_values, reverse=True)
    
    def begin_incident_edges(self, vertex: T) -> BidirectionalIterator[tuple[T, T]]:
        v_id = self._get_vertex_id(vertex)
        incident = []
        for u, v in self._edges:
            if u == v_id or v == v_id:
                incident.append((self._vertices[u], self._vertices[v]))
        return BidirectionalIterator(incident)
    
    def rbegin_incident_edges(self, vertex: T) -> BidirectionalIterator[tuple[T, T]]:
        v_id = self._get_vertex_id(vertex)
        incident = []
        for u, v in self._edges:
            if u == v_id or v == v_id:
                incident.append((self._vertices[u], self._vertices[v]))
        return BidirectionalIterator(incident, reverse=True)
    
    def const_begin_incident_edges(self, vertex: T) -> BidirectionalIterator[tuple[T, T]]:
        v_id = self._get_vertex_id(vertex)
        incident = []
        for u, v in self._edges:
            if u == v_id or v == v_id:
                incident.append((self._vertices[u], self._vertices[v]))
        return ConstBidirectionalIterator(incident)
    
    def const_rbegin_incident_edges(self, vertex: T) -> BidirectionalIterator[tuple[T, T]]:
        v_id = self._get_vertex_id(vertex)
        incident = []
        for u, v in self._edges:
            if u == v_id or v == v_id:
                incident.append((self._vertices[u], self._vertices[v]))
        return ConstBidirectionalIterator(incident, reverse=True)

    def begin_adjacent_vertices(self, vertex: T) -> BidirectionalIterator[T]:
        v_id = self._get_vertex_id(vertex)
        adjacent = []
        for u, v in self._edges:
            if u == v_id:
                adjacent.append(self._vertices[v])
        return BidirectionalIterator(adjacent)
    
    def rbegin_adjacent_vertices(self, vertex: T) -> BidirectionalIterator[T]:
        v_id = self._get_vertex_id(vertex)
        adjacent = []
        for u, v in self._edges:
            if u == v_id:
                adjacent.append(self._vertices[v])
        return BidirectionalIterator(adjacent, reverse=True)
    
    def const_begin_adjacent_vertices(self, vertex: T) -> BidirectionalIterator[T]:
        v_id = self._get_vertex_id(vertex)
        adjacent = []
        for u, v in self._edges:
            if u == v_id:
                adjacent.append(self._vertices[v])
        return ConstBidirectionalIterator(adjacent)
    
    def const_rbegin_adjacent_vertices(self, vertex: T) -> BidirectionalIterator[T]:
        v_id = self._get_vertex_id(vertex)
        adjacent = []
        for u, v in self._edges:
            if u == v_id:
                adjacent.append(self._vertices[v])
        return ConstBidirectionalIterator(adjacent, reverse=True)

    def __str__(self) -> str:
        from io import StringIO
        output = StringIO()

        output.write("Vertices:\n")
        for v in self.begin_vertices():
            output.write(f"  {v}\n")

        output.write("Edges:\n")
        for u, v in self.begin_edges():
            output.write(f"  {u} -> {v}\n")

        return output.getvalue().rstrip()

    def _get_vertex_id(self, value: T) -> int:
        try:
            return self._vertices.index(value)
        except ValueError:
            raise VertexNotExistsError(f"Vertex {value} not in graph")

    def has_vertex(self, value: T) -> bool:
        return value in self._vertices

    def has_edge(self, from_val: T, to_val: T) -> bool:
        try:
            u = self._get_vertex_id(from_val)
            v = self._get_vertex_id(to_val)
            return (u, v) in self._edges
        except VertexNotExistsError:
            return False

    def add_vertex(self, value: T) -> None:
        if self.has_vertex(value):
            raise VertexAlreadyExistsError(f"Vertex {value} already exists")
        v_id = len(self._vertices)
        self._vertices.append(value)

        self._incidence.append([0] * len(self._edges))

    def add_edge(self, from_val: T, to_val: T) -> None:
        if self.has_edge(from_val, to_val):
            raise EdgeAlreadyExistsError(f"Edge ({from_val} → {to_val}) already exists")
        u = self._get_vertex_id(from_val)
        v = self._get_vertex_id(to_val)
        e_id = len(self._edges)
        self._edges.append((u, v))

        for row in self._incidence:
            row.append(0)

        self._incidence[u][e_id] = -1  # исходит
        self._incidence[v][e_id] = +1  # входит

    def in_degree(self, value: T) -> int:
        v_id = self._get_vertex_id(value)
        return sum(1 for e_id in range(len(self._edges)) if self._incidence[v_id][e_id] == 1)

    def out_degree(self, value: T) -> int:
        v_id = self._get_vertex_id(value)
        return sum(1 for e_id in range(len(self._edges)) if self._incidence[v_id][e_id] == -1)
    
    def edge_degree(self, from_val: T, to_val: T) -> int:
        if not self.has_edge(from_val, to_val):
            raise EdgeNotExistsError(f"Edge ({from_val} -> {to_val}) does not exist")
    
        if from_val == to_val:
            return 1
        else:
            return 2

    def vertex_count(self) -> int:
        return len(self._vertices)

    def edge_count(self) -> int:
        return len(self._edges)

    def remove_edge(self, from_val: T, to_val: T) -> None:
        try:
            u = self._get_vertex_id(from_val)
            v = self._get_vertex_id(to_val)
        except VertexNotExistsError:
            raise EdgeNotExistsError(f"Edge ({from_val} -> {to_val}) cannot be removed: one of vertices does not exist")

        try:
            e_id = self._edges.index((u, v))
        except ValueError:
            raise EdgeNotExistsError(f"Edge ({from_val} -> {to_val}) does not exist")

        del self._edges[e_id]

        for row in self._incidence:
            del row[e_id]

    def remove_vertex(self, value: T) -> None:
        if not self.has_vertex(value):
            raise VertexNotExistsError(f"Vertex {value} does not exist")

        v_id = self._get_vertex_id(value)

        edges_to_remove = []
        for e_id, (u, v) in enumerate(self._edges):
            if u == v_id or v == v_id:
                edges_to_remove.append(e_id)

        for e_id in reversed(edges_to_remove):
            del self._edges[e_id]
            for row in self._incidence:
                del row[e_id]

        del self._incidence[v_id]

        del self._vertices[v_id]

        for i in range(len(self._edges)):
            u, v = self._edges[i]
            new_u = u - 1 if u > v_id else u
            new_v = v - 1 if v > v_id else v
            self._edges[i] = (new_u, new_v)

    

    def erase_vertex(self, it: BidirectionalIterator[T]) -> None:
        if it._container is not self._vertices:
            raise ValueError("Iterator does not belong to this graph's vertices")
        if not (0 <= it._index < len(self._vertices)):
            raise VertexNotExistsError("Iterator out of range")
        vertex_value = self._vertices[it._index]
        self.remove_vertex(vertex_value)

    def erase_edge(self, it: BidirectionalIterator[tuple[T, T]]) -> None:
        if not (0 <= it._index < len(it._container)):
            raise EdgeNotExistsError("Iterator out of range")
        from_val, to_val = it._container[it._index]
        if not self.has_edge(from_val, to_val):
            raise EdgeNotExistsError(f"Edge ({from_val} -> {to_val}) does not exist")
        self.remove_edge(from_val, to_val)