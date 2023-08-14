from pairwise_traceback import _get_paths, _modify_path
#from webapp.lib.pairwise_traceback import _get_paths, _modify_path

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
        s2_alg += ' ' 
        alg += ' '

    for y in range(len(seq2)-1,j,-1):
        s2_alg = seq2[y] + s2_alg
        s1_alg += ' '
        alg += ' '
    
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

    while i > 0 and j > 0:
        s1_alg = seq1[i] + s1_alg
        s2_alg = seq2[j] + s2_alg
        alg = ' ' + alg
        i -= 1 ; j -= 1

    while i > 0:
        s1_alg = seq1[i] + s1_alg
        s2_alg = ' ' + s2_alg
        alg = ' ' + alg
        i -= 1

    while j > 0:
        s1_alg = ' ' + s1_alg
        s2_alg = seq2[j] + s2_alg
        alg = ' ' + alg
        j -= 1
    
    print('\nalignment\n',s1_alg,'\n',alg,'\n',s2_alg,'\n')

    return [s1_alg, alg, s2_alg]

# Gibt die Matrix, ALignments und den Score zurück
def get_result(sequence1: str, sequence2: str, match: float, missmatch: float, gap_penalty: float):
    seq1, seq2 = '-' + sequence1, '-' + sequence2

    traceback = [[None for j in range(len(seq2))] for i in range(len(seq1))]
    matrix = [[0 for j in range(len(seq2))] for i in range(len(seq1))]

    def is_match(a, b, match, mismatch):
        if a == b: return match
        return mismatch

    k = 0 # Bestes Score: Score der längsten gemeinsamen Teilsequenz

    # Initialisierung
    for i in range(1, len(seq1)):
        for j in range(1, len(seq2)):

            diag = matrix[i-1][j-1] + is_match(seq1[i], seq2[j], match, missmatch)
            hor = matrix[i][j-1]-gap_penalty
            vert = matrix[i-1][j]-gap_penalty
            none = 0
            maxScore = max(diag, vert, hor, none)
            matrix[i][j] = maxScore
            traceback[i][j] = traceback_value(diag, vert, hor, none)

            # setze k immer auf den maximalen Score
            if k < maxScore:
                k = maxScore
                

    #for i in matrix: print(i)
    #for j in traceback: print(j)

    # Liste von Startposition zum Traceback
    start_pos = []
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if matrix[i][j] == k: start_pos.append([i,j])
    #print(start_pos)

    # Findet Pfade 
    unmodified_paths = [_get_paths(traceback, pos) for pos in start_pos]

    #print('unmodified_paths', unmodified_paths)

    # Erstellt wieder die Liste der Startpositionen zum Traceback, weil sie nach dem Finden der Pfade geändert wird 
    start_pos = []
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if matrix[i][j] == k: start_pos.append([i,j])

    # Erstellt ein Dictionary aller Alignment und speichert in richtigen Format wie im Entwurf des Algorithmus 
    alignments = []
    for p in range(len(start_pos)):
        alignments.extend([{'alignment': get_alignment(seq1, seq2, path, start_pos[p]), 'path': _modify_path(path, start_pos[p])} for path in unmodified_paths[p]])

    score = k # Das beste Score
    #print('score',score)

    return {'matrix': matrix,
            'traceback':traceback,
            'alignments': alignments,
            'score': score}

res = get_result('fcggcggccggcagfc','atfdggcdad',2,-1,1)
print(res['alignments'])


