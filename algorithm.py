def matrix_generation(first_sentence, second_sentence):

    if isinstance(first_sentence, str) == False or isinstance(second_sentence, str) == False:
        raise TypeError("One of the inputs is not a string.")
    if len(first_sentence) == 0 or len(second_sentence) == 0:
        raise ValueError("One of the sentences are empty.")

    first_sentence = "X_" + first_sentence
    second_sentence = "X_" + second_sentence
    matrix = [[0 for x in range(len(second_sentence))] for y in range(len(first_sentence))]
    for i in range(len(first_sentence)):
        matrix[i][0] = first_sentence[i]
    for j in range(len(second_sentence)):
        matrix[0][j] = second_sentence[j]
    return matrix

def matrix_printer(matrix):
    for i in range(len(matrix)):
        print(matrix[i])
    print("")

def edge_filler(matrix, gap_penalty):
    for i in range(2, len(matrix)):
        for j in range(2, len(matrix[i])):
            matrix[i][1] = gap_penalty * (i-1)
            matrix[1][j] = gap_penalty * (j-1)
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


def needleman_wunsch_directions(matrix, match_score, mismatch_penalty, gap_penalty):
    directional_matrix = [[' ' for x in range(len(matrix[0]))] for y in range(len(matrix))]

    for i in range(len(matrix)):
        directional_matrix[i][0] = matrix[i][0]
    for j in range(len(matrix[0])):
        directional_matrix[0][j] = matrix[0][j]

    for j in range(2, len(matrix[0])):
        directional_matrix[1][j] = "LEFT"
    for i in range(2, len(matrix)):
        directional_matrix[i][1] = "UP"

    directional_matrix[1][1] = 0

    for i in range(2, len(matrix)):
        for j in range(2, len(matrix[0])):
            diagonal = matrix[i - 1][j - 1]
            up = matrix[i - 1][j]
            left = matrix[i][j - 1]

            if matrix[i][0] == matrix[0][j]:
                diag_score = diagonal + match_score
            else:
                diag_score = diagonal + mismatch_penalty

            up_score = up + gap_penalty
            left_score = left + gap_penalty

            max_score = max(diag_score, up_score, left_score)
            if diag_score == left_score == up_score:
                directional_matrix[i][j] = "DIAG_UP_LEFT"
            elif diag_score == up_score and diag_score > left_score:
                directional_matrix[i][j] = "DIAG_UP"
            elif diag_score == left_score and diag_score > up_score:
                directional_matrix[i][j] = "DIAG_LEFT"
            elif up_score == left_score and up_score > diag_score:
                directional_matrix[i][j] = "UP_LEFT"
            elif max_score == diag_score:
                directional_matrix[i][j] = "DIAG"
            elif max_score == up_score:
                directional_matrix[i][j] = "UP"
            else:
                directional_matrix[i][j] = "LEFT"


    return directional_matrix


def traceback(directional_matrix, first_sentence, second_sentence):
    path = []
    alignment1 = []
    alignment2 = []

    i = len(directional_matrix) - 1
    j = len(directional_matrix[0]) - 1

    while i > 1 or j > 1:
        current_direction = directional_matrix[i][j]

        if current_direction == 0:
            i -= 1
            j -= 1
            continue

        path.append(current_direction)

        if i <= 1 < j:
            alignment1.append('-')
            alignment2.append(second_sentence[j-2])
            j -= 1
            continue
        elif j <= 1 < i:
            alignment1.append(first_sentence[i-2])
            alignment2.append('-')
            i -= 1
            continue

        if current_direction == "DIAG" or current_direction == "DIAG_UP" or current_direction == "DIAG_LEFT":
            alignment1.append(first_sentence[i-2])
            alignment2.append(second_sentence[j-2])
            i -= 1
            j -= 1
        elif current_direction == "UP" or current_direction == "UP_LEFT":
            alignment1.append(first_sentence[i-2])
            alignment2.append('-')
            i -= 1
        elif current_direction == "LEFT":
            alignment1.append('-')
            alignment2.append(second_sentence[j-2])
            j -= 1

    path.reverse()
    alignment1.reverse()
    alignment2.reverse()

    return path, ''.join(alignment1), ''.join(alignment2)

def similarity_score(first_allingment, second_allingment):
    score = 0
    for i in range(len(first_allingment)):
        if first_allingment[i] == second_allingment[i]:
            score += 1
    return score/len(first_allingment)
def comparision_analyzer(first_allingment, second_allingment):
    comparision = ""
    for i in range(len(first_allingment)):
        if first_allingment[i] == second_allingment[i]:
            comparision = comparision + "*"
        elif first_allingment[i] == "-" or second_allingment[i] == "-":
            comparision = comparision + "-"
        else:
            comparision = comparision + "!"
    return comparision
def main(first_sentence, second_sentence, match_score, mismatch_penalty, gap_penalty):
    matrix = needleman_wunsch(first_sentence, second_sentence, match_score, mismatch_penalty, gap_penalty)
    matrix_printer(matrix)
    matrix = needleman_wunsch_directions(matrix, match_score, mismatch_penalty, gap_penalty)
    matrix_printer(matrix)

    path, aligned_seq1, aligned_seq2 = traceback(matrix, first_sentence, second_sentence)

    print("Path:", path)
    print("1:", aligned_seq1)
    print("2:", aligned_seq2)
    print("Match score:", (similarity_score(aligned_seq1, aligned_seq2) * 100).__round__(2), "%")
    print("Comparision:", comparision_analyzer(aligned_seq1, aligned_seq2))
