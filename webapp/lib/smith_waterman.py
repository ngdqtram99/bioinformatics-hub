#from traceback import _get_paths, _modify_path
from webapp.lib.traceback import _get_paths, _modify_path

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
def get_alignment(seq1: str, seq2: str, path: list, start_pos: list):
    s1_alg = ""  # Alignment von Sequenz 1
    alg = ""  # Wenn die Buchstaben identisch an der selben Stelle zweier Sequenzen sind, ergibt '|', sonst ' ' (leer-Zeichen)
    s2_alg = ""  # Alignment von Sequenz 2
    
    # Start von ganz unten rechts (globales Alignment)
    i = start_pos[0]
    j = start_pos[1]
    
    for x in range(len(seq1)-1,i,-1):
        s1_alg = seq1[x] + s1_alg
        s2_alg = '_' + s2_alg
        alg += '_'

    for y in range(len(seq2)-1,j,-1):
        s2_alg = seq2[y] + s2_alg
        s1_alg += '_'
        alg += '_'

    # Erstellt Alignment
    for p in path:
        if p == "diag":
            s1_alg = seq1[i] + s1_alg
            s2_alg = seq2[j] + s2_alg
            alg = '|' + alg if seq1[i] == seq2[j] else ' ' + alg
            i -= 1;
            j -= 1

    while i > 0 and j > 0:
        s1_alg = seq1[i] + s1_alg
        s2_alg = seq2[j] + s2_alg
        alg = '_' + alg
        i -= 1 ; j -= 1

    while i > 0:
        s1_alg = seq1[i] + s1_alg
        s2_alg = '_' + s2_alg
        alg = '_' + alg
        i -= 1

    while j > 0:
        s1_alg = '_' + s1_alg
        s2_alg = seq2[j] + s2_alg
        alg = '_' + alg
        j -= 1
    
    print('\nalignment\n',s1_alg,'\n',alg,'\n',s2_alg,'\n')

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
            vert = matrix[i][j-1]+gap_penalty
            hor = matrix[i-1][j]+gap_penalty
            none = 0
            maxScore = max(diag, vert, hor, none)
            matrix[i][j] = maxScore
            traceback[i][j] = traceback_value(diag, vert, hor, none)

            # setze k immer auf den maximalen Score
            if k < maxScore:
                k = maxScore
                max_i = i
                max_j = j

    #for i in matrix: print(i)
    #for j in traceback: print(j)

    start_pos = []
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if matrix[i][j] == k: start_pos.append([i,j])
    print(start_pos)

    unmodified_paths = [_get_paths(traceback, pos) for pos in start_pos]


    for i in range(len(unmodified_paths)):
        sm_paths = [] # Smith-Watermann-Path: beinhalt nur Paths, die nur diagonale Richtungen enthälten
        for path in unmodified_paths[i]:
            if 'vert' not in path and 'hor' not in path:
                sm_paths.append(path)
        unmodified_paths[i] = sm_paths
    
    #print('unmodified_paths', unmodified_paths)

    #start_pos = [max_i, max_j]

    start_pos = []
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if matrix[i][j] == k: start_pos.append([i,j])

    alignments = []
    for p in range(len(start_pos)):
        alignments.extend([{'alignment': get_alignment(seq1, seq2, path, start_pos[p]), 'path': _modify_path(path, start_pos[p])} for path in unmodified_paths[p]])

    score = k
    print('score',score)
    return {'matrix': matrix,
            'alignments': alignments,
            'score': score}

res = get_result('fcggtcggtca','ggtc',2,-1,-2)
#print(res['alignments'])


