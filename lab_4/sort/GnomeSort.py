

class GnomeSort:
    def gnome_sort(self, arr):
        i = 1
        while i < len(arr):
            if i > 0 and arr[i - 1] > arr[i]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                i -= 1
            else:
                i += 1
        return arr