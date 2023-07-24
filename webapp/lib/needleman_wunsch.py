from traceback import _get_paths, _modify_path
#from webapp.lib.traceback import _get_paths, _modify_path

# Gibt die Richtung/Vorgänger zurück
def traceback_value(dia,ver,hor, similarity : bool):
    m_value = max(dia,ver,hor) if similarity else min(dia,ver,hor)

    indexes = [index for index, value in enumerate([dia, ver, hor]) if value == m_value]

    def _direction(index : int):
        if index == 0: return "diag"
        elif index == 1: return "vert"
        else: return "hor" ## index = 2
    
    if len(indexes) == 1: return _direction(indexes[0])
    else: return [_direction(i) for i in indexes]
    
# Beispiel 
#print(traceback_value(4,3,4,True))
#print(traceback_value(3,6,5,True))

#---------------------------------
# Gibt die Alignment zurück
def get_alignment(seq1 : str, seq2: str, path : list): # Sequenzen ohne - am Anfang

    s1_alg = "" # Alignment von Sequenz 1
    alg = "" # Wenn die Buchstaben identisch an der selben Stelle zweier Sequenzen sind, ergibt '|', sonst ' ' (leer-Zeichen)
    s2_alg = "" # Alignment von Sequenz 2
    
    # Start von ganz unten rechts (globales Alignment)
    i = len(seq1)-1
    j  = len(seq2)-1

    # Erstellt Alignment
    for p in path: 
        if p == "diag":
            s1_alg = seq1[i] + s1_alg
            s2_alg = seq2[j] + s2_alg
            alg = '|' + alg if seq1[i] == seq2[j] else ' ' + alg
            i -= 1 ; j -= 1

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


    return [s1_alg,alg,s2_alg]

# Beispiel
#alignment = get_alignment('aatcg','aacg', ['diag', 'diag', 'vert', 'diag', 'diag'])
#for i in alignment: print(i)



# Needlemann-Wunsch-Algorithmus
def get_result(sequence1: str, sequence2: str, match : int, mismatch : int, gap_penalty : int, similarity : bool):
    seq1,seq2 = '-' + sequence1, '-' + sequence2

    traceback = [[None for j in range(len(seq2))] for i in range(len(seq1))]
    matrix = [[0 for j in range(len(seq2))] for i in range(len(seq1))]   
    
    #Initialisierung
    for j in range(1,len(seq2)): 
        matrix[0][j] = matrix[0][j-1] + gap_penalty
        traceback[0][j] = "hor"

    for i in range(1,len(seq1)): 
        matrix[i][0] = matrix[i-1][0] + gap_penalty 
        traceback[i][0] = "vert"
    
    # Gibt (Mis)-Match zurück, wenn die verglichen Buchstaben (nicht) identisch sind
    def is_match(a, b, match, mismatch):
        if a == b: return match
        return mismatch
    
    # Berechnet Werte in der Matrix
    for i in range(1,len(seq1)):
        for j in range(1,len(seq2)):
            ver = matrix[i-1][j] + gap_penalty
            hor = matrix[i][j-1] + gap_penalty
            dia = matrix[i-1][j-1] + is_match(seq1[i],seq2[j],match,mismatch)
            
            matrix[i][j] = max(dia,ver,hor) if similarity else min(dia,ver,hor)
            traceback[i][j] = traceback_value(dia,ver,hor, similarity)
    
    # Score
    score = matrix[len(seq1)-1][len(seq2)-1]

    # Alignment entspricht jedes besten Score
    start_pos = [len(seq1[1:]), len(seq2[1:])] # Start-Position zum Traceback (die ganz unten rechte Position) 
    
    '''
    print('traceback')
    for i in traceback: print(i)
    '''

    unmodified_paths = _get_paths(traceback, start_pos)

    '''
    print('unmodified_paths')
    for i in unmodified_paths: print(i)
    '''

    start_pos = [len(seq1[1:]), len(seq2[1:])] # Nach der Modifikation wird start_pos zu [0,0] gesetzt, deswegen muss es hier wieder richtig umgesetzt
    alignments = [{'alignment':get_alignment(seq1[1:],seq2[1:],path),'path':_modify_path(path,start_pos)} for path in unmodified_paths]
    
    '''
    print('alignments')
    for i in alignments: print(i)
    '''
    
    return {'matrix': matrix,
            'alignments': alignments,
            'score': score}
    
# Beispiel
res = get_result('actg','aacg',2,-1,-2,True)
#for i in res: print(res[i])
'''
[[0, -2, -4, -6, -8], 
 [-2, 2, 0, -2, -4], 
 [-4, 0, 1, 2, 0], 
 [-6, -2, -1, 0, 1], 
 [-8, -4, -3, -2, 2]]

[{'alignment': ['actg', '|  |', 'aacg'], 'path': [[[4, 4], 'diag'], [[3, 3], 'diag'], [[2, 2], 'diag'], [[1, 1], 'diag'], [[0, 0]]]}, 
{'alignment': ['-actg', ' || |', 'aac-g'], 'path': [[[4, 4], 'diag'], [[3, 3], 'vert'], [[2, 3], 'diag'], [[1, 2], 'diag'], [[0, 1], 'hor'], [[0, 0]]]}, 
{'alignment': ['a-ctg', '| | |', 'aac-g'], 'path': [[[4, 4], 'diag'], [[3, 3], 'vert'], [[2, 3], 'diag'], [[1, 2], 'hor'], [[1, 1], 'diag'], [[0, 0]]]}] 2

2
'''