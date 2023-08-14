#from pairwise_traceback import _get_paths, _modify_path
from webapp.lib.pairwise_traceback import _get_paths, _modify_path
 
# Traceback-Wert
def traceback_value(dia,ver,hor, similarity : bool):
    
    m = max(dia,ver,hor) if similarity else min(dia,ver,hor)
    if m == dia: return "diag"
    if m == ver: return "vert"
    else: return "hor"

# Gibt die Alignment zurück
def get_alignment(sequence1 : str, sequence2 : str, path : list, start_pos: list):

    s1_alg = ""
    s2_alg = ""
    alg = ""

    i = start_pos[0]
    j  = start_pos[1]

    assert i == len(sequence1)-1, "Die Position startet nicht aus die letzte Zeile der Matrix"
    
    # Alignment erstellen
    # Addiert Substring der Sequenz 2, die nicht zum Überlapp-Teil gehört
    for pos in range(j+1, len(sequence2)):
        s2_alg += sequence2[pos]

    # Addiert die Überlapp-Substring
    for p in path:
        if p == "diag":
            s1_alg = sequence1[i] + s1_alg
            s2_alg = sequence2[j] + s2_alg
            alg = "|" + alg if sequence1[i] == sequence2[j] else "_" + alg
            i -= 1 ; j -= 1
        elif p == "vert":
            s1_alg = sequence1[i] + s1_alg
            s2_alg = "-" + s2_alg
            alg = " " + alg
            i -= 1
        elif p == "hor":
            s1_alg = "-" + s1_alg
            s2_alg = sequence2[j] + s2_alg
            alg = " " + alg
            j -= 1

    # Addiert Substring der Sequenz 1, die nicht zum Überlapp-Teil gehört
    while i > 0:
        s1_alg = sequence1[i] + s1_alg
        s2_alg = " " + s2_alg
        alg = " " + alg
        i -= 1

    print('alignment\n',s1_alg,'\n',alg,'\n',s2_alg)

    return [s1_alg,alg,s2_alg]

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

    '''print('matrix')
    for i in matrix: print(i)
    print('traceback')
    for i in traceback: print(i)'''

    # Erstellt die Liste von Startpositionen zum Traceback
    ## Positionen des besten Score. Es ist möglich, viele Positionen besitzen den selben Score 
    list_start_pos = [i for i in range(len(seq2)) if matrix[-1][i] == max_value]
    ## Modifiziert die Liste von Integer (nur die Position IN der letzten Zeile) zur Liste von [Pos der letzten Zeile der 1. Seq][Pos IN der letzten Zeile]
    list_start_pos = [[len(sequence1),i] for i in list_start_pos]

    #print('list_start_pos',list_start_pos)

    # Findet Pfade
    unmodified_paths = [_get_paths(traceback, start_pos) for start_pos in list_start_pos]
    
    '''print('unmodified_paths')
    for i in unmodified_paths: print(i)'''

    # Erstellt wieder die Liste von Startpotitionen, weil sie nach dem Finden der Pfade geändert wird
    list_start_pos = [i for i in range(len(seq2)) if matrix[-1][i] == max_value]
    list_start_pos = [[len(sequence1),i] for i in list_start_pos]

    # Ertstellt eine Liste der Dictionaries der Alignments wie im Entwurf des Algorithmus
    alignments = []
    for i in range(len(list_start_pos)):
        alignments.extend([{'alignment':get_alignment(seq1,seq2,path, list_start_pos[i]),'path':_modify_path(path,list_start_pos[i])} for path in unmodified_paths[i]])    
    
    '''print('alignments')
    for i in alignments: print(i)'''
    
    return {'matrix': matrix,
            'traceback':traceback,
            'alignments': alignments,
            'score': max_value}

# Beispiel
res = get_result('tramnguyen','nguyntram', -1, 1 , 1, False)
for i in res: print(res[i])