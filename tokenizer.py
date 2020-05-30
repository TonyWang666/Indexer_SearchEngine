import os
import re

STOP_WORDS = set(["a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", "there", "these", "they", "this", "to", "was", "will", "with"])
# O(n*logn)

# O(n)
# this function reads a text file and return a list of the tokens in the file
def tokenize(filename: str) -> [str]:
    tokens = []
    with open(filename, 'r') as file:  # handle open and close file
        whole_file = file.read()  # read file
        tokens += [token.lower() for token in re.split('[^a-zA-Z0-9]', whole_file) if len(token) > 3 and token not in STOP_WORDS]
        # split the line by non-alphanumeric characters, and add tokens (len > 1) to the list
    return tokens


# O(n)
# take a list and return the word counts
def computeWordFrequencies(tokens: [str]) -> {str: int}:
    token_map = {}
    for token in tokens:
        if token in token_map:
            token_map[token] += 1
        else:
            token_map[token] = 1
    return token_map