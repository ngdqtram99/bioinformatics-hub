#from traceback import _get_paths, _modify_path
from webapp.lib.traceback import _get_paths, _modify_path

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
def get_alignment(seq1 : str, seq2: str, path : list, start_pos : list):

    s1_alg = "" # Alignment von Sequenz 1
    alg = "" # Wenn die Buchstaben identisch an der selben Stelle zweier Sequenzen sind, ergibt '|', sonst ' ' (leer-Zeichen)
    s2_alg = "" # Alignment von Sequenz 2
    
    # Start von ganz unten rechts (globales Alignment)
    i = start_pos[0]
    j  = start_pos[1]

    assert j == len(seq2)-1, 'Die Position kommt nicht aus der letzten Spalte'
    
    for x in range(len(seq1)-1,i,-1):
        s1_alg = seq1[x] + s1_alg
        s2_alg += '_'
        alg += ' '
    

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

    while i > 0:
        s1_alg = seq1[i] + s1_alg
        s2_alg = '_' + s2_alg
        alg = ' ' + alg
        i -= 1

    print('alignment\n',s1_alg,'\n',alg,'\n',s2_alg)
    
    return [s1_alg,alg,s2_alg]

# Beispiel
#alignment = get_alignment('aatcg','aacg', ['diag', 'diag', 'vert', 'diag', 'diag'])
#for i in alignment: print(i)


# Glokal-Algorithmus
def get_result(sequence1: str, sequence2: str, match: float, mismatch: float, gap_penalty: float, similarity : bool):
    # Sequenz 1 ist String und Sequenz 2 ist Pattern

    seq1,seq2 = '-' + sequence1, '-' + sequence2

    traceback = [[None for j in range(len(seq2))] for i in range(len(seq1))]
    matrix = [[0 for j in range(len(seq2))] for i in range(len(seq1))]   
    
    #Initialisierung
    for j in range(1,len(seq2)): 
        matrix[0][j] = matrix[0][j-1] + gap_penalty
        traceback[0][j] = "hor"

    
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
    
    '''
    print('matrix')
    for i in matrix: print(i)
    print('traceback')
    for i in traceback: print(i)
    '''

    # Die besten Scores und ihre Positionen
    last_col = [i[-1] for i in matrix] # Letzt Spalte der Scorematrix
    best_scores = []
    best_scores_pos = []
    
    # Addiert das beste Score (max./min. Werte abhängig von der Ähnlichkeit)
    best_scores.append(max(last_col)) if similarity else best_scores.append(min(last_col)) 
    tem_last_col = last_col.copy()
    for i in range(len(last_col)): # Addiert Position(en) des besten Scores
        if last_col[i] == best_scores[-1]:
            best_scores_pos.append(i)
        
            # Löscht das gerade gefundene beste Score, um das zweite beste Score zu finden
            tem_last_col.remove(best_scores[-1])
    
    assert len(last_col) > len(tem_last_col), 'Temporale last_col sollte keine das besten Score enthalten'
    
    if similarity and max(tem_last_col) >= best_scores[-1] - 2:
        best_scores.append(max(tem_last_col)) # Addiert das zweite beste Score
    
        for i in range(len(last_col)): # Addiert Position(en) des zweiten besten Scores
            if last_col[i] == best_scores[-1]:
                best_scores_pos.append(i)
    
    elif not similarity and min(tem_last_col) <= best_scores[-1] + 2:
        best_scores.append(min(tem_last_col)) # Addiert das zweite beste Score
    
        for i in range(len(last_col)): # Addiert Position(en) des zweiten besten Scores
            if last_col[i] == best_scores[-1]:
                best_scores_pos.append(i)
    
    #print('best_scores',best_scores)

    # Start-Position zum Traceback (die ganz unten rechte Position)  
    list_start_pos = [[i,len(sequence2)] for i in best_scores_pos] 
    

    unmodified_paths = [_get_paths(traceback, start_pos) for start_pos in list_start_pos]

    '''
    print('unmodified_paths')
    for i in unmodified_paths: print(i)
    '''

    # Nach der Modifikation werden alle start_pos zu [0,0] gesetzt, deswegen muss es hier wieder richtig umgesetzt
    list_start_pos = [[i,len(sequence2)] for i in best_scores_pos] 
    alignments = []

    for i in range(len(list_start_pos)):
        alignments.extend([{'alignment':get_alignment(seq1,seq2,path, list_start_pos[i]),'path':_modify_path(path,list_start_pos[i])} for path in unmodified_paths[i]])    
    '''
    print('alignments')
    for i in alignments: print(i)
    '''
    return {'matrix': matrix,
            'alignments': alignments,
            'score': best_scores}
    
# Beispiel
res = get_result('PXPO-YXPONY','PONY',0,1,1,False)
#for i in res: print(res[i])
