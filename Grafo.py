
import graphviz as gv
import random
import math
from Nodo import *
from Arista import *


class Grafo:

    def __init__(self, dirigido = False, auto = True, nombre="Grafo") -> None:
        self.dirigido = dirigido
        self.auto = auto
        self.nodos = {}
        self.aristas = {}
        self.nombre = nombre

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
        llave = 0 if len(self.aristas) == 0 else (max(self.aristas.keys())+1)
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
        aristas = []

        for a in self.aristas.values():
            id_a = arbol.agregarArista(a.nodo1.id, a.nodo2.id)
            aristas.append(arbol.aristas[id_a])
            arbol.aristas[id_a].data = a.data

        aristas.sort(key=lambda a: a.data, reverse=True)

        print([(a.data, str(a.nodo1), str(a.nodo2)) for a in aristas])

        for a in aristas:
            # print("\rProgreso: "+str(aristas.index(a))+" de "+str(len(aristas))+"       "+str(aristas.index(a)/len(aristas)), end="")
            
            # Vemos que pasa si se remueve de la lista de aristas
            # Guardando la arista primero
            print((a.data, str(a.nodo1), str(a.nodo2)))

            n1 = arbol.aristas[a.id].nodo1
            n2 = arbol.aristas[a.id].nodo2
            data = arbol.aristas[a.id].data

            arbol.aristas.pop(a.id)

            # Si no es dirigido
            if not self.dirigido:
                # Eliminamos de ambos nodos el vecino
                n1.vecinos.pop(n2.id)
                n2.vecinos.pop(n1.id)
            else: 
                n1.vecinos.pop(n2.id)
            
            print("Arista Eliminada: ", str(n1), "--", str(n2), " | ", data)

            if len(arbol.BFS(0).nodos) != len(self.nodos):
                id_a = arbol.agregarArista(n1.id, n2.id)
                arbol.aristas[id_a].data = data
                print("Recupero arista:", str(n1), "--", str(n2), " | ", data)
                
        return arbol

    def Prim(self):

        Q = []
        S = []

        aristas = [a for a in self.aristas.values()]
        aristas_actuales = []

        # Genero el los nodos en el arbol e inicializo Q
        arbol = Grafo()
        for n in self.nodos.values():
            arbol.agregarNodo(n.data)
            Q.append(n)
            
        # Tomo el primer nodo y lo guardo en S
        S.append(Q.pop(0))


        print("Iniciando algoritmo")
        # Mientras Q no este vacio
        while Q:
            print("\rProgreso: "+str(len(Q))+" de "+str(len(self.nodos))+"       "+str(len(Q)/len(self.nodos)), end="")
            minimo = (float('inf'),None)
         
            # prcrazyint("S:", [str(s) for s in S])
            # Por cada nodo en el arbol

            aristasS = list(filter(
                lambda ar: (ar.nodo1 in S and ar.nodo2 not in S) or (not self.dirigido and ar.nodo2 in S and ar.nodo1 not in S),
                aristas
            ))
            aristasS.sort(key=lambda a: a.data)

            aristas.pop(aristas.index(aristasS[0]))

            nodo_por_agregar = aristasS[0].nodo2 if aristasS[0].nodo1 in S else aristasS[0].nodo1
            
            # for n in S:
            #     # Busco sus vecinos no agregados
            #     for v in n.vecinos:
            #         # Si no esta en S, verifica el valor de la arista
            #         if self.nodos[v] not in S:
            #             #print("Buscando ", n, self.nodos[v])
            #             filtrado = filter(
            #                     lambda ar: ar == Arista(0,n,self.nodos[v]) or (not self.dirigido and ar == Arista(0,self.nodos[v],n)), 
            #                     self.aristas.values()
            #                 )
            #             lista_filtrada = list(filtrado)
            #             #print("\n\n")
            #             #print([(str(a.nodo1) +"--"+ str(a.nodo2)) for a in self.aristas.values()])
            #             #print([(str(a.nodo1) +"--"+ str(a.nodo2)) for a in lista_filtrada])
            #             # Vemos la arista que va de 'n' a 'v'
            #             e = lista_filtrada[0]
            #             #print("\t", e.data, " | ", e.nodo1,"--", e.nodo2)
            #             # Si su valor es menor al minimo
            #             if e.data < minimo[0]:
            #                 minimo = (e.data, e, self.nodos[v])
            # Agrego el minimo a S y la arista al arbol
            #print(len(Q))
            pop_index = Q.index(nodo_por_agregar)
            #print("Atista:", minimo[1].data,"Nodo:",Q[pop_index])
            nodo = Q.pop(pop_index)
            S.append(nodo)
            id_a = arbol.agregarArista(aristasS[0].nodo1.id, aristasS[0].nodo2.id)
            arbol.aristas[id_a].data = aristasS[0].data
        return arbol

    def expandirSpring(self, c1, c2, c3, c4):
        nodos = list(self.nodos.values())
        fuerzas = [[0,0] for n in nodos]
        # Calculo las fuerzas para cada vertice
        for n in self.nodos.values():
            indice = nodos.index(n) 
            for n2 in self.nodos.values():
                d = math.sqrt((n2.graficos["posicion"][0] - n.graficos["posicion"][0])**2 + (n2.graficos["posicion"][1] - n.graficos["posicion"][1])**2) + 1
                magnitud = 0
                # Si esta conectado
                if n2 in n.vecinos.values():
                    magnitud = c1 * math.log(d / c2)
                else: # Si no es adjacente se repele
                    magnitud = - c3 / math.sqrt(d)
                fuerzas[indice][0] += (n2.graficos["posicion"][0] - n.graficos["posicion"][0])/d * magnitud # X
                fuerzas[indice][1] += (n2.graficos["posicion"][1] - n.graficos["posicion"][1])/d * magnitud # Y
        
        # Muevo el vertice
        for n in self.nodos.values():
            indice = nodos.index(n)
            n.graficos["posicion"][0] += fuerzas[indice][0] * c4
            n.graficos["posicion"][1] += fuerzas[indice][1] * c4

    def expandirForceDirected(self, W, L, temp):
        k = math.sqrt(W*L / len(self.nodos))
        fuerza_repulcion = lambda x: k*k / x 
        fuerza_atraccion = lambda x: x*x / k

        for n in self.nodos.values():
            n.graficos["movimiento"] = [0,0]
            
            # Fuerzas de repulción, por lo que el vector delta esta invertido
            for v in self.nodos.values():
                if not n == v:
                    delta = [v.graficos["posicion"][0] - n.graficos["posicion"][0], v.graficos["posicion"][1] - n.graficos["posicion"][1]]
                    if delta[0] == 0:
                        delta[0] = 0.1*(random.random()+0.0001)
                    if delta[1] == 0:
                        delta[1] = 0.1*(random.random()+0.0001)
                    abs_delta = math.sqrt(delta[0]**2 + delta[1]**2)
                    fr_delta = fuerza_repulcion(abs_delta)
                    n.graficos["movimiento"][0] -= (delta[0]/abs_delta) * fr_delta
                    n.graficos["movimiento"][1] -= (delta[1]/abs_delta) * fr_delta
        
        # Fuerzas de atraccion
        for a in self.aristas.values():
            delta = [a.nodo1.graficos["posicion"][0] - a.nodo2.graficos["posicion"][0], a.nodo1.graficos["posicion"][1] - a.nodo2.graficos["posicion"][1]]
            abs_delta = math.sqrt(delta[0]**2 + delta[1]**2)
            if abs_delta == 0:
                abs_delta = 1
            fa_delta = fuerza_atraccion(abs_delta)
            a.nodo1.graficos["movimiento"][0] -= (delta[0]/abs_delta) * fa_delta
            a.nodo1.graficos["movimiento"][1] -= (delta[1]/abs_delta) * fa_delta
            
            a.nodo2.graficos["movimiento"][0] += (delta[0]/abs_delta) * fa_delta
            a.nodo2.graficos["movimiento"][1] += (delta[1]/abs_delta) * fa_delta


        for i in range(len(self.nodos)):
            abs_vec_mov = math.sqrt(self.nodos[i].graficos["movimiento"][0]**2 + self.nodos[i].graficos["movimiento"][1]**2)
            self.nodos[i].graficos["posicion"][0] += self.nodos[i].graficos["movimiento"][0] * min(abs_vec_mov, temp)
            self.nodos[i].graficos["posicion"][1] += self.nodos[i].graficos["movimiento"][1] * min(abs_vec_mov, temp)

            # self.nodos[i].graficos["posicion"][0] = min(W/2, max(-W/2, self.nodos[i].graficos["posicion"][0]))
            # self.nodos[i].graficos["posicion"][1] = min(L/2, max(-L/2, self.nodos[i].graficos["posicion"][1]))
            pass

    def calcularRepulsion(self, W, L, n, QT_raiz, h):
        k = math.sqrt(W*L / len(self.nodos))
        fuerza_repulcion = lambda x: k*k / x

        f = [0,0]
        v = [n.graficos["posicion"][0] - QT_raiz.data[5][0],
             n.graficos["posicion"][1] - QT_raiz.data[5][1]]
        d = math.sqrt((QT_raiz.data[1][2] - QT_raiz.data[1][0])*(QT_raiz.data[1][1] - QT_raiz.data[1][3]))
        abs_v = math.sqrt(v[0]*v[0] + v[1]*v[1])

        if abs_v == 0:
            return f
        
        # Está muy lejos
        if d/abs_v < h or not QT_raiz.data[6]: # o no dividido
            fr_kv = fuerza_repulcion(abs_v)
            masa = QT_raiz.data[4]
            return [v[0]/abs_v * fr_kv * masa, v[1]/abs_v * fr_kv * masa]
        
        # Está muy cerca
        else:
            for v in QT_raiz.vecinos.values():
                if v.data[2] > QT_raiz.data[2]: # Es un subsector
                    repulsion = self.calcularRepulsion(W, L, n, v, h)
                    f[0] += repulsion[0]
                    f[1] += repulsion[1]
            return f

        

    def expandirForceDirectedBarnesHut(self, W, L, temp):

        min_x = min([n.graficos["posicion"][0] for n in self.nodos.values()]) 
        min_y = min([n.graficos["posicion"][1] for n in self.nodos.values()]) 

        max_x = max([n.graficos["posicion"][0] for n in self.nodos.values()]) 
        max_y = max([n.graficos["posicion"][1] for n in self.nodos.values()])


        k = math.sqrt(W*L / len(self.nodos))
        fuerza_atraccion = lambda x: x*x / k

        QT = ArbolQuad(min_x-10,max_y+10,max_x+10,min_y-10,[n for n in self.nodos.values()])
        QT.generarArbol()

        for n in self.nodos.values():
            n.graficos["movimiento"] = self.calcularRepulsion(W,L,n, QT.nodos[0], 1)
        
        # Fuerzas de atraccion
        for a in self.aristas.values():
            delta = [a.nodo1.graficos["posicion"][0] - a.nodo2.graficos["posicion"][0], a.nodo1.graficos["posicion"][1] - a.nodo2.graficos["posicion"][1]]
            abs_delta = math.sqrt(delta[0]**2 + delta[1]**2)
            if abs_delta == 0:
                abs_delta = 1
            fa_delta = fuerza_atraccion(abs_delta)
            a.nodo1.graficos["movimiento"][0] -= (delta[0]/abs_delta) * fa_delta
            a.nodo1.graficos["movimiento"][1] -= (delta[1]/abs_delta) * fa_delta
            
            a.nodo2.graficos["movimiento"][0] += (delta[0]/abs_delta) * fa_delta
            a.nodo2.graficos["movimiento"][1] += (delta[1]/abs_delta) * fa_delta

        # Movemos y limitamos al centro dado

        centro_grafo = [(max_x + min_x)/2, (max_y + min_y)/2]
        desplazamiento = [ (W/2 - centro_grafo[0]), (L/2 - centro_grafo[1])]

        for i in range(len(self.nodos)):
            abs_vec_mov = math.sqrt(self.nodos[i].graficos["movimiento"][0]**2 + self.nodos[i].graficos["movimiento"][1]**2)
            self.nodos[i].graficos["posicion"][0] += self.nodos[i].graficos["movimiento"][0] * min(abs_vec_mov, temp) + desplazamiento[0]
            self.nodos[i].graficos["posicion"][1] += self.nodos[i].graficos["movimiento"][1] * min(abs_vec_mov, temp) + desplazamiento[1]

            # self.nodos[i].graficos["posicion"][0] = min(W/2, max(-W/2, self.nodos[i].graficos["posicion"][0]))
            # self.nodos[i].graficos["posicion"][1] = min(L/2, max(-L/2, self.nodos[i].graficos["posicion"][1]))
    
        


class ArbolQuad(Grafo):
    def __init__(self, limite_izq, limite_sup, limite_der, limite_inf, puntos, dirigido=False, auto=True, nombre="Grafo") -> None:
        super().__init__(dirigido, auto, nombre)
        self.puntos = puntos
        self.limite_der = limite_der
        self.limite_izq = limite_izq
        self.limite_sup = limite_sup
        self.limite_inf = limite_inf
        self.cantidad = 1
    
    def subdividir(self, n_raiz, puntos, limite, nivel):
        if len(puntos)>self.cantidad:
            # print("Subdividiendo...")
            # Creamos listas para los nodos
            puntos_ne = []
            puntos_nw = []
            puntos_se = []
            puntos_sw = []
            # Clasificamos los puntos
            # print("Puntos:",[p.graficos["posicion"] for p in puntos])
            for p in puntos:
                # print("NW",p.graficos["posicion"][0] >= limite[0],p.graficos["posicion"][0] < (limite[0]+limite[2])/2,
                #       p.graficos["posicion"][1] <= limite[1],p.graficos["posicion"][1] > (limite[1]+limite[3])/2)
                if p.graficos["posicion"][0] >= limite[0] and p.graficos["posicion"][0] < (limite[0]+limite[2])/2 \
                    and p.graficos["posicion"][1] <= limite[1] and p.graficos["posicion"][1] > (limite[1]+limite[3])/2:
                    puntos_nw.append(p)

                # print("NE",p.graficos["posicion"][0] >= (limite[0]+limite[2])/2 ,p.graficos["posicion"][0] <= limite[2],
                #     p.graficos["posicion"][1] <= limite[1], p.graficos["posicion"][1] > (limite[1]+limite[3])/2)
                if p.graficos["posicion"][0] >= (limite[0]+limite[2])/2 and p.graficos["posicion"][0] <= limite[2] \
                    and p.graficos["posicion"][1] <= limite[1] and p.graficos["posicion"][1] > (limite[1]+limite[3])/2:
                    puntos_ne.append(p)

                # print("SW",p.graficos["posicion"][0] >= limite[0], p.graficos["posicion"][0] < (limite[0]+limite[2])/2,
                #     p.graficos["posicion"][1] <= (limite[1]+limite[3])/2, p.graficos["posicion"][1] >= limite[3])
                if p.graficos["posicion"][0] >= limite[0] and p.graficos["posicion"][0] < (limite[0]+limite[2])/2 \
                    and p.graficos["posicion"][1] <= (limite[1]+limite[3])/2 and p.graficos["posicion"][1] >= limite[3]:
                    puntos_sw.append(p)

                # print("SE",p.graficos["posicion"][0] >= (limite[0]+limite[2])/2, p.graficos["posicion"][0] <= limite[2],
                #     p.graficos["posicion"][1] <= (limite[1]+limite[3])/2, p.graficos["posicion"][1] >= limite[3])
                if p.graficos["posicion"][0] >= (limite[0]+limite[2])/2 and p.graficos["posicion"][0] <= limite[2] \
                    and p.graficos["posicion"][1] <= (limite[1]+limite[3])/2 and p.graficos["posicion"][1] >= limite[3]:
                    puntos_se.append(p)
            # print(puntos_ne)
            # print(puntos_nw)
            # print(puntos_se)
            # print(puntos_sw)
            # Creamos los nodos conectados a la raiz solo si existen puntos en el cuadrante
            
            masa_total = 0
            centro_total = [0,0]
            
            if len(puntos_ne) > 0:
                # Estructura de vertice quad:
                # 0 - id
                # 1 - rectangulo sector
                # 2 - nivel
                # 3 - nombre
                # 4 - masa
                # 5 - centro
                # 6 - subdividido
                id_ne = self.agregarNodo([len(self.nodos), ((limite[0]+limite[2])/2, limite[1],limite[2], (limite[1]+limite[3])/2), nivel+1,str(nivel)+"NE", 0, [0,0], True])
                self.agregarArista(n_raiz.id, id_ne)
                masa, centro = self.subdividir(self.nodos[id_ne], puntos_ne, ((limite[0]+limite[2])/2, limite[1],limite[2], (limite[1]+limite[3])/2), nivel+1) # NE
                
                self.nodos[id_ne].data[4] = masa
                self.nodos[id_ne].data[5] = [(c/masa) for c in centro]

                masa_total += masa
                centro_total[0] += centro[0]
                centro_total[1] += centro[1]
                
            if len(puntos_nw) > 0:
                id_nw = self.agregarNodo([len(self.nodos), (limite[0], limite[1],(limite[0]+limite[2])/2, (limite[1]+limite[3])/2), nivel+1,str(nivel)+"NW", 0, [0,0], True])
                self.agregarArista(n_raiz.id, id_nw)
                masa, centro = self.subdividir(self.nodos[id_nw], puntos_nw, (limite[0], limite[1],(limite[0]+limite[2])/2, (limite[1]+limite[3])/2), nivel+1) # NW
                
                self.nodos[id_nw].data[4] = masa
                self.nodos[id_nw].data[5] = [(c/masa) for c in centro]

                masa_total += masa
                centro_total[0] += centro[0]
                centro_total[1] += centro[1]
            if len(puntos_se) > 0:
                id_se = self.agregarNodo([len(self.nodos), ((limite[0]+limite[2])/2, (limite[1]+limite[3])/2,limite[2], limite[3]), nivel+1,str(nivel)+"SE", 0, [0,0], True])
                self.agregarArista(n_raiz.id, id_se)
                masa, centro = self.subdividir(self.nodos[id_se], puntos_se, ((limite[0]+limite[2])/2, (limite[1]+limite[3])/2,limite[2], limite[3]), nivel+1) # SE
                
                self.nodos[id_se].data[4] = masa
                self.nodos[id_se].data[5] = [(c/masa) for c in centro]

                masa_total += masa
                centro_total[0] += centro[0]
                centro_total[1] += centro[1]

            if len(puntos_sw) > 0:
                id_sw = self.agregarNodo([len(self.nodos), (limite[0], (limite[1]+limite[3])/2,(limite[0]+limite[2])/2, limite[3]), nivel+1,str(nivel)+"SW", 0, [0,0], True])
                self.agregarArista(n_raiz.id, id_sw)
                masa, centro = self.subdividir(self.nodos[id_sw], puntos_sw, (limite[0], (limite[1]+limite[3])/2,(limite[0]+limite[2])/2, limite[3]), nivel+1) # SW
                
                self.nodos[id_sw].data[4] = masa
                self.nodos[id_sw].data[5] = [(c/masa) for c in centro]

                masa_total += masa
                centro_total[0] += centro[0]
                centro_total[1] += centro[1]
            # print("Puntos",len(puntos))
            # print("Masa",masa_total)
            # print("Centro", centro_total)
            return masa_total, centro_total
        else:
            # print("Maximo...")
            # id_punto = self.agregarNodo([len(self.nodos), limite, nivel+1, '"'+str(puntos[0].data)+'"', 1, puntos[0].graficos["posicion"]])# puntos[0].data)
            # self.agregarArista(n_raiz.id,id_punto)
            cx = 0
            cy = 0
            for p in puntos:
                cx += p.graficos["posicion"][0]
                cy += p.graficos["posicion"][1]

            return len(puntos), [cx/len(puntos), cy/len(puntos)] 
    def generarArbol(self):
        id_raiz = self.agregarNodo([0, (self.limite_izq, self.limite_sup, self.limite_der, self.limite_inf), 0,"C", 1,[0,0], False])
        
        # Generamos subdivisiones del espacio
        masa, centro = self.subdividir(
            self.nodos[id_raiz], 
            self.puntos,
            (self.limite_izq, self.limite_sup, self.limite_der, self.limite_inf),
            0)
        self.nodos[id_raiz].data[4] = masa
        self.nodos[id_raiz].data[5] = [c/masa for c in centro]
        
        