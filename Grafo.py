
import graphviz as gv
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
        self.aristas[len(self.aristas)] = Arista(len(self.aristas),nodo1, nodo2)
        nodo1.vecinos[id_nodo2] = nodo2
        if not self.dirigido and id_nodo1 != id_nodo2:
            nodo2.vecinos[id_nodo1] = nodo1

    def imprimir(self):
        for n in self.nodos:
            print((n.id, n.data), end='\t| {')
            for a in self.aristas:
                if a.nodo1.id == n.id:
                    print((a.nodo2.id, self.nodos[a.nodo2.id].data), end=',')
                if not self.dirigido and a.nodo2.id == n.id:
                    print((a.nodo1.id, self.nodos[a.nodo1.id].data), end=',')

            print('}')
            
    # TODO
    def guardar(self, name="grafo.dot", data=False):
        with open(name, "w") as f:
            f.write("digraph G {\n" if self.dirigido else "graph G {\n")
            for n in self.nodos.values():
                f.write(str(n.id) + (f'[label="{n.data}"]\n' if data else "\n"))
            for a in self.aristas.values():
                f.write(str(a.nodo1.id) + (" -> " if self.dirigido else " -- ") + str(a.nodo2.id) + '\n')

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


