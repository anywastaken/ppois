
class PigeonholeSort:
    def pigeonhole_sort(self, arr):
        if not arr:
            return arr

        values = [x.value for x in arr]
        min_val = min(values)
        max_val = max(values)
        size = max_val - min_val + 1

        pigeon_holes = [[] for _ in range(size)]

        for obj in arr:
            index = obj.value - min_val
            pigeon_holes[index].append(obj)

        result = []
        for hole in pigeon_holes:
            result.extend(hole)

        return result