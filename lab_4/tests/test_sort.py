import pytest
from sort.ExampleClass import ExampleClass
from sort.GnomeSort import GnomeSort
from sort.PigeonholeSort import PigeonholeSort


class TestGnomeSort:

    def test_gnome_sort_empty(self):
        sorter = GnomeSort()
        arr = []
        result = sorter.gnome_sort(arr)
        assert result == []

    def test_gnome_sort_single(self):
        sorter = GnomeSort()
        arr = [ExampleClass(5)]
        result = sorter.gnome_sort(arr)
        assert result == [ExampleClass(5)]

    def test_gnome_sort_already_sorted(self):
        sorter = GnomeSort()
        arr = [ExampleClass(1), ExampleClass(2), ExampleClass(3)]
        result = sorter.gnome_sort(arr)
        assert result == [ExampleClass(1), ExampleClass(2), ExampleClass(3)]

    def test_gnome_sort_reverse_sorted(self):
        sorter = GnomeSort()
        arr = [ExampleClass(3), ExampleClass(2), ExampleClass(1)]
        result = sorter.gnome_sort(arr)
        assert result == [ExampleClass(1), ExampleClass(2), ExampleClass(3)]

    def test_gnome_sort_random_order(self):
        sorter = GnomeSort()
        arr = [ExampleClass(5), ExampleClass(2), ExampleClass(8), ExampleClass(1)]
        result = sorter.gnome_sort(arr)
        expected = [ExampleClass(1), ExampleClass(2), ExampleClass(5), ExampleClass(8)]
        assert result == expected

    def test_gnome_sort_with_duplicates(self):
        sorter = GnomeSort()
        arr = [ExampleClass(3), ExampleClass(1), ExampleClass(3), ExampleClass(2)]
        result = sorter.gnome_sort(arr)
        expected = [ExampleClass(1), ExampleClass(2), ExampleClass(3), ExampleClass(3)]
        assert result == expected


class TestPigeonholeSort:

    def test_pigeonhole_sort_empty(self):
        sorter = PigeonholeSort()
        arr = []
        result = sorter.pigeonhole_sort(arr)
        assert result == []

    def test_pigeonhole_sort_single(self):
        sorter = PigeonholeSort()
        arr = [ExampleClass(10)]
        result = sorter.pigeonhole_sort(arr)
        assert result == [ExampleClass(10)]

    def test_pigeonhole_sort_already_sorted(self):
        sorter = PigeonholeSort()
        arr = [ExampleClass(1), ExampleClass(2), ExampleClass(3)]
        result = sorter.pigeonhole_sort(arr)
        assert result == [ExampleClass(1), ExampleClass(2), ExampleClass(3)]

    def test_pigeonhole_sort_reverse_sorted(self):
        sorter = PigeonholeSort()
        arr = [ExampleClass(5), ExampleClass(3), ExampleClass(1)]
        result = sorter.pigeonhole_sort(arr)
        assert result == [ExampleClass(1), ExampleClass(3), ExampleClass(5)]

    def test_pigeonhole_sort_random_order(self):
        sorter = PigeonholeSort()
        arr = [ExampleClass(7), ExampleClass(2), ExampleClass(9), ExampleClass(4)]
        result = sorter.pigeonhole_sort(arr)
        expected = [ExampleClass(2), ExampleClass(4), ExampleClass(7), ExampleClass(9)]
        assert result == expected

    def test_pigeonhole_sort_with_duplicates(self):
        sorter = PigeonholeSort()
        arr = [ExampleClass(4), ExampleClass(1), ExampleClass(4), ExampleClass(3)]
        result = sorter.pigeonhole_sort(arr)
        expected = [ExampleClass(1), ExampleClass(3), ExampleClass(4), ExampleClass(4)]
        assert result == expected

    def test_pigeonhole_sort_negative_values(self):
        sorter = PigeonholeSort()
        arr = [ExampleClass(-2), ExampleClass(3), ExampleClass(0), ExampleClass(-5)]
        result = sorter.pigeonhole_sort(arr)
        expected = [ExampleClass(-5), ExampleClass(-2), ExampleClass(0), ExampleClass(3)]
        assert result == expected


# === Дополнительный тест: сравнение с встроенной сортировкой ===
def test_gnome_vs_builtin():
    arr = [ExampleClass(v) for v in [10, 3, 7, 1, 9, 4]]
    expected = sorted(arr, key=lambda x: x.value)
    gnome = GnomeSort().gnome_sort(arr.copy())
    assert gnome == expected


def test_pigeonhole_vs_builtin():
    arr = [ExampleClass(v) for v in [8, 2, 5, 2, 9, 1]]
    expected = sorted(arr, key=lambda x: x.value)
    pigeon = PigeonholeSort().pigeonhole_sort(arr.copy())
    assert pigeon == expected