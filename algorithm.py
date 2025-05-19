def matrix_generation(rows, cols):
    """Generate an empty matrix with given dimensions"""
    return [[0 for _ in range(cols)] for _ in range(rows)]

def matrix_printer(matrix, file=None):
    """Printer of the matrix to console with writing it to a file."""
    for i in range(len(matrix)):
        if file:
            file.write(str(matrix[i]) + '\n')
        else:
            print(matrix[i])
    if file:
        file.write('\n')
    else:
        print("")

def edge_filler(matrix, gap_penalty):
    """
    Filler of the edges of the matrix with gap penalties."""
    for j in range(2, len(matrix[0])):
        matrix[1][j] = gap_penalty * (j-1)
    for i in range(2, len(matrix)):
        matrix[i][1] = gap_penalty * (i-1)
    return matrix

def needleman_wunsch(seq1, seq2, match_score, mismatch_penalty, gap_penalty):
    """Perform Needleman-Wunsch alignment for two sequences"""
    m, n = len(seq1), len(seq2)
    score_matrix = matrix_generation(m + 1, n + 1)
    
    for i in range(m + 1):
        score_matrix[i][0] = gap_penalty * i
    for j in range(n + 1):
        score_matrix[0][j] = gap_penalty * j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score_matrix[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty)
            delete = score_matrix[i-1][j] + gap_penalty
            insert = score_matrix[i][j-1] + gap_penalty
            score_matrix[i][j] = max(match, delete, insert)
    
    # Traceback
    align1, align2 = '', ''
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and score_matrix[i][j] == score_matrix[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty):
            align1 = seq1[i-1] + align1
            align2 = seq2[j-1] + align2
            i -= 1
            j -= 1
        elif i > 0 and score_matrix[i][j] == score_matrix[i-1][j] + gap_penalty:
            align1 = seq1[i-1] + align1
            align2 = '-' + align2
            i -= 1
        else:
            align1 = '-' + align1
            align2 = seq2[j-1] + align2
            j -= 1
            
    return align1, align2


def needleman_wunsch_directions(matrix, match_score, mismatch_penalty, gap_penalty):
    """
       Function createing a directional matrix, that indicates the optimal path for alignment.
       """
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


def traceback(numeric_matrix, directional_matrix, first_sentence, second_sentence):
    """
    Performs the traceback to find the optimal alignment path.
    """
    path = []
    alignment1 = []
    alignment2 = []

    i = len(directional_matrix) - 1
    j = len(directional_matrix[0]) - 1
    biggest_number = numeric_matrix[i][j]
    for counter in range(len(directional_matrix[0]) - 1, 1, -1):
        if numeric_matrix[i][counter] > biggest_number:
            biggest_number = numeric_matrix[i][j]
            j = counter
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

        if current_direction == "DIAG" or current_direction == "DIAG_UP" or current_direction == "DIAG_LEFT" or current_direction == "DIAG_UP_LEFT":
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

def calculate_similarity_score(seq1, seq2):
    """Calculate similarity score between two sequences"""

    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be of equal length")
    
    score = 0
    for i in range(len(seq1)):
        if seq1[i] == seq2[i]:
            score += 1
    return score

def similarity_score(first_allingment, second_allingment):
    """
    Calculate the similarity score between two aligned sequences."""
    score = 0
    for i in range(len(first_allingment)):
        if first_allingment[i] == second_allingment[i]:
            score += 1
    return score/len(first_allingment)

def comparision_analyzer(first_allingment, second_allingment):
    """
    Create a string representation of the alignment comparison.
    """
    comparision = ""
    for i in range(len(first_allingment)):
        if first_allingment[i] == second_allingment[i]:
            comparision = comparision + "+"
        elif first_allingment[i] == "-" or second_allingment[i] == "-":
            comparision = comparision + "-"
        else:
            comparision = comparision + "!"
    return comparision


def find_center_sequence(sequences, match_score, mismatch_penalty, gap_penalty):
    """Find the center sequence for star alignment
    """
    n = len(sequences)
    total_scores = [0] * n
    
    for i in range(n):
        for j in range(n):
            if i != j:
                align1, align2 = needleman_wunsch(sequences[i], sequences[j], 
                                                match_score, mismatch_penalty, gap_penalty)
                total_scores[i] += calculate_similarity_score(align1, align2)
    
    center_idx = total_scores.index(max(total_scores))
    return center_idx

def mark_optimal_path(matrix, path_coordinates):
    """
    Marks the optimal path in a matrix with an indicator.
    """
    marked_matrix = [row[:] for row in matrix]

    for i, j in path_coordinates:
        if isinstance(marked_matrix[i][j], str) and len(marked_matrix[i][j]) > 1:
            marked_matrix[i][j] = f"[{marked_matrix[i][j]}]"
        else:
            marked_matrix[i][j] = f"[{marked_matrix[i][j]}]"

    return marked_matrix

def multiple_sequence_alignment(sequences, match_score, mismatch_penalty, gap_penalty):
    """Perform multiple sequence alignment using center star method"""
    if not sequences:
        return []
    
    center_idx = find_center_sequence(sequences, match_score, mismatch_penalty, gap_penalty)
    center_seq = sequences[center_idx]
    
    alignments = []
    aligned_center = []
    
    for i, seq in enumerate(sequences):
        if i != center_idx:
            center_align, other_align = needleman_wunsch(center_seq, seq, 
                                                       match_score, mismatch_penalty, gap_penalty)
            alignments.append(other_align)
            aligned_center.append(center_align)
    
    max_len = max(len(align) for align in alignments + aligned_center)
    
    final_alignments = []
    for align in alignments:
        final_alignments.append(align + '-' * (max_len - len(align)))
    
    final_alignments.insert(center_idx, center_seq + '-' * (max_len - len(center_seq)))
    
    return final_alignments

def main(sequences, match_score, mismatch_penalty, gap_penalty):
    """Main function to perform multiple sequence alignment"""
    aligned_sequences = multiple_sequence_alignment(sequences, match_score, mismatch_penalty, gap_penalty)
    
    print("\nMultiple Sequence Alignment Results:")
    for i, seq in enumerate(aligned_sequences):
        print(f"Sequence {i + 1}: {seq}")
    
    return aligned_sequences