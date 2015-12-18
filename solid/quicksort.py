import unittest

def my_quicksort(array):
    # assert len(array) > 0, "The array is empty. "
    if len(array) <= 1: return array
    pivot = array[0]
    i = 1 # [i:] stores elems >= pivot
    for j in range(len(array)):
        if array[j] < pivot:
            if i!=j: array[i],array[j] = array[j], array[i]
            i += 1
    array[0], array[i-1] = array[i-1], array[0]
    return my_quicksort(array[0:i-1]) + [pivot] + my_quicksort(array[i:])

def simple_quicksort(array):
    less = []; greater = []
    if len(array) <= 1: return array
    pivot = array.pop()
    for x in array:
        #if x <= pivot: less.append(x) # the same as `<`
        #else: greater.append(x)
        if x < pivot: less.append(x)
        else: greater.append(x)
    return simple_quicksort(less) + [pivot] + simple_quicksort(greater)

class TestQuickSort(unittest.TestCase):

    def setUp(self):
        self.array = [9,8,4,5,32,64,2,1,0,10,19,27]

    def test_quicksort(self):
        print my_quicksort(self.array)
        self.assertEqual(my_quicksort(self.array), [0,1,2,4,5,8,9,10,19,27,32,64])
        print my_quicksort([1,3,2,4,5,2,1,7])
        self.assertEqual(my_quicksort([1,3,2,4,5,2,1,7]), [1,1,2,2,3,4,5,7])
        self.assertEqual(simple_quicksort(self.array), [0,1,2,4,5,8,9,10,19,27,32,64])

if __name__ == "__main__":
    unittest.main()
