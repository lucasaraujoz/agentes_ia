import os
import time
import random
import math
import numpy as np
SLEEP = 0.02
TAMANHO_AMBIENTE = 20


class Lixo():
    def __init__(self):
        self.x = None
        self.y = None
        self.valor = None

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setValor(self, valor):
        self.valor = valor

    def getValor(self):
        return self.valor


class Mapa():
    def __init__(self):
        self.matriz = []  # se reconstroi toda iteração
        # list[Objetos tipo Lixo] (1,3,4) #TEM QUE SER FIXO, N PODE VARIAR
        self.lixos = []
        self.construirMapa()
        self.lixos_aleatorios()

    def construirMapa(self):
        self.matriz.clear()
        for _ in range(TAMANHO_AMBIENTE):
            linha = []
            for _ in range(TAMANHO_AMBIENTE):
                linha.append("\033[37m.\033[0;0m")  # "."
            self.matriz.append(linha)

    def adicionarLixo(self, x, y, valor):
        lixo = Lixo()
        lixo.setX(x)
        lixo.setY(y)
        lixo.setValor(valor)
        self.lixos.append(lixo)

    def getMapa(self):
        return self.matriz

    def lixos_aleatorios(self):
        # Gere lixos orgânicos
        organicos = []
        while len(organicos) < 10:
            # Evita posições (0,0) e (19,19)
            x, y = np.random.randint(1, 19, size=2)
            if (x, y) not in organicos:
                organicos.append((x, y))
                self.adicionarLixo(x, y, 'O')
        # Gere lixos recicláveis
        reciclaveis = []
        while len(reciclaveis) < 5:
            # Evita posições (0,0) e (19,19)
            x, y = np.random.randint(1, 19, size=2)
            if (x, y) not in organicos and (x, y) not in reciclaveis:
                reciclaveis.append((x, y))
                self.adicionarLixo(x, y, 'R')


class Robo():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.status = False
        self.posicaoLixo = None
        self.lembrarLixos = []

    def mover_esquerda(self):
        if (self.x > 0):
            self.x -= 1

    def mover_direita(self):
        if self.x < 19:
            self.x += 1

    def mover_cima(self):
        if self.y > 0:
            self.y -= 1

    def mover_baixo(self):
        if self.y < 19:
            self.y += 1

    def carregandoLixo(self):
        return self.status


class App():
    def __init__(self):
        self.agente = Robo()
        self.mapa = Mapa()
        self.direcao = 1
        self.goBack = False
        self.levandoLixo = False
        self.objetivos = []
        self.importarObjetivos()

    def importarObjetivos(self):
        if (len(self.objetivos) > 0):
            self.objetivos.clear()
        for lixo in self.mapa.lixos:
            self.objetivos.append((lixo.x, lixo.y))

    def draw(self):
        self.drawAgente()
        self.drawLixo()
        print("  ", end='')
        print()
        for i in range(TAMANHO_AMBIENTE):
            # Usando a formatação ANSI para definir cor e estilo do texto
            print(f"\033[1;37m{i:2}\033[m|", end='')
            for j in range(TAMANHO_AMBIENTE):
                print(f"{self.mapa.matriz[i][j]:2}", end=' ')
            print("")

    def drawLixo(self):
        for lixo in self.mapa.lixos:#r=azul
            self.mapa.matriz[lixo.y][lixo.x] = "\033[36m" + "*" + \
                "\033[0;0m" if lixo.valor == "R" else "\033[33m" + \
                "*" + "\033[0;0m"

    def drawAgente(self):
        lista = [
            (self.agente.x - 1, self.agente.y),       # Oeste
            (self.agente.x + 1, self.agente.y),       # Leste
            (self.agente.x, self.agente.y + 1),       # Norte
            (self.agente.x, self.agente.y - 1),       # Sul
            (self.agente.x - 1, self.agente.y + 1),   # Noroeste
            (self.agente.x + 1, self.agente.y + 1),   # Nordeste
            (self.agente.x + 1, self.agente.y - 1),   # Sudeste
            (self.agente.x - 1, self.agente.y - 1),   # Sudoeste
        ]
        for percepcoes in lista:
            x = percepcoes[0]
            y = percepcoes[1]
            if x >= 0 and x < TAMANHO_AMBIENTE and y >= 0 and y < TAMANHO_AMBIENTE:
                # pass
                self.mapa.matriz[y][x] = '\033[34mX\033[0;0m'
        print("\033[0m")
        self.mapa.matriz[self.agente.y][self.agente.x] = '\033[34mA\033[0;0m'

    def drawMap(self):
        self.mapa.construirMapa()  # renderiza do 0 mapa

    def irAteLixeira(self):
        print("chamando irAteLixeira()")
        if (self.agente.x == 19 and self.agente.y == 19):
            # voltar
            # self.goBack=True
            self.levandoLixo = False
            self.importarObjetivos()
            # self.objetivos.pop(0)#tenho que remover aquilo que eu carreguei ou so atualizar a lista de objetivos sem
            self.direcao = -1
        elif self.agente.x < 19:
            self.agente.mover_direita()
        elif self.agente.y < 19:  # o if e executado primeiro mesmo elif tbm sendo verdadeiro
            self.agente.mover_baixo()

    def ir_ate_posicao(self, x, y):
        if (self.levandoLixo == True):
            self.irAteLixeira()
        else:
            if self.agente.x == x and self.agente.y == y:
                if not self.levandoLixo:
                    self.levandoLixo = True
                    # remove lixo
                    for l in self.mapa.lixos:
                        if self.agente.x == l.x and self.agente.y == l.y:
                            self.mapa.lixos.remove(l)
                            break
            elif self.levandoLixo == False:
                if self.agente.x != x:
                    if self.agente.x < x:
                        self.agente.mover_direita()
                    elif self.agente.x > x:
                        self.agente.mover_esquerda()
                elif self.agente.y != y:
                    if self.agente.y < y:
                        self.agente.mover_baixo()
                    elif self.agente.y > y:
                        self.agente.mover_cima()

    def distancia(self, ponto):
        return math.sqrt((self.agente.x - ponto[0])**2 + (self.agente.y - ponto[1])**2)

    def ordenar_lista_por_distancia(self):
        self.objetivos = sorted(
            self.objetivos, key=lambda ponto: self.distancia(ponto))

    def loop(self):
        while True:
            os.system('clear')
            print(self.agente.x, self.agente.y, "levandoLixo=",
                  self.levandoLixo, "goback=", self.goBack, "direcao=", self.direcao)
            print(
                f'posição ultimo lixo ={self.agente.posicaoLixo}, listadelixos = {self.objetivos}')
            self.drawMap()
            self.draw()
            self.ir_ate_posicao(self.objetivos[0][0], self.objetivos[0][1])
            #input()
            time.sleep(SLEEP)
            self.ordenar_lista_por_distancia()
            if (len(self.mapa.lixos) == 0 and self.agente.x == 19 and self.agente.y == 19):
                break


inicio = time.time()
app = App()
#tempo inicial
app.loop()
#tempo final
final = time.time()
print("Tempo de execução: {} segundos".format(final-inicio))

#Tempo de execução: 14.732276439666748 segundos
