import os
import time
import random
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
        self.matriz=[] # se reconstroi toda iteração
        self.lixos = [] #list[Objetos tipo Lixo] (1,3,4) #TEM QUE SER FIXO, N PODE VARIAR 
        self.construirMapa()
        self.lixos_aleatorios()
    def construirMapa(self):
        self.matriz.clear()
        for _ in range(TAMANHO_AMBIENTE):
            linha = []
            for _ in range(TAMANHO_AMBIENTE):
                linha.append("\033[37m.\033[0;0m") #"."
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
            x, y = np.random.randint(1, 19, size=2) # Evita posições (0,0) e (19,19)
            if (x, y) not in organicos:
                organicos.append((x, y))
                self.adicionarLixo(x, y, 'O')
        # Gere lixos recicláveis
        reciclaveis = []
        while len(reciclaveis) < 5:
            x, y = np.random.randint(1, 19, size=2) # Evita posições (0,0) e (19,19)
            if (x, y) not in organicos and (x, y) not in reciclaveis:
                reciclaveis.append((x, y))
                self.adicionarLixo(x, y, 'R')
        
class Robo():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.status = False
    def mover_esquerda(self):
        if(self.x>0):
            self.x-=1
    def mover_direita(self):
        if self.x<19:
            self.x+=1
    def mover_cima(self):
        if self.y>0:
            self.y-=1
    def mover_baixo(self):
        if self.y<19:
            self.y+=1
    def carregandoLixo(self):
        return self.status
    
class App():
    def __init__(self):
        self.agente = Robo()
        self.mapa = Mapa()
        self.direcao = 1
        self.goBack=False
    def draw(self):
        self.drawAgente()
        self.drawLixo()
        print("  ", end='')
        print()
        for i in range(TAMANHO_AMBIENTE):
            print(f"\033[1;37m{i:2}\033[m|", end='')
            for j in range(TAMANHO_AMBIENTE):
                print(f"{self.mapa.matriz[i][j]:2}", end=' ')
            print("")
    def drawLixo(self):
        for lixo in self.mapa.lixos:
            self.mapa.matriz[lixo.y][lixo.x] = "\033[36m" + "*" + "\033[0;0m" if lixo.valor == "R" else "\033[33m" + "*" + "\033[0;0m"

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
        self.mapa.construirMapa() #renderiza do 0 mapa  
    def remover_lixo_se_existir(self,y,x):
        percep = self.mapa.matriz[y][x]  # . O R L
        if(percep != '.'): #teoria se alguma percepção for == "*" ai eu verifico o que é.
            if not self.agente.carregandoLixo():
                for lixo in self.mapa.lixos:
                    if(x == lixo.x and y == lixo.y):
                        self.agente.status=True
                        self.mapa.lixos.remove(lixo)
                        self.goBack=False
                        break
                    #self.irAteLixeira()
            else:
                pass#caso esteja carregando e encontrar algo, pode registrar em algum atributo
                    #de posições onde passou por algum lixo
        return False
    

    def zigZag(self):
            self.procurarLixo() #bom trocar essa funcao pra inspecionandoArea
            if(self.agente.x < 20 and self.agente.y < 20 and self.agente.status==False and self.goBack==False):
                if self.agente.x == 19 and self.direcao == 1:
                    self.agente.mover_baixo()
                    self.direcao = -1
                elif self.agente.x == 0 and self.direcao==-1:
                    self.agente.mover_baixo()
                    self.direcao = 1
                else:
                    self.agente.x+=self.direcao #vai pra esquerda ou direta depende da direcao
                return True
            self.irAteLixeira()
                
    def procurarLixo(self):
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
                self.remover_lixo_se_existir(y,x)                 
    def irAteLixeira(self):
        # Entregar lixo para o ponto de descarte
        if(self.goBack):
            self.agente.status=False
            self.retornarPosInicial()
        elif(self.agente.x==19 and self.agente.y==19):
            #voltar
            self.goBack=True
            self.direcao=-1
        elif self.agente.x < 19:
            self.agente.mover_direita() 
        elif self.agente.y < 19: #o if e executado primeiro mesmo elif tbm sendo verdadeiro
            self.agente.mover_baixo()
    
    def retornarPosInicial2(self):
        if self.agente.x > 0:
            self.agente.mover_esquerda()
        elif self.agente.y > 0:
            self.agente.mover_cima()
        else:
            self.goBack=False
            #self.agente.status=False
    def retornarPosInicial(self):
        if(self.agente.x==0 and self.agente.y==0):
            self.goBack=False
        else:
            if self.agente.x == 0 and self.direcao == -1:
               self.agente.mover_cima()
               self.direcao = 1
            elif self.agente.x == 19 and self.direcao == 1:
                self.agente.mover_cima()
                self.direcao = -1
            else:
                self.agente.x += self.direcao
        #return True
    def ir_ate_posicao(self,x,y):
        #ir exatamente ao mesmo ponto
        if(self.agente.x!=x and self.agente.y!=y):
            if self.agente.x < x:
                self.agente.mover_direita()
            elif self.agente.x > x:
                self.agente.mover_esquerda()
            if self.agente.y < y:
                self.agente.mover_baixo()
            elif self.agente.y > y:
                self.agente.mover_cima()
        else:
            exit()
        #exit()
    def loop(self):
        while True:
            os.system('clear')
            print(self.agente.x, self.agente.y, self.agente.carregandoLixo(), "goback=", self.goBack, "direcao=", self.direcao)
            self.drawMap()
            self.draw()
            self.zigZag()
            #input()
            time.sleep(SLEEP)
            if (len(self.mapa.lixos) == 0 and self.agente.x == 19 and self.agente.y == 19):
                break

app = App()
app.loop()


