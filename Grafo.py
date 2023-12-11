
import graphviz as gv
import random
import math
from Nodo import *
from Arista import *

class Grafo:

    def __init__(self, dirigido = False, auto = True) -> None:
        self.dirigido = dirigido
        self.auto = auto
        self.nodos = {}
        self.aristas = {}

    def agregarNodo(self, data):
        llave = -1

        # Si se encuentra en el diccionario
        if list([nodo.data for nodo in self.nodos.values()]).count(data) != 0:
            # Busca su llave
            index = list([nodo.data for nodo in self.nodos.values()]).index(data)
            llave = list(self.nodos.keys())[index]
            # Si encontró entonces regresa el nodo
            return llave
        
        nuevo_id = len(self.nodos)
        self.nodos[nuevo_id] = (Nodo(nuevo_id,data))
        return nuevo_id
    
    def agregarArista(self, id_nodo1, id_nodo2):
        nodo1 = self.nodos.get(id_nodo1)
        nodo2 = self.nodos.get(id_nodo2)
        llave = len(self.aristas)
        self.aristas[llave] = Arista(llave,nodo1, nodo2)
        nodo1.vecinos[id_nodo2] = nodo2
        if not self.dirigido and id_nodo1 != id_nodo2:
            nodo2.vecinos[id_nodo1] = nodo1
        return llave
    
    def generarValoresDeArista(self):
        for a in self.aristas.values():
            a.data = random.randint(1,30)

    def imprimir(self):
        for n in self.nodos.values():
            print((n.id, n.data), end='\t| {')
            for a in self.aristas.values():
                if a.nodo1.id == n.id:
                    print((a.nodo2.id, self.nodos[a.nodo2.id].data), end=',')
                if not self.dirigido and a.nodo2.id == n.id:
                    print((a.nodo1.id, self.nodos[a.nodo1.id].data), end=',')

            print('}')
            
    def guardar(self, name="grafo.dot", data=False):
        with open(name, "w") as f:
            f.write("digraph G {\n" if self.dirigido else "graph G {\n")
            for n in self.nodos.values():
                f.write(str(n.id) + (f'[label="{n.data}"]\n' if data else "\n"))
            for a in self.aristas.values():
                f.write(str(a.nodo1.id) + (" -> " if self.dirigido else " -- ") +
                         str(a.nodo2.id) + (f" [label='{a.data}']" if data else "") + '\n')

            f.write("}\n")

    def BFS(self,s):

        visitados = {}
        visitados[s] = self.nodos[s]
        nodos_a_expandir = []

        arbol = Grafo()
        id_nodo_actual = arbol.agregarNodo(self.nodos[s].data)

        nodos_a_expandir.append(self.nodos[s])

        # Agregamos aristas del arbol
        while len(nodos_a_expandir) != 0:

            nodo_actual = nodos_a_expandir.pop(0)
            id_nodo_actual = arbol.agregarNodo(nodo_actual.data)
            
            for v in nodo_actual.vecinos.values():
                if visitados.get(v.id) == None:
                    visitados[v.id] = v
                    id_vecino = arbol.agregarNodo(v.data)
                    arbol.agregarArista(id_nodo_actual,id_vecino)
                    nodos_a_expandir.append(v)
            
        return arbol

    def DFS(self,s, arbol, visitados={}):
        visitados[s] = self.nodos[s]

        id_nodo_actual = arbol.agregarNodo(self.nodos[s].data)
        for v in self.nodos[s].vecinos.values():
            if visitados.get(v.id) == None:
                id_vecino = self.DFS(v.id, arbol, visitados)
                arbol.agregarArista(id_nodo_actual, id_vecino)
        return id_nodo_actual


    def DFS_I(self,s):
        visitados = {}
        visitados[s] = self.nodos[s]
        pila = []
        pila.append(s)
        
        arbol = Grafo()
        

        while len(pila) != 0:
            id_nodo_actual = arbol.agregarNodo(self.nodos[pila[-1]].data)
            #print("ina = iv =",id_nodo_actual)
            #print(f"vis = [{[n.data for n in visitados.values()]}]")
            #print(f"vec = [{[n.data for n in self.nodos[pila[-1]].vecinos.values()]}]")
            retroceder = True
            for v in self.nodos[pila[-1]].vecinos.values():
                if visitados.get(v.id) == None:
                    visitados[v.id] = v
                    
                    id_vecino = arbol.agregarNodo(v.data)
                    #print("\tiv =", id_vecino)
                    arbol.agregarArista(id_nodo_actual, id_vecino)
                    #print(f"\tar = ({id_nodo_actual},{id_vecino})")
                    #print(pila, end=' -> ')
                    pila.append(v.id)
                    #print(pila)
                    retroceder = False
                    break
            if retroceder:
                pila.pop()
        return arbol
    
    def Dijstra(self,s):
        visitados = {}

        #prioridades = [(len(self.nodos)+1,self.nodos[x]) for x in range(len(self.nodos))]
        prioridades = [[math.inf,self.nodos[x].id, -1, -1] for x in range(len(self.nodos))]
        #print("P:",prioridades)
        
        # Colocar nodo s con prioridad 0
        prioridades[s][0] = 0
        le = 0

        arbol = Grafo()

        while len(prioridades) > 0:
            prioridades.sort()
            p,idnodo,i1,peso = prioridades.pop(0)
            nodo = self.nodos[idnodo]
            d_id_nodo = arbol.agregarNodo(str(nodo.data)+" - "+ str(p))
            visitados[nodo.id] = nodo

            if i1 != -1:
                a_id_a = arbol.agregarArista(i1,d_id_nodo)
                arbol.aristas[a_id_a].data = peso
            
            
            #print("N:", nodo.data)
            #print("Vec:", [v.data for v in nodo.vecinos.values()])
            #print("Vis:", [(v,visitados.get(v).data) for v in visitados.keys()])

            # Actualizamos las prioridades para sacar el mejor
            # valor en la siguiente iteracion
            for v in nodo.vecinos.values():
                # si no esta en visitados
                if visitados.get(v.id) == None:

                    # Obtenemos index del objeto
                    #print("Prio:",prioridades)
                    #print("V:",v.data)
                    elemento = next(filter(lambda pri: pri[1] == v.id,prioridades))
                    #print(elemento)
                    vi = prioridades.index(elemento)
                    # Obtenemos el dato de la arista
                    arista = next(
                        filter(
                            lambda a: a == Arista(0,nodo, v) or (not self.dirigido and a == Arista(0,v,nodo)),
                            self.aristas.values()
                        )
                    )
                    le = arista.data

                    # (u,v)Si d(v)>d(u)+le
                    if prioridades[vi][0] > p + le:
                        prioridades[vi][0] = p + le
                        prioridades[vi][2] = d_id_nodo
                        prioridades[vi][3] = le
                        # Actualizar prioridad de v->d(v)=d(u)+le
            #arbol.imprimir()

        return arbol
    
    def KruscalD(self):
        arbol = Grafo()
        grupos = []

        # Creamos los grupos
        for v in self.nodos.values():
            grupos.append([v])
            arbol.agregarNodo(v.data)

        # Ordenamos
        aristas = [arista for arista in self.aristas.values()]
        aristas.sort(key=lambda a: a.data)

        # Comenzamos a mezclar
        for a in aristas:
            g1 = -1
            g2 = -1
            #Buscar nodo de atista en grupos
            for g in grupos:
                if a.nodo1 in g:
                    g1 = grupos.index(g)
                    break
            for g in grupos:
                if a.nodo2 in g:
                    g2 = grupos.index(g)
                    break
            # Si son de grupos diferentes los mezclo
            if g1 != g2:
                grupos[g1].extend(grupos[g2])
                grupos.pop(g2)
                id_a = arbol.agregarArista(a.nodo1.id, a.nodo2.id)
                arbol.aristas[id_a].data = a.data
        return arbol

    def KruscalI(self):
        arbol = Grafo()
        for n in self.nodos.values():
            arbol.agregarNodo(n.data)

        # Generamos lista de aristas para ordenar
        # Ordenamos
        aristas = [arista for arista in self.aristas.values()]
        aristas_arbol = [arista for arista in self.aristas.values()]
        aristas.sort(key=lambda a: a.data, reverse=True)


        for a in aristas:
            # Vacio el arbol y vecinos de nodos
            arbol.aristas = {}
            for n in arbol.nodos.values():
                n.vecinos = {}

            # Vemos que pasa si se remueve de la lista de aristas
            for ar in aristas_arbol:
                if ar != a:
                    arbol.agregarArista(ar.nodo1.id, ar.nodo2.id)

            # Si no se desconectó el grafo
            # bfs = arbol.BFS(0)
            # print('\n**********************************************\nArbol:')
            # arbol.imprimir()
            # print('\n**********************************************\nBFS:')
            # bfs.imprimir()
            # print('**********************************************\n\n')
            # nodosBFS = len(bfs.nodos)
            # print(nodosBFS, "-",len(self.nodos), "--", len(arbol.aristas))
            if len(arbol.BFS(0).nodos) == len(self.nodos):
                aristas_arbol.pop(aristas_arbol.index(a))

        # Vacio el arbol y vecinos de nodos
        arbol.aristas = {}
        for n in arbol.nodos.values():
            n.vecinos = {}

        # Vemos que pasa si se remueve de la lista de aristas
        for ar in aristas_arbol:
            id_a = arbol.agregarArista(ar.nodo1.id, ar.nodo2.id)
            arbol.aristas[id_a].data = ar.data
        
        return arbol

    def Prim(self):

        Q = []
        S = []

        # Genero el los nodos en el arbol e inicializo Q
        arbol = Grafo()
        for n in self.nodos.values():
            arbol.agregarNodo(n.data)
            Q.append(n)
            
        # Tomo el primer nodo y lo guardo en S
        S.append(Q.pop(0))

        # Mientras Q no este vacio
        while Q:
            minimo = (float('inf'),None)

            # print("\nBuscando en:")
            # print("Q:", [str(q) for q in Q])
            # print("S:", [str(s) for s in S])
            # Por cada nodo en el arbol
            for n in S:
                # Busco sus vecinos no agregados
                for v in n.vecinos:
                    # Si no esta en S, verifica el valor de la arista
                    if self.nodos[v] not in S:
                        # Vemos la arista que va de 'n' a 'v'
                        e = next(
                            filter(
                                lambda ar: ar == Arista(0,n,self.nodos[v]) or (not self.dirigido and ar == Arista(0,self.nodos[v],n)), 
                                self.aristas.values()
                            )
                        )
                        #print("\t", e.data, " | ", e.nodo1,"--", e.nodo2)
                        # Si su valor es menor al minimo
                        if e.data < minimo[0]:
                            minimo = (e.data, e, self.nodos[v])
            # Agrego el minimo a S y la arista al arbol
            #print(len(Q))
            pop_index = Q.index(minimo[2])
            #print("Atista:", minimo[1].data,"Nodo:",Q[pop_index])
            nodo = Q.pop(pop_index)
            S.append(nodo)
            id_a = arbol.agregarArista(minimo[1].nodo1.id, minimo[1].nodo2.id)
            arbol.aristas[id_a].data = minimo[0]
        return arbol

