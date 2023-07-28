from traceback import _get_paths, _modify_path


# Gibt die Richtung/Vorgänger zurück
def traceback_value(dia, ver, hor, none):
    m_value = max(dia, ver, hor, none)

    indexes = [index for index, value in enumerate([dia, ver, hor, none]) if value == m_value]

    def _direction(index: int):
        if index == 0:
            return "diag"
        elif index == 1:
            return "vert"
        elif index == 2:
            return "hor"
        else:
            return None  ## index = 3

    if len(indexes) == 1:
        return _direction(indexes[0])
    else:
        return [_direction(i) for i in indexes]


# Gibt die Alignment zurück
def get_alignment(seq1: str, seq2: str, path: list):
    s1_alg = ""  # Alignment von Sequenz 1
    alg = ""  # Wenn die Buchstaben identisch an der selben Stelle zweier Sequenzen sind, ergibt '|', sonst ' ' (leer-Zeichen)
    s2_alg = ""  # Alignment von Sequenz 2

    # Start von ganz unten rechts (globales Alignment)
    i = len(seq1) - 1
    j = len(seq2) - 1

    # Erstellt Alignment
    for p in path:
        if p == "diag":
            s1_alg = seq1[i] + s1_alg
            s2_alg = seq2[j] + s2_alg
            alg = '|' + alg if seq1[i] == seq2[j] else ' ' + alg
            i -= 1;
            j -= 1

        elif p == "vert":
            s1_alg = seq1[i] + s1_alg
            s2_alg = "-" + s2_alg
            alg = ' ' + alg
            i -= 1

        elif p == "hor":
            s1_alg = "-" + s1_alg
            s2_alg = seq2[j] + s2_alg
            alg = ' ' + alg
            j -= 1

    return [s1_alg, alg, s2_alg]

# Gibt die Matrix, ALignments und den Score zurück
def get_result(sequence1, sequence2, match, missmatch, gap_penalty):
    seq1, seq2 = '-' + sequence1, '-' + sequence2

    traceback = [[None for j in range(len(seq2))] for i in range(len(seq1))]
    matrix = [[0 for j in range(len(seq2))] for i in range(len(seq1))]

    def is_match(a, b, match, mismatch):
        if a == b: return match
        return mismatch

    k = 0 # Score der längsten gemeinsamen Teilsequenz
    max_i = 0 # Speichert an welchem Punkt in Sequenz 1 der maximale Score ist
    max_j= 0 # Speichert an welchem Punkt in Sequenz 2 der maximale Score ist

    # Initialisierung
    for i in range(1, len(seq1)):
        for j in range(1, len(seq2)):

            diag = matrix[i-1][j-1] + is_match(seq1[i], seq2[j], match, missmatch)
            vert = matrix[i][j-1]-gap_penalty
            hor = matrix[i-1][j]-gap_penalty
            none = 0
            maxScore = max(diag, vert, hor, none)
            matrix[i][j] = maxScore
            traceback[i][j] = traceback_value(diag, vert, hor, none)

            # setze k immer auf den maximalen Score
            if k < maxScore:
                k = maxScore
                max_i = i
                max_j = j


    start_pos = [max_i, max_j]

    unmodified_paths = _get_paths(traceback, start_pos)

    alignments = [{'alignment': get_alignment(seq1, seq2, path), 'path': _modify_path(path, start_pos)} for path in
                  unmodified_paths]

    score = k

    return {'matrix': matrix,
            'alignments': alignments,
            'score': score}




