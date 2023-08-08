# Traceback-Wert
def traceback_value(dia,ver,hor, similarity : bool):
    
    m = max(dia,ver,hor) if similarity else min(dia,ver,hor)
    if m == dia: return "dia"
    if m == ver: return "ver"
    else: return "hor"

# Gibt die Alignment zurück
def get_alignment(sequence1 : str, sequence2 : str, traceback : list, position: int):

    s1_alg = ""
    s2_alg = ""
    
    i = len(traceback) - 1
    j  = position

    # Alignment erstellen
    # Addiert Substring der Sequenz 2, die nicht zum Überlapp-Teil gehört
    for pos in range(j+1, len(sequence2)):
        s2_alg += sequence2[pos]

    # Addiert die Überlapp-Substring
    while i > 0 and j > 0:
        if traceback[i][j] == "dia":
            s1_alg = sequence1[i] + s1_alg
            s2_alg = sequence2[j] + s2_alg
            i -= 1 ; j -= 1
        elif traceback[i][j] == "ver":
            s1_alg = sequence1[i] + s1_alg
            s2_alg = "-" + s2_alg
            i -= 1
        elif traceback[i][j] == "hor":
            s1_alg = "-" + s1_alg
            s2_alg = sequence2[j] + s2_alg
            j -= 1

    # Addiert Substring der Sequenz 1, die nicht zum Überlapp-Teil gehört
    while i > 0:
        s1_alg = sequence1[i] + s1_alg
        s2_alg = '-' + s2_alg
        i -= 1

    return [[*s1_alg],[*s2_alg]]

# Überlapp-Algorithmus
def get_result(sequence1: str, sequence2: str, match: float, mismatch: float, gap_penalty:float, similarity: bool):
    seq1,seq2 = '-' + sequence1, '-' + sequence2

    traceback = [[None for j in range(len(seq2))] for i in range(len(seq1))]
    matrix = [[0 for j in range(len(seq2))] for i in range(len(seq1))]
    
    #Initialisierung
    for i in range(1,len(seq2)):
        matrix[0][i] = matrix[0][i-1] + gap_penalty

    # Berechnet Werte in der Matrix
    for i in range(1,len(seq1)):
        for j in range(1,len(seq2)):
            s = match if seq1[i] == seq2[j] else mismatch
            
            ver = matrix[i-1][j] + gap_penalty
            hor = matrix[i][j-1] + gap_penalty
            dia = matrix[i-1][j-1] + s
            
            matrix[i][j] = max(dia,ver,hor) if similarity else min(dia,ver,hor)
            
            traceback[i][j] = traceback_value(dia,ver,hor,similarity)
    
    # Bestes Score der letzten Zeile der Scorematrix
    max_value = max(matrix[-1]) 
    # Positionen des besten Score. Weil es möglich ist, viele Positionen den selben Score besitzen, behält die Methode nur die im Matrix ganz rechten Position 
    for i in range(len(seq2)):
        if matrix[-1][i] == max_value: 
            pos = i

    # Alignment entspricht jedes besten Score
    alignments = get_alignment(seq1, seq2, traceback, pos)

    '''
    print(matrix)
    print(traceback)
    for i in alignments: print(i)
    '''

    return {'matrix': matrix,
            'alignments': alignments,
            'score': max_value}

# Beispiel
res = get_result('AAAN','ANNA', 2, -1 ,-2, True)
for i in res: print(res[i])