
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
            a.data = random.randint(0,30)

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
        prioridades = [[math.inf,self.nodos[x].id, -1] for x in range(len(self.nodos))]
        print("P:",prioridades)
        
        # Colocar nodo s con prioridad 0
        prioridades[s][0] = 0

        arbol = Grafo()

        while len(prioridades) > 0:
            prioridades.sort()
            p,idnodo,i1 = prioridades.pop(0)
            nodo = self.nodos[idnodo]
            d_id_nodo = arbol.agregarNodo(nodo.data)
            visitados[nodo.id] = nodo

            if i1 != -1:
                arbol.agregarArista(i1,d_id_nodo)
            
            
            print("N:", nodo.data)
            print("Vec:", [v.data for v in nodo.vecinos.values()])
            print("Vis:", [(v,visitados.get(v).data) for v in visitados.keys()])

            # Actualizamos las prioridades para sacar el mejor
            # valor en la siguiente iteracion
            for v in nodo.vecinos.values():
                # si no esta en visitados
                if visitados.get(v.id) == None:

                    # Obtenemos index del objeto
                    print("Prio:",prioridades)
                    print("V:",v.data)
                    elemento = next(filter(lambda pri: pri[1] == v.id,prioridades))
                    print(elemento)
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
                        # Actualizar prioridad de v->d(v)=d(u)+le
            arbol.imprimir()

        return arbol 

