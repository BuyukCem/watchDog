import os

def search(arr, reference):
    for i in range(len(arr)):
        if arr[i] == reference:
            return True
    return False