from enum import Enum

class Directions(Enum):
    UP = '^'
    DOWN = 'v'
    DIAG = '/'
    LEFT = '<'
    RIGHT = '>'

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
    for i in range(2, len(matrix)):
        for j in range(2, len(matrix[i])):
            matrix[i][1] = gap_penalty * (i-1)
            matrix[1][j] = gap_penalty * (j-1)
            # if i == 1 and j == 1:
            #     matrix[i][j] = 0
            # elif matrix[i][0] == matrix[0][j]:
            #     matrix[i][j] = matrix[i][j] + 1
            # else:
            #     matrix[i][j] = matrix[i][j] + missmatch
    return matrix

def needleman_wunsch(first_sentence, second_sentence, match_score, mismatch_penalty, gap_penalty):
    matrix = edge_filler(matrix_generation(first_sentence, second_sentence), gap_penalty)

    matrix = edge_filler(matrix, gap_penalty)

    for i in range(2, len(matrix)):
        for j in range(2, len(matrix[0])):
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

def needleman_wunsch_directions(matrix):

    directional_matrix = [[' ' for x in range(len(matrix[0]))] for y in range(len(matrix))]
    gap_penalty = -5
    match_score = 10
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[0])):
            if i>=2 and j>=2:
                if matrix[i][j] == matrix[i-1][j] + gap_penalty:
                    directional_matrix[i][j] = Directions.UP
                elif matrix[i][j] == matrix[i][j-1] + gap_penalty:
                    directional_matrix[i][j] = Directions.LEFT
                elif matrix[i][j] == matrix[i-1][j-1] + match_score:
                    directional_matrix[i][j] = Directions.DIAG
                else:
                    directional_matrix[i][j] = Directions.DOWN

    return directional_matrix
matrix = needleman_wunsch("CATTCAC","CTCGCAGC", 10, -2, -5)
matrix_printer(matrix)
matrix = needleman_wunsch_directions(matrix)
matrix_printer(matrix)