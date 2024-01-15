import random
import time
from typing import TypeVar, List, Callable, Dict, Tuple
from dataclasses import dataclass

T = TypeVar("T")  # represents generic type


def do_comparison(first: T, second: T, comparator: Callable[[T, T], bool], descending: bool) -> bool:
    """
    Compares two elements using the comparator function.

    param first (T): First item to compare.
    param second (T): Second item to compare.
    param comparator: A comparator function that returns True if fist should come
    before second.
    param descending: Sorts in descending order if True; defaults to False.
    return: True if first should come before second depending on comparator.
    """
    if descending:
        return comparator(second, first)
    else:
        return comparator(first, second)

def selection_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Sorts a list in-place using the selection sort algorithm.
    Uses a comparator function to determine the order of elements.
    If 'descending' is True, sorts in descending order.

    :param data: List to be sorted
    :param comparator: Function to determine the order of elements
    :param descending: If True, sorts in descending order
    """
    length = len(data)

    for i in range(length - 1):
        min = i
        for j in range (i + 1, length):
            if descending:
                if comparator(data[min], data[j]):
                    min = j
            else:
                if comparator(data[j], data[min]):
                    min = j
        data[i], data[min] = data[min], data[i]


def bubble_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                descending: bool = False) -> None:
    """
    Sorts a list in-place using the bubble sort algorithm.
    Uses a comparator function to determine the order of elements.
    If 'descending' is True, sorts in descending order.

    :param data: List to be sorted
    :param comparator: Function to determine the order of elements
    :param descending: If True, sorts in descending order
    """
    length = len(data)

    for i in range(length):
        swapped = False

        for j in range(0, length - i - 1):
            # Check if the current element should be swapped with the next element
            if descending:
                swap = comparator(data[j], data[j + 1])
            else:
                swap = comparator(data[j + 1], data[j])

            if swap:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True

        # If no two elements were swapped in the inner loop, the list is already sorted
        if not swapped:
            break

def insertion_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Sorts a list in-place using the insertion sort algorithm.
    Uses a comparator function to determine the order of elements.
    If 'descending' is True, sorts in descending order.

    :param data: List to be sorted
    :param comparator: Function to determine the order of elements
    :param descending: If True, sorts in descending order
    """
    length = len(data)

    for i in range(1, length):
        current = data[i]  # Store the current element to be inserted
        j = i - 1  # Initialize an index to traverse the sorted portion of the list

        # Determine the correct insertion position for the current element
        while j >= 0:
            if descending:
                # For descending order, move elements to the right if they are less than the current element
                if not comparator(current, data[j]):
                    data[j + 1] = data[j]  # Shift the element to the right
                    j -= 1  # Move to the previous position
                else:
                    break  # Stop when the correct position is found
            else:
                # For ascending order, move elements to the right if they are greater than the current element
                if comparator(current, data[j]):
                    data[j + 1] = data[j]  # Shift the element to the right
                    j -= 1  # Move to the previous position
                else:
                    break  # Stop when the correct position is found

        # Insert the current element into its correct position in the sorted portion
        data[j + 1] = current

def hybrid_merge_sort(data: List[T], *, threshold: int = 12,
                      comparator: Callable[[T, T], bool] = lambda x, y: x < y, descending: bool = False) -> None:
    """
    Sorts a list using a hybrid of merge sort and insertion sort algorithms.
    Uses a comparator function to determine the order of elements.
    If 'descending' is True, sorts in descending order.

    Uses insertion sort for lists smaller than 'threshold'.

    :param data: List to be sorted
    :param threshold: Size limit for using insertion sort
    :param comparator: Function to determine the order of elements
    :param descending: If True, sorts in descending order
    """

    def merge(left: List[T], right: List[T]) -> List[T]:
        merged = []
        while left and right:
            if do_comparison(left[0], right[0], comparator, descending):
                merged.append(left.pop(0))
            else:
                merged.append(right.pop(0))
        return merged + left + right

    if len(data) <= 1 or len(data) <= threshold:
        insertion_sort(data, comparator=comparator, descending=descending)
    else:
        mid = len(data) // 2
        left = data[:mid]
        right = data[mid:]

        hybrid_merge_sort(left, threshold=threshold, comparator=comparator, descending=descending)
        hybrid_merge_sort(right, threshold=threshold, comparator=comparator, descending=descending)

        data[:] = merge(left, right)


def maximize_rewards(item_prices: List[int]) -> (List[Tuple[int, int]], int):
    """
    Calculates maximum reward points from a list of item prices. Pairs items with equal sums and calculates reward points as the product of the prices in each pair. Returns an empty list and -1 if no valid pairing is possible or the list is empty.

    :param item_prices: List of item prices
    :return: A tuple containing a list of pairs and the total reward points
    """
    if len(item_prices) < 2:  # if the list is empty or has only one item
        return [], -1

    hybrid_merge_sort(item_prices)  # sort in ascending order

    pairs = []
    points = 0
    left = 0
    right = len(item_prices) - 1

    pair_sum = item_prices[left] + item_prices[right]

    while left < right:
        if item_prices[left] + item_prices[right] > pair_sum:
            right -= 1
        elif item_prices[left] + item_prices[right] < pair_sum:
            left += 1
        else:
            pairs.append((item_prices[left], item_prices[right]))
            points += item_prices[left] * item_prices[right]
            left += 1
            right -= 1

    if len(pairs) * 2 == len(item_prices):
        return pairs, points
    else:
        return [], -1


# below function given by class
def quicksort(data) -> None:
    """
    Sorts a list in place using quicksort
    :param data: Data to sort
    """

    def quicksort_inner(first, last) -> None:
        """
        Sorts portion of list at indices in interval [first, last] using quicksort

        :param first: first index of portion of data to sort
        :param last: last index of portion of data to sort
        """
        # List must already be sorted in this case
        if first >= last:
            return

        left = first
        right = last

        # Need to start by getting median of 3 to use for pivot
        # We can do this by sorting the first, middle, and last elements
        midpoint = (right - left) // 2 + left
        if data[left] > data[right]:
            data[left], data[right] = data[right], data[left]
        if data[left] > data[midpoint]:
            data[left], data[midpoint] = data[midpoint], data[left]
        if data[midpoint] > data[right]:
            data[midpoint], data[right] = data[right], data[midpoint]
        # data[midpoint] now contains the median of first, last, and middle elements
        pivot = data[midpoint]
        # First and last elements are already on right side of pivot since they are sorted
        left += 1
        right -= 1

        # Move pointers until they cross
        while left <= right:
            # Move left and right pointers until they cross or reach values which could be swapped
            # Anything < pivot must move to left side, anything > pivot must move to right side
            #
            # Not allowing one pointer to stop moving when it reached the pivot (data[left/right] == pivot)
            # could cause one pointer to move all the way to one side in the pathological case of the pivot being
            # the min or max element, leading to infinitely calling the inner function on the same indices without
            # ever swapping
            while left <= right and data[left] < pivot:
                left += 1
            while left <= right and data[right] > pivot:
                right -= 1

            # Swap, but only if pointers haven't crossed
            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1

        quicksort_inner(first, left - 1)
        quicksort_inner(left, last)

    # Perform sort in the inner function
    quicksort_inner(0, len(data) - 1)