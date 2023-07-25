pos = [3,4]
path = []

# Gibt die Position des Vorgängers zurück 
def _pos(pos : list, direction : str):
    if direction == 'diag': return [pos[0]-1,pos[1]-1]
    if direction == 'vert': return [pos[0]-1,pos[1]]
    if direction == 'hor': return [pos[0],pos[1]-1]

# Gibt Liste aller Pfäder von einer Startposition zurück
def _get_paths(traceback,start_pos):
    result = []
    path = []

    # Rekursive Methode, 
    def _recursiv(traceback, pos, path):
        
        # Stoppbedingung der Rekursive: wenn es keinen Vorgänger mehr zugreifen kann (None), wird ein vollständiger Pfad in result addiert
        if traceback[pos[0]][pos[1]] == None: 
            #print('a path done')
            result.append(path)
            return path

        # Falls es mehrere Vorgänger gibt
        if isinstance(traceback[pos[0]][pos[1]], list): 
            path = [path.copy() for _ in range(len(traceback[pos[0]][pos[1]]))]
            #print('hier2',path)

            for i in range(len(path)): path[i].append(traceback[pos[0]][pos[1]][i])
            #print('hier3',path)


            for i in range(len(path)):
                #print('check',path[i],'pos_before',pos,'pos_after',_pos(pos,path[i][-1]))
                path[i] = _recursiv(traceback,_pos(pos,path[i][-1]),path[i])
                

        # Falls es nur einen Vorgänger gibt
        else:
            while pos[0] >= 0 and pos[1] >= 0:
                if traceback[pos[0]][pos[1]] == None: break

                path.append(traceback[pos[0]][pos[1]])
                print('hier1',path)
                #print('check pos bf', pos)
                if traceback[pos[0]][pos[1]] == 'diag': 
                    pos[0] -= 1 
                    pos[1] -= 1
                elif traceback[pos[0]][pos[1]] == 'vert': pos[0] -= 1
                elif traceback[pos[0]][pos[1]] == 'hor': pos[1] -= 1
                #print('check_pos_af',pos)
                path = _recursiv(traceback, pos, path)
                if isinstance(traceback[pos[0]][pos[1]], list): break
            
    _recursiv(traceback,start_pos,path)
    return result

traceback = [[None,'hor', 'hor', 'hor', 'hor',],
             ['vert', 'diag','hor','vert','hor'],
             ['vert', 'diag',['diag','vert','hor'],'hor','hor'],
             ['vert', 'vert',['vert','hor'],'hor','hor']]

paths = _get_paths(traceback,pos)
#print('result',paths)
'''
[['hor', 'hor', 'vert', 'diag', 'diag'], 
 ['hor', 'hor', 'vert', 'vert', 'hor', 'diag'], 
 ['hor', 'hor', 'vert', 'hor', 'diag', 'vert'], 
 ['hor', 'hor', 'hor', 'vert', 'diag', 'vert']] 
'''


#-------------------------------------------
# Modifiziert den Pfad, damit seine Format dieselben im Entwurf passt
def _modify_path(path : list, start_pos : list):
    list_of_pos = [start_pos]
    # Erzeugt eine Liste der Positionen anhand des Pfades ## Liste von Format: pos = [Zeile, Spalte] ## z.B [5,4]
    for i in range(len(path)):
        list_of_pos.append(_pos(list_of_pos[-1],path[i]))
    #print(list_of_pos)    

    modified_path = [] # Liste von Format [pos,Richtungen an dieser Position]
    
    # Addiert die Positionen
    for i in range(len(list_of_pos)):
        modified_path.append([list_of_pos[i]])  
    #print(modified_path) # z.B. [[[5,4]], [[4,3]],..., [0,0]]

    for i in range(len(path)):
        modified_path[i].append(path[i])
    #print(modified_path) # z.B. [[[5,4],'diag'], [[4,3], 'diag'],..., [0,0]] 
    
    #print('modified')
    return modified_path # Ergebnis: der Pfad entspricht die Format von path im Entwurf

# Beispiel
modified_path = _modify_path(paths[0],[3,4])
#print(modified_path)