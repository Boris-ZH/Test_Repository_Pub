def binary_search(array, element, left, right):
    if left > right:
            return False
    middle = (right + left) // 2
    if element == array[middle]:
        if array[middle - 1] < element and element <= array[middle]:
            return middle
        elif element < array[middle]:
            return binary_search(array, element, left, middle - 1)
    elif element == array[middle - 1]:
            return binary_search(array, element, left, middle - 1)
    else:
            return binary_search(array, element, middle + 1, right)
array = list(map(int, input("Введите целые числа через пробел: ").split()))
element = int(input("Введите любое число из списка: "))
array = sorted(array)
print(array)
left = int(array[0])
right = int(array[-1])
if element < left or element > right:
    print('Числа нет в диапазоне')
else:
    print(binary_search(array, element, 0, len(array) - 1))