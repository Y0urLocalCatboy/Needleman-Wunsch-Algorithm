from enum import Enum

class Directions(Enum):
    UP = 1
    DOWN = 2
    DIAG = 3
    LEFT = 4
    RIGHT = 5

def matrix_generation(first_sentence, second_sentence):
    if isinstance(first_sentence, str) == False or isinstance(second_sentence, str) == False:
        raise TypeError("One of the inputs is not a string.")
    if len(first_sentence) == 0 or len(second_sentence) == 0:
        raise ValueError("One of the sentences are empty.")
    first_sentence = "  " + first_sentence
    second_sentence = "  " + second_sentence
    matrix = [[0 for x in range(len(second_sentence))] for y in range(len(first_sentence))]
    for i in range(len(first_sentence)):
        matrix[i][0] = first_sentence[i]
    for j in range(len(second_sentence)):
        matrix[0][j] = second_sentence[j]
    return matrix

def matrix_printer(matrix):
    for i in range(len(matrix)):
        print(matrix[i])

def edge_filler(matrix, gap_penalty):
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            matrix[i][1] = gap_penalty * i
            matrix[1][j] = gap_penalty * j
            # if i == 1 and j == 1:
            #     matrix[i][j] = 0
            # elif matrix[i][0] == matrix[0][j]:
            #     matrix[i][j] = matrix[i][j] + 1
            # else:
            #     matrix[i][j] = matrix[i][j] + missmatch
    return matrix


def needleman_wunsch(matrix, match_score, mismatch_penalty, gap_penalty):
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(2, rows):
        for j in range(2, cols):
            if isinstance(matrix[i][0], str) and isinstance(matrix[0][j], str):
                if matrix[i][0] == matrix[0][j]:
                    score = match_score
                else:
                    score = mismatch_penalty

                match = matrix[i - 1][j - 1] + score
                delete = matrix[i - 1][j] + gap_penalty
                insert = matrix[i][j - 1] + gap_penalty

                matrix[i][j] = max(match, delete, insert)

    return matrix


matrix = matrix_generation("CTCGCAGC ", "CATTCAC")
matrix = edge_filler(matrix, -5)
matrix = needleman_wunsch(matrix, 10, -2, -5)
matrix_printer(matrix)