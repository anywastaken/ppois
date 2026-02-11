import pytest
from copy import deepcopy
from graph.DirectedGraphIncidence import DirectedGraphIncidence
from graph.exceptions import (
    VertexNotExistsError,
    VertexAlreadyExistsError,
    EdgeNotExistsError,
    EdgeAlreadyExistsError
)
from graph.iterators.BidirectionalIterator import BidirectionalIterator
from graph.iterators.ConstBidirectionalIterator import ConstBidirectionalIterator

# Импортируем пользовательский класс
from sort.ExampleClass import ExampleClass


class TestDirectedGraphIncidence:

    # === 1. Базовая инициализация и свойства ===
    def test_init_empty(self):
        g = DirectedGraphIncidence[str]()
        assert g.empty()
        assert g.vertex_count() == 0
        assert g.edge_count() == 0

    def test_clear(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_edge("A", "A")
        g.clear()
        assert g.empty()

    # === 2. Добавление вершин и рёбер ===
    def test_add_vertex(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        assert not g.empty()
        assert g.vertex_count() == 1
        assert g.has_vertex("A")

    def test_add_duplicate_vertex_raises(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        with pytest.raises(VertexAlreadyExistsError):
            g.add_vertex("A")

    def test_add_edge(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        assert g.edge_count() == 1
        assert g.has_edge("A", "B")

    def test_add_edge_nonexistent_vertex_raises(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        with pytest.raises(VertexNotExistsError):
            g.add_edge("A", "B")

    def test_add_duplicate_edge_raises(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        with pytest.raises(EdgeAlreadyExistsError):
            g.add_edge("A", "B")

    # === 3. Степени вершин и рёбер ===
    def test_in_out_degree(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_vertex("C")
        g.add_edge("A", "B")
        g.add_edge("C", "B")
        assert g.in_degree("B") == 2
        assert g.out_degree("A") == 1
        assert g.out_degree("B") == 0

    def test_edge_degree(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        assert g.edge_degree("A", "B") == 2

        g.add_edge("A", "A")
        assert g.edge_degree("A", "A") == 1

    # === 4. Удаление ===
    def test_remove_vertex(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        g.remove_vertex("B")
        assert g.vertex_count() == 1
        assert g.edge_count() == 0
        assert not g.has_vertex("B")

    def test_remove_nonexistent_vertex_raises(self):
        g = DirectedGraphIncidence[str]()
        with pytest.raises(VertexNotExistsError):
            g.remove_vertex("X")

    def test_remove_edge(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        g.remove_edge("A", "B")
        assert g.edge_count() == 0
        assert not g.has_edge("A", "B")

    def test_remove_nonexistent_edge_raises(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        with pytest.raises(EdgeNotExistsError):
            g.remove_edge("A", "B")

    # === 5. Итераторы: вершины ===
    def test_begin_vertices(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        assert list(g.begin_vertices()) == ["A", "B"]
        assert list(g.rbegin_vertices()) == ["B", "A"]
        assert list(g.const_begin_vertices()) == ["A", "B"]
        assert list(g.const_rbegin_vertices()) == ["B", "A"]

    # === 6. Итераторы: рёбра ===
    def test_begin_edges(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_vertex("C")
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        edges = list(g.begin_edges())
        assert edges == [("A", "B"), ("B", "C")]
        assert list(g.rbegin_edges()) == [("B", "C"), ("A", "B")]
        assert list(g.const_begin_edges()) == [("A", "B"), ("B", "C")]
        assert list(g.const_rbegin_edges()) == [("B", "C"), ("A", "B")]

    # === 7. Итераторы: инцидентные рёбра ===
    def test_begin_incident_edges(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_vertex("C")
        g.add_edge("A", "B")
        g.add_edge("C", "B")
        incident = list(g.begin_incident_edges("B"))
        assert set(incident) == {("A", "B"), ("C", "B")}
        assert list(g.rbegin_incident_edges("B")) == list(reversed(incident))
        assert list(g.const_begin_incident_edges("B")) == incident
        assert list(g.const_rbegin_incident_edges("B")) == list(reversed(incident))

    # === 8. Итераторы: смежные вершины ===
    def test_begin_adjacent_vertices(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_vertex("C")
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        adjacent = list(g.begin_adjacent_vertices("A"))
        assert set(adjacent) == {"B", "C"}
        assert list(g.rbegin_adjacent_vertices("A")) == list(reversed(adjacent))
        assert list(g.const_begin_adjacent_vertices("A")) == adjacent
        assert list(g.const_rbegin_adjacent_vertices("A")) == list(reversed(adjacent))

    # === 9. Удаление по итератору ===
    def test_erase_vertex_by_iterator(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        it = g.begin_vertices()
        g.erase_vertex(it)
        assert g.vertex_count() == 1
        assert g.has_vertex("B")
        assert not g.has_vertex("A")

    def test_erase_edge_by_iterator(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        it = g.begin_edges()
        g.erase_edge(it)
        assert g.edge_count() == 0

    # === 10. Сравнения и копирование ===
    def test_equality(self):
        g1 = DirectedGraphIncidence[str]()
        g1.add_vertex("A")
        g1.add_vertex("B")
        g1.add_edge("A", "B")

        g2 = DirectedGraphIncidence[str]()
        g2.add_vertex("A")
        g2.add_vertex("B")
        g2.add_edge("A", "B")

        g3 = DirectedGraphIncidence[str]()
        g3.add_vertex("X")

        assert g1 == g2
        assert g1 != g3

    def test_comparison_by_edge_count(self):
        g1 = DirectedGraphIncidence[str]()
        g1.add_vertex("A")
        g1.add_vertex("B")
        g1.add_edge("A", "B")

        g2 = DirectedGraphIncidence[str]()
        g2.add_vertex("X")
        g2.add_vertex("Y")
        g2.add_edge("X", "Y")
        g2.add_edge("Y", "X")

        assert g1 < g2
        assert g2 > g1
        assert g1 <= g2
        assert g2 >= g1

    def test_deepcopy(self):
        g1 = DirectedGraphIncidence[ExampleClass]()
        a = ExampleClass(10)
        b = ExampleClass(20)
        g1.add_vertex(a)
        g1.add_vertex(b)
        g1.add_edge(a, b)

        g2 = deepcopy(g1)
        assert g1 == g2
        assert g2.has_edge(a, b)
        assert g2.vertex_count() == 2

    # === 11. Вывод (__str__) ===
    def test_str_output(self):
        g = DirectedGraphIncidence[str]()
        g.add_vertex("A")
        g.add_edge("A", "A")
        output = str(g)
        assert "Vertices:" in output
        assert "Edges:" in output
        assert "A -> A" in output

    # === 12. Работа с пользовательским типом ===
    def test_custom_type(self):
        g = DirectedGraphIncidence[ExampleClass]()
        a = ExampleClass(5)
        b = ExampleClass(15)
        g.add_vertex(a)
        g.add_vertex(b)
        g.add_edge(a, b)
        assert g.has_vertex(a)
        assert g.has_edge(a, b)
        assert g.in_degree(b) == 1
        assert g.out_degree(a) == 1