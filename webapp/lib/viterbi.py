# Inputs: Sequenz, Emissionsmatrix (Set von Tupels (Tulpe: ein String (Zustand) und eine Liste (Wahrscheinlichkeiten))), Übergangmatrix (gleich Type wie Emissionsmatrix)
# Outputs: Wahrscheinlichkeitsmatrix, Pfad, Zustand Matrix 

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

def get_idmax(df_lastcol: Series): # enthält nur die letzte Spalte
    #print(df_lastcol)
    max_value = df_lastcol.max()
    num = df_lastcol.to_numpy()

    # Erstellt eine Liste, die alle Indexes mit dem maximalen Wert beinhält
    idmax = np.array(np.where(num == max_value)).tolist()

    return idmax[0] if len(idmax) == 1 else idmax # Gibt Integer (Index) oder eine Liste von Integer (Indexes) zurück

# Beispiele
'''df = DataFrame({'A':[1,2,3,4],'B':[3,4,1,4]},index=['a','b','c','d'])
df_lastcol = df.iloc[:,-1]
print('list_idmax', get_idmax(df_lastcol))'''

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
    # Prüft, ob es mindestens 2 Zustände gibt, außer dem Start-Zustand
    assert len(trans_states) >= 2, "Mindestens 2 Zustände eingegeben werden, außer Start-Zustand"
    # Prüft, ob die Summe der Wahrscheinlichkeiten eines Zustands >= 0 und <= 1 ist
    for i in range(1,len(transition)):
        assert sum(transition[i][1]) >= 0 and sum(transition[i][1]) <= 1, "Die Summe der Übergang-Wahrscheinlichkeiten des Zustands {transition[i][0]} ist <= 0 oder >= 1"

    # Emissionsmatrix
    # Prüft, ob es keinen Start-Zustand gibt ### falls Form Bug hat
    em_states = [tup[0] for tup in emission]
    assert 'Start' not in em_states, "Der Start-Zustand sollte nicht da sein"
    # Prüft, ob alle Symbols in der Matrix auch in der Matrix sind 
    for s in emission[0][1]: assert s in seq, "Die Wahrscheinlichkeit des Symbols {s} fehlt"
    # Prüft, ob die Summe alle Wahrscheinlichkeiten eines Zustands >= 0 und <= 1 ist
    for i in range(1,len(emission)):
        assert sum(emission[i][1]) >= 0 and sum(emission[i][1]) <= 1, "Die Summe der Emission-Wahrscheinlichkeiten des Zustand {emission[i][0]} ist <= 0 oder >= 1"

    # Prüft jede Wahrscheinlichkeit in beiden Matrizen: Wert in (0,1)
    for tup in transition[1:]: # außer der Kopfzeile 
        for pro in tup[1]: 
            assert pro > 0 and pro < 1, "Die Wahrscheinlichkeit von {pro} in der Übergangsmatrix ist unpassend"
    for tup in emission[1:]: # außer der Kopfzeile
        for pro in tup[1]: 
            assert pro > 0 and pro < 1, "Die Wahrscheinlichkeit von {pro} in der Emissionsmatrix ist unpassend"
    
    # Initialisierung
    #----------------
    # Sequenz: Fügt Start-Symbol ein
    seq = 's' + seq
    
    # Matrizen: Konvertiert zu DataFrame 
    trans_df = to_dataframe(transition)
    em_df = to_dataframe(emission)


    # Wahrscheinlichkeitsmatrix (DataFrame), Traceback-Pfad und Zustand-Pfad
    pro_df = DataFrame(0.0, index= trans_states, columns= [*seq])
    pro_df.loc['Start','s'] = 1 
    traceback = DataFrame(None, index=[' '], columns=[*seq[1:]]) # Traceback-Pfad
    state_path = [] # Speichert die Zustände jedes Symbols

    state_df = DataFrame(index=['Zustand'],columns=[*seq[1:]])
    #print(em_df)
    #print(trans_df)

    # Berechnen
    # ---------------
    for i_symbol in range(1,len(seq)):
        symbol = pro_df.columns[i_symbol]
        # Beim ersten Symbol wird die Wahrscheinlichkeit von Start-Zustand gerechnet
        if i_symbol == 1:
            # Addiert Traceback (i_symbol-1, weil kein s Symbol in den Zeilenamen von path ist))
            traceback.iloc[0][i_symbol-1] = 'Start'

            for state in pro_df.index[1:]:
                pro_df.loc[state][i_symbol] = pro_df.loc['Start']['s'] * trans_df.loc['Start'][state] * em_df.loc[state][symbol]
            #print(pro_df)

        # Beim übrige Symbole werden ihre Wahrscheinlichkeit von die maximalen vorangegangenen gerechnet werden
        else:   
            # Addiert Traceback (i_symbol-1, weil kein s Symbol in den Zeilenamen von path ist)
            traceback.iloc[0][i_symbol-1] = pre_state = pro_df.iloc[:,i_symbol-1].idxmax()

            for state in pro_df.index[1:]:
                pro_df.loc[state][i_symbol] = pro_df.loc[pre_state][i_symbol-1] * trans_df.loc[pre_state][state] * em_df.loc[state][symbol]
            #print(pro_df)
        
        ### state of max of the present symbol in the path and state_path
        state_path.append(pro_df.iloc[:,i_symbol].idxmax())
        #print(state_path)
        
    assert len(state_path) == len(seq[1:]) # Prüft, ob die Anzahl der Zustände die Länge der Sequenz entspricht
    # add state in state_df
    state_df.loc['Zustand'] = state_path

    # Erzeugt die log-Wahrscheinlichkeitsmatrix
    logpro_df = np.log(pro_df)
    
    # Erreicht path vom traceback
    path = list(reversed(traceback.iloc[0,:]))

    
    '''
    print(pro_df)
    print(logpro_df)
    print('bug hier')
    print('path',path)
    print(state_df)
    '''

    return {'probability': to_nestedlist(pro_df), 'log_probability': to_nestedlist(logpro_df),
            'path': path,
            'path_matrix': to_nestedlist(state_df)}
    

# Beispiel
trans = [(' ',['+','-']),
      ('Start',[0.5,0.5]),
      ('+',[0.4,0.6]),
      ('-',[0.7,0.3])]

df = to_dataframe(trans)
#print(df)
#print(to_nestedlist(df))

em = [(' ',[*'ATGC']),
      ('+',[0.25,0.25,0.25,0.25]),
      ('-',[0.125,0.125,0.375,0.375])]

seq = 'TGTACAA'
#print(get_results(seq,trans,em))