
import graphviz as gv
from Nodo import *
from Arista import *

class Grafo:

    def __init__(self, dirigido = False, auto = True) -> None:
        self.dirigido = dirigido
        self.nodos = {}
        self.aristas = {}

    def agregarNodo(self, data):
        llave = -1

        # Si se encuentra en el diccionario
        if list(self.nodos.values()).count(data) != 0:
            # Busca su llave
            index = list(self.nodos.values()).index(data)
            llave = list(self.nodos.keys())[index]
            # Si encontró entonces regresa el nodo
            return llave
        
        nuevo_id = len(self.nodos)
        self.nodos[nuevo_id] = (Nodo(nuevo_id,data))
        return nuevo_id
    
    def agregarArista(self, id_nodo1, id_nodo2):
        nodo1 = self.nodos.get(id_nodo1)
        nodo2 = self.nodos.get(id_nodo2)
        self.aristas[len(self.aristas)] = (Arista(len(self.aristas),nodo1, nodo2))

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
    def guardar(self, name="grafo.dot"):
        with open(name, "w") as f:
            f.write("digraph G {\n" if self.dirigido else "graph G {\n")
            for n in self.nodos.values():
                f.write(str(n.id) + f'[label="{n.data}"]\n')
            for a in self.aristas.values():
                f.write(str(a.nodo1.id) + (" -> " if self.dirigido else " -- ") + str(a.nodo2.id) + '\n')

            f.write("}\n")
