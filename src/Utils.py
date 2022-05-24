from collections import defaultdict
from Representation import AdjacencyList
import copy
import random
from Generator import Generator
#------------------------------------------------------------------------------------------------------------------
#
# PROJECT 2
#
#------------------------------------------------------------------------------------------------------------------
#ex1
def valid_graph(seq):
    if len(seq)==0:
        return False
    # jeśli liczba wszystkich nieparzystych elementów jest nieparzysta, to ciąg na pewno nie jest graficzny
    seq = sorted(seq, reverse=True)
    if sum(1 for i in seq if i%2==1)%2 == 1:
        return False
    while True:
        if all(i==0 for i in seq):
            return True #Jeśli tablica składa się z samych zer, to ciąg wejściowy jest graficzny
        if seq[0]<0 or seq[0]>=len(seq) or any(i<0 for i in seq):
            return False
        for i in range(1, seq[0]+1):
            seq[i] = seq[i]-1
        seq[0] =0
        seq = sorted(seq, reverse=True)

#ex2   
def randomizeGraph(adjacency_list,numberOfRandomize): 
    i=0
    data={'name': 'RandomizeGraph.png','size': (6, 6),'directed_all': False,'node_size': 500,'graph': copy.deepcopy(adjacency_list.graph),'nodes_description':{},'edges_description':{}}
    while i<numberOfRandomize:
        a=random.sample(list(data['graph'].keys()),1)[0]
        b=random.sample(list(data['graph'][a]),1)[0]
        c=random.sample(list(data['graph'].keys()),1)[0]
        d=random.sample(list(data['graph'][c]),1)[0]
        if a!=c and a!=d and b!=c and b!=d and c not in data['graph'][a] and d not in data['graph'][b]:
            data['graph'][a].remove(b)
            data['graph'][b].remove(a)

            data['graph'][c].remove(d)
            data['graph'][d].remove(c)

            data['graph'][a].append(c)
            data['graph'][c].append(a)

            data['graph'][b].append(d)
            data['graph'][d].append(b) 

            i+=1
    return AdjacencyList(data)

#konstrukcja grafu prostego  o stopniach wierzchołków zadanych przez ciąg graficzny
def cons_graph(seq):
    seq = sorted(seq, reverse=True)
    out = []
    
    data={'name': 'CoherentComponent.png','size': (6, 6),'directed_all': False,'node_size': 500,'graph': {},'nodes_description':{},'edges_description':{}}
    for i in range(len(seq)):                       #+1
        data['graph'][i]=[]

    verts = [[i, seq[i]] for i in range(len(seq))]  #+1
    for i in range(len(seq)):
        for j in range(1, 1 + verts[0][1]):
            out.append([verts[0][0], verts[j][0]])
            verts[j][1] -= 1
        verts[0][1] = 0
        verts.sort(key=lambda x: x[1], reverse=True)
    out.sort()

    for i in range(len(out)):
        data['graph'][out[i][0]].append(out[i][1])
        data['graph'][out[i][1]].append(out[i][0])
    #data['graph'].pop(0)
    return AdjacencyList(data)

#znajdowanie najwiekszej spojnej skladowej
#ex3
def components_rec(nr, v, G, comp):
    for u in G[v]:
        if comp[u] == -1:
            comp[u] = nr
            components_rec(nr,u,G,comp)

def components(G):
    nr=0
    comp = [-1] * len(G.keys())

    for v in G.keys():
        if comp[v] == -1:
            nr += 1
            comp[v] = nr
            components_rec(nr, v, G, comp)

    comp_repr = defaultdict(list)

    for i,k in enumerate(comp):
        comp_repr[k].append(i)  #i+1

    comp_big=0
    comp_big_len=0
    comps=[]
    tmpStr=""
    for comp, comp_v in sorted(comp_repr.items()):
        if len(comp_v) > comp_big_len:
            comp_big = comp
            comp_big_len = len(comp_v)
        tmpStr+=f'{comp}) {[i+1 for i in comp_v]}\n'
        print(f'{comp}) {comp_v}')
        comps.append(comp_v)

    print(f"Najwieksza skladowa ma numer {comp_big}.")
    tmpStr+=f"Najwieksza skladowa ma numer {comp_big}.\n"
    return tmpStr
    # return comps, comp_big

#ex5
#generowanie losowych grafów k-regularnych 
#n - ilosc wierzcholkow
def random_k_regular(k,n):
    if n-k>0:
        seq = [k for _ in range(n)]
        randomizeGraph(cons_graph(seq),100).graphVisualization()

#poszukiwania cyklu Hamiltona
#ex6
def find_Hamiltion_cycle(graph, v=1, stack=[]):
    if v not in stack:
        stack.append(v)

        if len(graph) == len(stack):
            if stack[-1] in graph[stack[0]]:
                stack.append(stack[0])
                return [x for x in stack]
            else:
                stack.pop()
                return None
        
        for x in graph[v]:
            tmp_stack = copy.deepcopy(stack)
            res = find_Hamiltion_cycle(graph, x, tmp_stack)
            if res is not None:
                return res