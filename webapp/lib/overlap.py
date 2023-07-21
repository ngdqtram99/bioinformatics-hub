from pandas import DataFrame

# Konvertiert zur geschachtelte Matrix
def to_matrix(dataframe : DataFrame):
    matrix = [[' ']]
    matrix[0] += list(dataframe.columns)

    for i in dataframe.index: matrix.append([i])

    for i in range(1,len(matrix)):
        matrix[i].extend(list(dataframe.iloc[i-1]))

    return matrix

# Traceback-Wert
def traceback_value(dia,ver,hor):
    m = max(dia,ver,hor)
    if m == dia: return "dia"
    if m == ver: return "ver"
    else: return "hor"

# Gibt die Alignment zurück
def get_alignment(traceback : DataFrame, position: int):

    s1_alg = ""
    s2_alg = ""
    
    i = len(traceback.index) - 1 
    j  = position

    seq1 = traceback.index
    seq2 = traceback.columns

    # Alignment erstellen
    # Addiert Substring der Sequenz 2, die nicht zum Überlapp-Teil gehört
    for c in range(j+1, len(traceback.columns)):
        s2_alg += seq2[c]

    # Addiert die Überlapp-Substring
    while i > 0 and j > 0:
        if traceback.iloc[i][j] == "dia":
            s1_alg = seq1[i] + s1_alg
            s2_alg = seq2[j] + s2_alg
            i -= 1 ; j -= 1
        elif traceback[i][j] == "ver":
            s1_alg = seq1[i] + s1_alg
            s2_alg = "-" + s2_alg
            i -= 1
        elif traceback[i][j] == "hor":
            s1_alg = "-" + s1_alg
            s2_alg = seq2[j] + s2_alg
            j -= 1
    
    # Addiert Substring der Sequenz 1, die nicht zum Überlapp-Teil gehört
    while i > 0:
        s1_alg = seq1[i] + s1_alg
        s2_alg = '-' + s2_alg
        i -= 1
    
    return [[*s1_alg],[*s2_alg]]

# Überlapp-Algorithmus
def get_result(sequence1: str, sequence2: str, match = 1, mismatch = -1, gap_penalty = -1):
    seq1,seq2 = '-' + sequence1, '-' + sequence2

    traceback = DataFrame(None, index=[*seq1], columns=[*seq2])
    matrix = DataFrame(0, index=[*seq1], columns=[*seq2])    

    assert gap_penalty <= 0, 'gap_penalty sollte kleiner oder gleich 0 sein'
    
    #Initialisierung
    for i in range(1,len(matrix.columns)):
        matrix.loc['-'][i] = matrix.loc['-'][i-1] + gap_penalty
    
    # Berechnet Werte in der Matrix
    for i in range(1,len(matrix.index)):
        for j in range(1,len(matrix.columns)):
            s = match if matrix.index[i] == matrix.columns[j] else mismatch
            ver = matrix.iloc[i-1][j] + gap_penalty
            hor = matrix.iloc[i][j-1] + gap_penalty
            dia = matrix.iloc[i-1][j-1] + s
            
            matrix.iloc[i][j] = max(dia,ver,hor)
            traceback.iloc[i][j] = traceback_value(dia,ver,hor)
    
    # Bestes Score
    max_value = max(matrix.iloc[len(sequence1)]) 
    # Positionen des besten Score. Viele Positionen die den gleichen Score besitzen
    for i in range(len(matrix.columns)):
        if matrix.iloc[len(sequence1)][i] == max_value: 
            pos = i

    # Alignment entspricht jedes besten Score
    alignments = get_alignment(traceback, pos)

    '''	
    print(matrix)
    print(traceback)
    for i in alignments: print(i)
    '''

    return {'matrix': to_matrix(matrix),
            'alignments': alignments,
            'score': max_value}

# Beispiel
res = get_result('AAAN','ANNA')
#for i in res: print(res[i])