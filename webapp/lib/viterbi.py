# Inputs: Sequenz, Emissionsmatrix (Set von Tupels (Tulpe: ein String (Zustand) und eine Liste (Wahrscheinlichkeiten))), Übergangmatrix (gleich Type wie Emissionsmatrix)
# Outputs: Wahrscheinlichkeitsmatrix, Pfad, Zustand Matrix 

import copy
from pandas import DataFrame, Series
import numpy as np

# Konvertiert django definierte Matrix zu DataFrame
## Achtung: Matrix wird transponiert, nutzt DataFrame.transpose, um die richtige Matrix zu erreichen
def to_dataframe(matrix):
    todict = {} ### Kopfzeile (Benennung der Zustände/Symbols sind benötigt)
    for tup in matrix: 
        todict[tup[0]] = tup[1]
        
    todf = DataFrame(todict, index=todict[' ']) # Setzt die Kopfzeile als Index der DataFrame
    return todf.iloc[:,1:].transpose()

# Konvertiert DataFrame zu eine geschachtelte Matrix
def to_nestedlist(df : DataFrame):
    nestedlist = [[' ']]
    # Fügt die Kopfzeile mit den Benennungen ein
    nestedlist[0] += list(df.columns)
    # Fügt die erste Spalte mit den Benennungen ein
    for i in df.index: nestedlist.append([i])

    # Fügt die Werte (Wahrscheinlichkeiten/Zustände) ein
    for i in range(1,len(nestedlist)):
        for j in range(1,len(nestedlist[0])):
            nestedlist[i].append(df.iloc[i-1,j-1])
    
    #for i in nestedlist: print(i)
    return nestedlist

# Gibt den/die Index(e) der Start-Position(en) zurück, deren Wahrscheinlichkeit  maximal ist/sind
def get_start_pos(df_lastcol: Series): # enthält nur die letzte Spalte
    #print(df_lastcol)
    max_value = df_lastcol.max()
    num = df_lastcol.to_numpy()

    # Liste, die alle Indexes mit dem maximalen Wert beinhält
    return np.array(np.where(num == max_value)).tolist()[0]

# Beispiele
'''df = DataFrame({'A':[1,2,3,4],'B':[3,4,1,4]},index=['a','b','c','d'])
df_lastcol = df.iloc[:,-1]
print('get_start_pos', get_start_pos(df_lastcol))
'''

# Gibt den/die Index(e) der Prä-Zustand/-Zustände zurück
# Methode dient als die Werte in der Tracebackmatrix
def get_id_pre_state(tem_pro: list):
    max_pro = max(tem_pro)
    id_pre_state = [i+1 for i in range(len(tem_pro)) if tem_pro[i] == max_pro]

    assert len(id_pre_state) > 0
    if len(id_pre_state) == 1: return id_pre_state[0] # Liste, wenn die Wahrscheinlichkeit aus vieler Zustände kommt
    else: return id_pre_state # Integer, wenn die Wahrscheinlichkeit nur aus einem Zustand kommt

# Beispiel
'''tem_pro = [5,3,5]
print('result',get_id_pre_state(tem_pro))
'''

# Gibt das Pfad von einer Start-Position zurück
def get_path(traceback: DataFrame, start_pos: list, limited_number_of_paths: int):
    result = []
    path = []

    def recursiv(traceback: DataFrame, pos: list, path: list):
        
        path.append(copy.copy(pos))
        #print('check path', path)
               
        if isinstance(traceback.iloc[pos[0]][pos[1]], list):
            # Vermehrt die aktuellen Pfade wegen vieler Möglichkeiten für die nächste Richtung
            path = [path.copy() for _ in range(len(traceback.iloc[pos[0]][pos[1]]))]
            #print('check list paths 1',path)

            # Sucht die vollständige Pfade aus der Richtung in der Liste
            for i in range(len(path)):
                # Nutzt indirekte Position, damit die selben Position für den nächsten Index nicht geändert wird  
                path[i] = recursiv(traceback,[traceback.iloc[pos[0]][pos[1]][i],path[i][-1][1]-1],path[i])
                #print('check path index ',i, path[i])
            #print('check list paths 2',path)
        
        else:
            if np.isnan(traceback.iloc[pos[0]][pos[1]]):
                    result.append(path)
                    #print('check path after stop', path)
                    return path
            while pos[0] > 0 and pos[1] > 0:
                if len(result) >= limited_number_of_paths: break # Generiert maximal eine bestimmte Menge der Pfade
                pos[0] = traceback.iloc[pos[0]][pos[1]]
                pos[1] -= 1
                #print('pos next',pos)                
                
                path = recursiv(traceback,pos,path)
                if isinstance(traceback.iloc[pos[0]][pos[1]], list): break 

        return path
    recursiv(traceback,start_pos,path)
    return result  

# Beispiel für result
# [[[3,4],[1,3],[1,2],[2,1],[0,0]]] Liste enthält ein Pfad
# [[[3,4],[1,3],[1,2],[2,1],[0,0]],[[3,4],[1,3],[2,2],[3,1],[0,0]]] Liste enthält 2 Pfade

# Durch den Pfad gibt die Zustände der Sequenz zurück (in der Richtung entlang der Sequenz)
def get_states(trans_states: list, path: list):
    states = []
    
    for pos in path[:-1]: # Außer der Start-Zustand an der [0,0]
        #print('pos in get states', pos)
        states.append(trans_states[pos[0]]) # pos[0] entspricht den Index des Zustandes in der trans_states
    #print('states',states)
    
    return list(reversed(states))
            
# Viterbi Algorithmus
def get_results(seq, transition, emission):
    # Prüft die Bedingungen
    #---------------------
    # Sequenz
    # Prüft, ob Sequenz nicht leer ist
    assert len(seq) > 0, "Die Sequenz muss mindestens einen Buchstabe haben"
    
    # Übergangsmatrix
    # Prüft, ob der Start-Zustand vorhanden ist
    trans_states = [tup[0] for tup in transition if tup[0] != ' '] # ' ' liegt in der Kopfzeile, trotzdem ist kein Zustand
    assert 'Start' in trans_states, "Der Start-Zustand fehlt"
    assert trans_states.index('Start') == 0, "Der Start-Zustand sollte im ersten Index stehen"
    # Prüft, ob die Summe der Wahrscheinlichkeiten eines Zustands >= 0 und <= 1 ist
    for i in range(1,len(transition)):
        assert sum(transition[i][1]) >= 0 and sum(transition[i][1]) <= 1, f"Die Summe der Übergang-Wahrscheinlichkeiten des Zustands {transition[i][0]} ist <= 0 oder >= 1"

    # Emissionsmatrix
    # Prüft, ob es keinen Start-Zustand gibt ### falls Form Bug hat
    em_states = [tup[0] for tup in emission]
    assert 'Start' not in em_states, "Der Start-Zustand sollte nicht da sein"
    # Prüft, ob alle Symbols in der Matrix auch in der Matrix sind 
    for s in emission[0][1]: assert s in seq, f"Die Wahrscheinlichkeit des Symbols {s} fehlt"
    # Prüft, ob die Summe alle Wahrscheinlichkeiten eines Zustands >= 0 und <= 1 ist
    for i in range(1,len(emission)):
        assert sum(emission[i][1]) >= 0 and sum(emission[i][1]) <= 1, f"Die Summe der Emission-Wahrscheinlichkeiten des Zustand {emission[i][0]} ist <= 0 oder >= 1"

    # Prüft jede Wahrscheinlichkeit in beiden Matrizen: Wert in (0,1)
    for tup in transition[1:]: # außer der Kopfzeile 
        for pro in tup[1]: 
            assert pro > 0 and pro < 1, f"Die Wahrscheinlichkeit von {pro} in der Übergangsmatrix ist unpassend"
    for tup in emission[1:]: # außer der Kopfzeile
        for pro in tup[1]: 
            assert pro > 0 and pro < 1, f"Die Wahrscheinlichkeit von {pro} in der Emissionsmatrix ist unpassend"
    
    # Initialisierung
    #----------------
    # Sequenz: Fügt Start-Symbol ein
    seq = chr(1) + seq
    
    # Matrizen: Konvertiert zu DataFrame 
    trans_df = to_dataframe(transition)
    em_df = to_dataframe(emission)


    # Wahrscheinlichkeitsmatrix (DataFrame), Traceback-Pfad und Zustand-Pfad
    pro_df = DataFrame(0.0, index= trans_states, columns= [*seq])
    pro_df.loc['Start',chr(1)] = 1 
    traceback_df = DataFrame(None, index= trans_states, columns=[*seq]) # Traceback-Pfad

    #print(em_df)
    #print(trans_df)

    # Berechnen
    # ---------------
    for id_symbol in range(1,len(seq)):
        symbol = pro_df.columns[id_symbol]
        # Beim ersten Symbol wird die Wahrscheinlichkeit von Start-Zustand gerechnet
        if id_symbol == 1:            

            for state in trans_states[1:]: # Außer Start-Zustand
                pro_df.loc[state][id_symbol] = pro_df.loc['Start'][chr(1)] * trans_df.loc['Start'][state] * em_df.loc[state][symbol]
                traceback_df.loc[state][id_symbol] = 0 # alle wird aus dem Start-Zustand berechnet
            

        # Beim übrige Symbole werden ihre Wahrscheinlichkeit von die maximalen vorangegangenen gerechnet werden
        else:  
            for state in trans_states[1:]: # Außer Start-Zustand
                tem_pro = []
                for pre_state in trans_states[1:]: # Außer Start-Zustand
                    tem_pro.append(pro_df.loc[pre_state][id_symbol-1] * trans_df.loc[pre_state][state] * em_df.loc[state][symbol])

                pro_df.loc[state][id_symbol] = max(tem_pro)
                traceback_df.loc[state][id_symbol] = get_id_pre_state(tem_pro)         

    # Erzeugt die log-Wahrscheinlichkeitsmatrix
    logpro_df = np.log(pro_df)

    '''print(pro_df)
    print(logpro_df)
    print(traceback_df)'''

    # Erstellt die Liste der Start-Position(en)
    list_start_pos = get_start_pos(pro_df.iloc[:,-1]) # Speichert nur Index der Start-Position(en)
    list_start_pos = [[i,len(seq)-1] for i in list_start_pos] # Speichert die Koordination in Tracebackmatrix
    #print('list_start_pos',list_start_pos)

    # Speichert alle Pfade aus der Start-Position(en) 
    paths = []
    count = 100 # Zählt Menge der Pfade. Der Algorithmus begrenzt die Menge in 100 Pfade
    for start_pos in list_start_pos:
        #print('b4',len(paths))

        if count <= 0: break # Generiert maximal nur 100 Pfade
        
        paths.extend(get_path(traceback_df,start_pos, count))
        
        #print('after',len(paths))
        
        count = count-len(paths)
        #print('count',count)
    assert len(paths) <= 100
    #print('paths in viterbi',len(paths))

    # Zustände der Sequenz: Dictionary {'states': Liste der Zustände (vorwärts),
    #                                   'path': Pfad (rückwärts)}
    states = [{'states': get_states(trans_states, path),
               'path': path} 
               for path in paths]

    #for i in states: print(i)
    
    return {'probability': to_nestedlist(pro_df), 'log_probability': to_nestedlist(logpro_df),
            'states': states,
            'traceback': to_nestedlist(traceback_df)}
    

# Beispiel
trans = [(' ',['+','-']),
      ('Start',[0.5,0.5]),
      ('+',[0.4,0.6]),
      ('-',[0.5,0.5])]

df = to_dataframe(trans)
#print(df)
#print(to_nestedlist(df))

em = [(' ',[*'ATGC']),
      ('+',[0.25,0.25,0.25,0.25]),
      ('-',[0.25,0.25,0.25,0.25])]

seq = 'TGTACAA'
res = get_results(seq,trans,em)
#print((res['states']))