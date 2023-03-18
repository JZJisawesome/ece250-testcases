#This script was provided by the ECE 250 Teaching Staff under the MIT License. Thanks! - JZJ
import sys
import difflib
import re

#determines if a string has only numbers in it
def is_numeric_string(s):
    values = s.strip().split()  # split the string into individual values
    for value in values:
        if not value.isnumeric():  # check if each value is numeric
            return False
    return True

"""
Check if two strings of space-separated numbers are identical when sorted.

Args:
    str1 (str): The first string of space-separated numbers.
    str2 (str): The second string of space-separated numbers.

Returns:
    bool: True if the two sorted lists of numbers are identical, False otherwise.
"""
def is_sorted_list_equal(str1, str2):
    #if both are numeric lists, check equality
    if(is_numeric_string(str1) and is_numeric_string(str2)):
        list1 = sorted(str1.split())
        list2 = sorted(str2.split())

        return list1 == list2
        
    #one of them isn't a numeric list, so clearly they can't be sorted and equal!
    return False


#parses a string into triples. This way we can parse strings into a graph
def parse_numeric_triples(s):
    values = s.strip().split()  # split the string into individual values
    n = len(values)
    if n % 3 != 0:
        raise ValueError("Input string does not contain a multiple of 3 values")
    triples = []
    for i in range(0, n, 3):
        try:
            x = float(values[i])
            y = float(values[i+1])
            z = float(values[i+2])
        except ValueError:
            raise ValueError("Invalid value found in input string")
        triples.append((x, y, z))
    return triples

#pre-sort the triples to ensure that the output will make sense
def swap_elements(triples):
    for i in range(len(triples)):
        if triples[i][1] < triples[i][0]:
            triples[i] = (triples[i][1], triples[i][0], triples[i][2])


#Sorts the triples by first, then second, then third
def sort_numeric_triples(triples):
    swap_elements(triples)
    triples.sort(key=lambda x: (x[0], x[1], x[2]))

"""
Check if two lists of triples contain the same triples.

Args:
- triples1: A list of triples, each triple is a tuple of three elements
- triples2: A list of triples, each triple is a tuple of three elements

Returns:
- A boolean indicating whether the two lists contain the same triples
"""
def same_triples(triples1, triples2):
    # Check if the lists have the same length
    if len(triples1) != len(triples2):
        return False
    
    # Check if each triple in triples1 is also in triples2
    for triple in triples1:
        if triple not in triples2:
            return False
    
    # Check if each triple in triples2 is also in triples1
    for triple in triples2:
        if triple not in triples1:
            return False
    
    # If we made it here, the lists must contain the same triples
    return True


#determines if two strings match within threshold using the edit distance
def string_match(str1, str2, threshold):
    seq_match = difflib.SequenceMatcher(None, str1.strip(), str2.strip())
    similarity = seq_match.ratio()
    return similarity >= threshold

def compute_threshold(s, N):
    """
    Compute a threshold value based on the input string s and an integer N.
    The threshold value represents the maximum allowed edit distance if N characters in the input string were different.
    """
    n = len(s)
    if n == 0:
        return 0.0

    # Compute the maximum number of allowed edits based on the length of the string and the value of N
    max_edits = min(n, N)

    # Compute the minimum ratio of matching characters required to consider the strings a match
    min_ratio = 1.0 - float(max_edits) / n

    # Compute the threshold based on the minimum ratio and the length of the string
    threshold = difflib.SequenceMatcher(None, s, s).real_quick_ratio() * min_ratio
    
    #the "fiddle" here is because this threshold is exact, but represented as floating point. This would mean an additional 1% difference is allowed
    fiddle = 0.01
    return threshold - fiddle

#this checks if the numbers match in a given pair of strings
def check_numbers_match(s1, s2):
    """
    Check if the numbers in two strings match exactly, for all numbers in the string.

    Args:
    s1 (str): First string to check.
    s2 (str): Second string to check.

    Returns:
    bool: True if the numbers in the strings match exactly, False otherwise.
    """
    regex = r"\d+"
    nums1 = list(map(int, re.findall(regex, s1))) if re.search(regex, s1) else []
    nums2 = list(map(int, re.findall(regex, s2))) if re.search(regex, s2) else []
    return nums1 == nums2

"""
    Returns the first value in a space-separated string.
    This is used when parsing an input file in the auto-grader: we remove
    the command from the input line, and then grade accordingly
"""    
def get_first_value(string):
    # Split the string into a list of values using spaces as the delimiter
    values = string.split()

    # Return the first value in the list
    return values[0]
