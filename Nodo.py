
class Nodo:
    def __init__(self, id, data) -> None:
        self.id = id
        self.data = data
        self.vecinos = {}

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Nodo):
            return self.id == __value.id and self.data == __value.data
        return False
    
    def __str__(self) -> str:
        return "("+str(self.id) + ":'" + str(self.data)+"')"