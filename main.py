from Grafo import *
import random

def grafoMalla(m, n, dirigido=False):
    """
    Genera grafo de malla
    :param m: número de columnas (> 1)
    :param n: número de filas (> 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    print("Generando grafo de malla con ")

    if m <= 1:
        m = 2
    if n <= 1:
        n = 2

    nuevo_grafo = Grafo(dirigido=dirigido)

    # Generamos nodos
    for i in range(m):
        for j in range(n):
            nuevo_grafo.agregarNodo(str(i)+","+str(j))
    
    # Generamos aristas
    for i in range(m):
        for j in range(n):
            if ( i + 1 < m): 
                nuevo_grafo.agregarArista(i*n + j, (i+1)*n + j)
            if ( j + 1 < n):
                nuevo_grafo.agregarArista(i*n + j, i*n + j+1)
    return nuevo_grafo


## Corregir repeticion de aristas
def grafoErdosRenyi(n, m, dirigido=False, auto=False):
    """
    Genera grafo aleatorio con el modelo Erdos-Renyi
    :param n: número de nodos (> 0)
    :param m: número de aristas (>= n-1)
    :param dirigido: el grafo es dirigido?
    :param auto: permitir auto-ciclos?
    :return: grafo generado
    """
    if n <= 0:
        n = 1
    if m < n-1:
        m = n-1

    nuevo_grafo = Grafo(dirigido=dirigido)
    for i in range(n):
        nuevo_grafo.agregarNodo(i)

    print(m)
    m = min(m,((n*(n-1) if dirigido else n*(n-1)/2) - (n if not auto else 0) ) + n)
    print(m)
    
    while len(nuevo_grafo.aristas) < m :
        i = random.randint(0,n-1)
        j = random.randint(0,n-1)
        if (auto or i != j):

            existe = False
            for a in nuevo_grafo.aristas.values():
                if (a.nodo1.id == i and a.nodo2.id == j):
                    existe = True

                if not dirigido and a.nodo1.id == j and a.nodo2.id == i:
                    existe = True
            if existe:
                continue
            
            # Agregamos nodo
            nuevo_grafo.agregarArista(i,j)
    return nuevo_grafo

def grafoGilbert(n, p, dirigido=False, auto=False):
    """
    Genera grafo aleatorio con el modelo Gilbert
    :param n: número de nodos (> 0)
    :param p: probabilidad de crear una arista (0, 1)
    :param dirigido: el grafo es dirigido?
    :param auto: permitir auto-ciclos?
    :return: grafo generado
    """
    if n <= 0:
        n = 1
    if 0 > p and p < 1:
        p = 0.5 # Valor por defecto en caso de que se proporcione valor erroneo
    
    nuevo_grafo = Grafo(dirigido=dirigido)
    for i in range(n):
        nuevo_grafo.agregarNodo(i)
    for i in range(n):
        for j in range(n):
            #if (not auto and i != j) or auto:
            if (auto or i != j):
                if not dirigido:
                    existe = False
                    for a in nuevo_grafo.aristas.values():
                        if (a.nodo1.id == i and a.nodo2.id == j) or \
                            (a.nodo1.id == j and a.nodo2.id == i):
                            existe = True
                            break
                    if existe:
                        continue

                if random.random() < p:
                    nuevo_grafo.agregarArista(i,j)
                

    return nuevo_grafo

def grafoGeograficoSimple(n, r, dirigido=False, auto=False):
    """
    Genera grafo aleatorio con el modelo geográfico simple
    :param n: número de nodos (> 0)
    :param r: distancia máxima para crear un nodo (0, 1)
    :param dirigido: el grafo es dirigido?
    :param auto: permitir auto-ciclos?
    :return: grafo generado
    """

    if n <= 0:
        n = 1
    if 0 > r and r < 1:
        r = 0.2

    nuevo_grafo = Grafo(dirigido=dirigido)
    # Creamos puntos en un cuadro de 1x1
    for i in range(n):
        nuevo_grafo.agregarNodo([random.random(), random.random()])
    for i in range(n):
        for j in range(n):
            # Si la distancia es menor
            
            if auto and i == j:
                nuevo_grafo.agregarArista(i,j)
            elif i != j:
                # Verificar que no exista si es no dirigido
                if not dirigido:
                    existe = False
                    for a in nuevo_grafo.aristas.values():
                        if (a.nodo1.id == i and a.nodo2.id == j) or \
                            (a.nodo1.id == j and a.nodo2.id == i):
                            existe = True
                            break
                    if existe:
                        continue
                # Verificar si la distancia es 
                if (nuevo_grafo.nodos[i].data[0]-nuevo_grafo.nodos[j].data[0]) ** 2 + \
                    (nuevo_grafo.nodos[i].data[1]-nuevo_grafo.nodos[j].data[1]) ** 2 < r*r:
                    nuevo_grafo.agregarArista(i,j)


    return nuevo_grafo

def grafoBarabasiAlbert(n, d, dirigido=False, auto=False):
    """
    Genera grafo aleatorio con el modelo Barabasi-Albert
    :param n: número de nodos (> 0)
    :param d: grado máximo esperado por cada nodo (> 1)
    :param dirigido: el grafo es dirigido?
    :param auto: permitir auto-ciclos?
    :return: grafo generado
    """

    if n <= 0:
        n = 1
    if d <= 1:
        d = 2

    nuevo_grafo = Grafo(dirigido=dirigido)
    for i in range(n):
        nuevo_grafo.agregarNodo(i)

        # Conectar nodo

        # Revisamos por cada nodo el número de aristas
        for j in range(len(nuevo_grafo.nodos)):
            if auto or i != j:

                # Verificar que no exista si es no dirigido
                if not dirigido:
                    existe = False
                    for a in nuevo_grafo.aristas.values():
                        if (a.nodo1.id == i and a.nodo2.id == j) or \
                            (a.nodo1.id == j and a.nodo2.id == i):
                            existe = True
                            break
                    if existe:
                        continue

                conectadas = len([x for x in nuevo_grafo.aristas.values() if x.nodo1.id == j or x.nodo2.id == j])
                p = (d - conectadas) / d
                if p > random.random():
                    nuevo_grafo.agregarArista(i,j)

    return nuevo_grafo

def grafoDorogovtsevMendes(n, dirigido=False):
    """
    Genera grafo aleatorio con el modelo Barabasi-Albert
    :param n: número de nodos (≥ 3)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    if n < 3:
        n = 3

    nuevo_grafo = Grafo(dirigido=dirigido)
    # Agregamos el primer triangulo
    for i in range(3):
        nuevo_grafo.agregarNodo(i)
    nuevo_grafo.agregarArista(0,1)
    nuevo_grafo.agregarArista(1,2)
    nuevo_grafo.agregarArista(2,0)

    # Agregamos el resto de nodos

    for i in range(3,n):
        nuevo_grafo.agregarNodo(i)
        arista = nuevo_grafo.aristas[random.randint(0, len(nuevo_grafo.aristas)-1)]

        nuevo_grafo.agregarArista(i, arista.nodo1.id)
        nuevo_grafo.agregarArista(i, arista.nodo2.id)

    return nuevo_grafo

# Para implementacion futura
#print(Arista(0,Nodo(0,'a'),Nodo(1,'b')) == Arista(1,Nodo(0,'a'),Nodo(1,'b')))

# Generacion de grafos
tamanios = [30,100,500]
cantidad = 1

# Ciclo generador
for n in tamanios:
    for j in range(cantidad):
        grafito = grafoMalla(int(n**(1/2))+1,int(n**(1/2))+1, False)
        grafito.guardar("Grafos/grafito_Malla_"+str(n)+"_"+str(j)+".gv")
        
        grafito = grafoErdosRenyi(n, n*random.randint(int(n/2),n), False, False)
        grafito.guardar("Grafos/grafito_ErdosRenyi_"+str(n)+"_"+str(j)+".gv")
        
        grafito = grafoGilbert(n, 0.5*random.random(), False, auto=False)
        grafito.guardar("Grafos/grafito_Gilbert_"+str(n)+"_"+str(j)+".gv")
        
        grafito = grafoGeograficoSimple(n, 0.05 + 0.20*random.random(), False, False)
        grafito.guardar("Grafos/grafito_GeograficoSimple_"+str(n)+"_"+str(j)+".gv")
        
        grafito = grafoBarabasiAlbert(n, int(n**(1/2)), False, False)
        grafito.guardar("Grafos/grafito_BarabasiAlbert_"+str(n)+"_"+str(j)+".gv")
        
        grafito = grafoDorogovtsevMendes(n, False)
        grafito.guardar("Grafos/grafito_DorogovtsevMendes_"+str(n)+"_"+str(j)+".gv")
        

"""

g = grafoMalla(5,3, True)
g.guardar("g.dot")

g2 = grafoErdosRenyi(100,2000, False, False)
g2.guardar("g2.dot")

g3 = grafoGilbert(20, 0.2, dirigido=True, auto=False)
g3.guardar("g3.dot")

g4 = grafoGeograficoSimple(200, 0.2, dirigido=True, auto=False)
g4.guardar("g4.dot")

g5 = grafoBarabasiAlbert(100, 4, False, False)
g5.guardar("g5.dot")

g6 = grafoDorogovtsevMendes(100, False)
g6.guardar("g6.dot")
"""