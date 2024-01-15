import random

class Nodo:
    def __init__(self, id, data) -> None:
        self.id = id
        self.data = data
        self.vecinos = {}
        self.graficos = {
            "color": (0,0,255, 100),
            "posicion": [random.random()*200 ,random.random()*200],
            "movimiento": [0,0],
            "ancho": 5
        }

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Nodo):
            return self.id == __value.id and self.data == __value.data
        return False
    
    def __hash__(self) -> int:
        return hash(self.data)
    
    def __str__(self) -> str:
        return "("+str(self.id) + ":'" + str(self.data)+"')"