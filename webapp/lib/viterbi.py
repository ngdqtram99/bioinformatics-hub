# inputs: seq, emission (set of tuple (tuple of one string and one list)), transition (same as emisison)
# outputs: matrix, path, state 

from pandas import DataFrame
import numpy as np

# convert django-defined matrix to dataframe
## Achtung: Matrix wird transponiert, use DataFrame.transpose to get right matrix
def to_dataframe(matrix):
    todict = {} ### we need to have the headline in the matrix too
    for tup in matrix: 
        todict[tup[0]] = tup[1]
        
    todf = DataFrame(todict, index=todict[' ']) # set headline as index
    return todf.iloc[:,1:].transpose()

# convert dataframe to a nested list
def to_nestedlist(df : DataFrame):
    nestedlist = [[' ']]
    # add headline
    nestedlist[0] += list(df.columns)
    # add first row
    for i in df.index: nestedlist.append([i])

    # add values
    for i in range(1,len(nestedlist)):
        for j in range(1,len(nestedlist[0])):
            nestedlist[i].append(df.iloc[i-1,j-1])
    
    #for i in nestedlist: print(i)
    return nestedlist

def get_results(seq, transition, emission):
    # Check conditions
    #---------------------
    # seq
    # check: not blank
    assert len(seq) > 0, "Die Sequenz muss mindestens einen Buchstabe haben"
    
    # transition
    # check 1: 'Start' state exists
    trans_states = [tup[0] for tup in transition if tup[0] != ' '] # ' ' belongs to headline and is not a state
    assert 'Start' in trans_states, "Der Start-Zustand fehlt"
    # check 2: min. 2 states (except 'Start' state)
    assert len(trans_states) >= 2, "Mindestens 2 Zustände eingegeben werden, außer Start-Zustand"
    

    # emission
    # check 1: no 'Start' state ### "somehow it's nonsence, but maybe form or view has bug :)"
    em_states = [tup[0] for tup in emission]
    assert 'Start' not in em_states, "Der Start-Zustand sollte nicht da sein"
    #check 2: all symbols in seq
    for s in emission[0][1]: assert s in seq, "Die Wahrscheinlichkeit des Symbols {s} fehlt"

    # check probability for both matrixes: value in [0,1]
    for tup in transition[1:]: # except headline 
        for pro in tup[1]: 
            assert pro >= 0 and pro <= 1, "Die Wahrscheinlichkeit von {pro} in der Übergangsmatrix ist unpassend"
    for tup in emission[1:]: # ecxcept headline
        for pro in tup[1]: 
            assert pro >= 0 and pro <= 1, "Die Wahrscheinlichkeit von {pro} in der Emissionsmatrix ist unpassend"
    
    # Initilization
    #----------------
    # seq: add Start symbol
    seq = 's' + seq
    
    # transition and emision: convert to dataFrame 
    trans_df = to_dataframe(transition)
    em_df = to_dataframe(emission)


    # probability matrix (dataframe), states matrix and path
    pro_df = DataFrame(0.0, index= trans_states, columns= [*seq])
    pro_df.loc['Start','s'] = 1 
    path = [] # save max probability in each column. 1 presents for the Start state
    state_path = [] # save state with max probability in each column

    state_df = DataFrame(index=['Zustand'],columns=[*seq[1:]])
    print(em_df)
    print(trans_df)

    # Calculating
    # ---------------
    for i_symbol in range(1,len(seq)):
        symbol = pro_df.columns[i_symbol]
        # first symbol: calculate the probability from Start state
        if i_symbol == 1:
            for state in pro_df.index[1:]:
                pro_df.loc[state][i_symbol] = pro_df.loc['Start']['s'] * trans_df.loc['Start'][state] * em_df.loc[state][symbol]
            #print(pro_df)

        # other symbol: calculate the probability from pre-symbol's probability
        else:    
            for state in pro_df.index[1:]:
                pro_df.loc[state][i_symbol] = path[-1] * trans_df.loc[state_path[-1]][state] * em_df.loc[state][symbol]
            #print(pro_df)
        
        # add max and state of max of the present symbol in the path and state_path
        path.append(pro_df.iloc[:,i_symbol].max())
        #print(path)
        state_path.append(pro_df.iloc[:,i_symbol].idxmax())
        #print(state_path)
        
    assert len(state_path) == len(seq[1:]) # check, if there are enough states for each symbol in the seq (just for sure)
    # add state in state_df
    state_df.loc['Zustand'] = state_path

    # create log probability matrix and log path following the probability matrix and path
    logpro_df = np.log(pro_df)
    logpath = [np.log(p) for p in path]
    
    '''
    print(pro_df)
    print(logpro_df)
    print('path',path)
    print('logpath',logpath)
    print(state_df)
    '''

    return {'probability': to_nestedlist(pro_df), 'log_probability': to_nestedlist(logpro_df),
            'path':path, 'log_path':logpath,
            'path_matrix': to_nestedlist(state_df)}
    

# Example
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