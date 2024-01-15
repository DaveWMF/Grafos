import pygame
from pygame import gfxdraw
from Grafo import *

MODO_PANTALLA_COMPLETA = 1
MODO_PANTALLA_DIV_2 = 2
MODO_PANTALLA_DIV_4 = 4

class Ventana:
    def __init__(self, modo) -> None:
        pygame.init()
        self.tam = 1280,720
        self.pantalla = pygame.display.set_mode(self.tam)

        pygame.display.set_caption("Grafos")
        self.run = True
        self.clock = pygame.time.Clock()
        
        self.modo = modo
        self.grafo = None

    def ejecutar(self, grafos):

        primer_iter = True
        temp_o = 0.0017
        temp = temp_o
        while self.run:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.pantalla.fill("white")


            # 
            if self.modo == MODO_PANTALLA_COMPLETA:
                # Pintar QuadTree
                # arbol = ArbolQuad(-360/escala,360/escala,360/escala, -360/escala, [n for n in grafos[0].nodos.values()])
                # arbol.generarArbol()

                # self.pintarArbolQuad(arbol, escala=escala)
                
                self.pintarGrafo(grafos[0])


                grafos[0].expandirSpring(2,1,1,0.1)
                #grafos[0].expandirForceDirected(self.tam[0],self.tam[1], temp)
                #grafos[0].expandirForceDirectedBarnesHut(self.tam[0],self.tam[1], temp)
            if self.modo == MODO_PANTALLA_DIV_2:
                
                #self.pintarGrafo(grafos[0],0)
                #self.pintarGrafo(grafos[1],1)
                grafos[0].expandirSpring(2,1,1,0.1)
                grafos[1].expandirSpring(2,1,1,0.1)
                grafos[0].expandirForceDirectedBarnesHut(self.tam[0],self.tam[1], temp)
                grafos[1].expandirForceDirectedBarnesHut(self.tam[0],self.tam[1], temp)

            if self.modo == MODO_PANTALLA_DIV_4:
                for i in range(min(4, len(grafos))):
                    self.pintarGrafo(grafos[i],i)
                    grafos[i].expandirSpring(2,1,1,0.1)
                    #grafos[i].expandirForceDirected(self.tam[0],self.tam[1], temp)
                    # if primer_iter:
                    #     grafos[i].expandirForceDirected(self.tam[0],self.tam[1], temp)
                    #     primer_iter = False
                    # grafos[i].expandirForceDirectedBarnesHut(self.tam[0],self.tam[1], temp)
            pygame.display.flip()
        pygame.quit()


    # modo - nos dice como se separan los cuadrantes
    # cuadrante - si hay mas de uno nos dibuja segun el cuadrante elejido
    def pintarGrafo(self, grafo, cuadrante = 0):
        
        # escala
        min_x = min([n.graficos["posicion"][0] for n in grafo.nodos.values()]) 
        min_y = min([n.graficos["posicion"][1] for n in grafo.nodos.values()]) 

        max_x = max([n.graficos["posicion"][0] for n in grafo.nodos.values()]) 
        max_y = max([n.graficos["posicion"][1] for n in grafo.nodos.values()])

        #x = max_x - min_x
        y = max_y - min_y

        escala = (self.tam[1])/y

        centro_grafo = [(max_x + min_x)/2, (max_y + min_y)/2]
        desplazamiento = [ (self.tam[0]/2 - centro_grafo[0]*escala), (self.tam[1]/2 - centro_grafo[1]*escala)]

        
        if self.modo == MODO_PANTALLA_COMPLETA:

            font = pygame.font.SysFont(None, 24)
            img = font.render(grafo.nombre, True, (0,0,0))
            self.pantalla.blit(img, (self.tam[0]/2, 10))
        
        if self.modo == MODO_PANTALLA_DIV_2:
            escala /= 2
            desplazamiento = [ (self.tam[0]*(1+2*cuadrante)/4 - centro_grafo[0]*escala), (self.tam[1]/2 - centro_grafo[1]*escala)]
            
            font = pygame.font.SysFont(None, 24)
            img = font.render(grafo.nombre, True, (0,0,0))
            self.pantalla.blit(img, (self.tam[0]*(1+2*cuadrante)/4, 10))

        if self.modo == MODO_PANTALLA_DIV_4:
            
            escala /= 4
            
            desplazamiento = [ (self.tam[0]*((1+2*cuadrante)%4)/4 - centro_grafo[0]*escala), (self.tam[1]*(1+(2*cuadrante//4)*2)/4 - centro_grafo[1]*escala)]

            font = pygame.font.SysFont(None, 24)
            img = font.render(grafo.nombre, True, (0,0,0))
            self.pantalla.blit(img, (self.tam[0]*((1+2*cuadrante)%4)/4, 10 + self.tam[1]*(2*cuadrante//4)/2))

        

        for a in grafo.aristas.values():
            pygame.draw.aaline(self.pantalla,
                               a.graficos["color"],
                               [a.nodo1.graficos["posicion"][0]*escala + desplazamiento[0] , a.nodo1.graficos["posicion"][1]*escala + desplazamiento[1] ], 
                               [a.nodo2.graficos["posicion"][0]*escala + desplazamiento[0] , a.nodo2.graficos["posicion"][1]*escala + desplazamiento[1] ])

        for n in grafo.nodos.values():
            gfxdraw.aacircle(self.pantalla, int(n.graficos["posicion"][0]*escala + desplazamiento[0]), int(n.graficos["posicion"][1]*escala + desplazamiento[1]), n.graficos["ancho"], n.graficos["color"])
            gfxdraw.filled_circle(self.pantalla, int(n.graficos["posicion"][0]*escala + desplazamiento[0]), int(n.graficos["posicion"][1]*escala + desplazamiento[1]), n.graficos["ancho"], n.graficos["color"])
    
    def pintarArbolQuad(self, arbolquad, escala = 1):
        self.aux_pintarArbolQuad(arbolquad.nodos[0], escala)
        offsetX = int(self.tam[0]/2) 
        offsetY = int(self.tam[1]/2)
        nodo = arbolquad.nodos[0]
        # gfxdraw.aacircle(self.pantalla, int(nodo.data[5][0] + offsetX), int(nodo.data[5][1] + offsetY), 2, (0,150,0))
        # gfxdraw.filled_circle(self.pantalla, int(nodo.data[5][0] + offsetX), int(nodo.data[5][1] + offsetY), 2, (0,150,0))
    
    def aux_pintarArbolQuad(self, nodo, escala):
        
        if str(type(nodo.data))=="<class 'list'>":
            offsetX = int(self.tam[0]/2) 
            offsetY = int(self.tam[1]/2)
            pygame.draw.rect(self.pantalla, (255,0,0), (nodo.data[1][0]*escala + offsetX ,
                                                    nodo.data[1][3]*escala + offsetY,
                                                    nodo.data[1][2]*escala-nodo.data[1][0]*escala,
                                                    nodo.data[1][1]*escala-nodo.data[1][3]*escala), 2)
            gfxdraw.aacircle(self.pantalla, int(nodo.data[5][0]*escala + offsetX), int(nodo.data[5][1]*escala + offsetY), int(4/(nodo.data[2]+1)), (0,150,0))
            gfxdraw.filled_circle(self.pantalla, int(nodo.data[5][0]*escala + offsetX), int(nodo.data[5][1]*escala + offsetY), int(4/(nodo.data[2]+1)), (0,150,0))
            # print("pintando", str(nodo))
            for v in nodo.vecinos.values():
                # print(str(v))
                if str(type(v.data))=="<class 'list'>":
                    # print(v.data[2],">",nodo.data[2], " == ",v.data[2] > nodo.data[2])
                    if v.data[2] > nodo.data[2]:
                        self.aux_pintarArbolQuad(v, escala)
        


        
        
if __name__ == '__main__':
    import pygame
    from math import pi
    import math as mm

    # Initialize pygame
    pygame.init()

    # Set the height and width of the screen
    size = [400, 300]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Example code for the draw module")

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    while not done:
        # This limits the while loop to a max of 60 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(60)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        # Clear the screen and set the screen background
        screen.fill("white")

        # Draw on the screen a green line from (0, 0) to (50, 30)
        # 5 pixels wide. Uses (r, g, b) color - medium sea green.
        pygame.draw.line(screen, (60, 179, 113), [0, 0], [50, 30], 5)

        # Draw on the screen a green line from (0, 50) to (50, 80)
        # Because it is an antialiased line, it is 1 pixel wide.
        # Uses (r, g, b) color - medium sea green.
        pygame.draw.aaline(screen, (60, 179, 113), [0, 50], [50, 80], True)

        # Draw on the screen 3 black lines, each 5 pixels wide.
        # The 'False' means the first and last points are not connected.
        pygame.draw.lines(
            screen, "black", False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5
        )

        # Draw a rectangle outline
        pygame.draw.rect(screen, "black", [75, 10, 50, 20], 2)

        # Draw a solid rectangle. Same color as "black" above, specified in a new way
        pygame.draw.rect(screen, (0, 0, 0), [150, 10, 50, 20])

        # Draw a rectangle with rounded corners
        pygame.draw.rect(screen, "green", [115, 210, 70, 40], 10, border_radius=15)
        pygame.draw.rect(
            screen,
            "red",
            [135, 260, 50, 30],
            0,
            border_radius=10,
            border_top_left_radius=0,
            border_bottom_right_radius=15,
        )

        # Draw an ellipse outline, using a rectangle as the outside boundaries
        pygame.draw.ellipse(screen, "red", [225, 10, 50, 20], 2)

        # Draw an solid ellipse, using a rectangle as the outside boundaries
        pygame.draw.ellipse(screen, "red", [300, 10, 50, 20])

        # This draws a triangle using the polygon command
        pygame.draw.polygon(screen, "black", [[100, 100], [0, 200], [200, 200]], 5)

        # Draw an arc as part of an ellipse.
        # Use radians to determine what angle to draw.
        pygame.draw.arc(screen, "black", [210, 75, 150, 125], 0, pi / 2, 2)
        pygame.draw.arc(screen, "green", [210, 75, 150, 125], pi / 2, pi, 2)
        pygame.draw.arc(screen, "blue", [210, 75, 150, 125], pi, 3 * pi / 2, 2)
        pygame.draw.arc(screen, "red", [210, 75, 150, 125], 3 * pi / 2, 2 * pi, 2)

        # Draw a circle
        pygame.draw.circle(screen, "blue", [60, 250], 40)
        pygame.draw.circle(screen, "red", [60, 250], 3)

        # Draw only one circle quadrant
        pygame.draw.circle(screen, "blue", [250+ 50 * mm.cos(2*mm.pi * pygame.time.get_ticks()/1000) , 250 + 50 * mm.sin(pygame.time.get_ticks()/1000) ], 40, 0, draw_top_right=True)
        pygame.draw.circle(screen, "red", [250, 250], 40, 30, draw_top_left=True)
        pygame.draw.circle(screen, "green", [250, 250], 40, 20, draw_bottom_left=True)
        pygame.draw.circle(screen, "black", [250, 250], 40, 10, draw_bottom_right=True)

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()

    # Be IDLE friendly
    pygame.quit()