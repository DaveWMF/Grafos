from Nodo import *

class Arista:
    def __init__(self, id_arista, nodo1, nodo2) -> None:
        self.id =  id_arista
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.data = 0

        self.graficos = {
            "color": (0,0,0),
            "ancho":2
        }
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Arista):
            return self.nodo1.id == __value.nodo1.id and self.nodo2.id == __value.nodo2.id
        return False
    
    def __hash__(self) -> int:
        return hash((self.nodo1.id,self.nodo2.id))
    
    