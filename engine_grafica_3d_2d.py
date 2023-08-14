import pyximport
pyximport.install(language_level = 3)

from math import cos, sin, radians
try:
    from matrix_otimizado import Matrix, Vector
    print("Usando código compilado")
except:
    print("Código compilado só funciona no python 3.7, usando código não compilado")
    from matrix import Matrix, Vector
    
from multiprocessing import Process
from random import random

try:
    import colorC
    print("Usando código compilado")
except:
    print("Código compilado só funciona no python 3.7, usando código não compilado")
    class func_color:
        def __init__(self):
            pass
        
        def corC(self, x_1, x_2, y_1, y_2):
            color = [255,255,255]

            try:
                color[0] = (50000 / (x_1+x_2))%255
            except:
                pass
            try:
                color[1] = (80000 / (y_1+x_1+y_2+x_2))%255
            except:
                pass
            try:
                color[2] = (50000 / (y_1+y_2))%255
            except:
                pass

            return color
    colorC = func_color()

class Line():
    """
    Cria as linhas que montarão a imagem 3d.
    """
    __slots__ = ("start", "end", "resp1", "resp2")
    def __init__(self, start, end):
        self.start = Vector(start)
        self.end = Vector(end)
        

    def __int__(self):
        self.resp1 = []
        self.resp2 = []
        for i in range(len(self.start)):
            self.resp1.append(self.start[i])
            self.resp2.append(self.end[i])
        self.start.vector = tuple(self.resp1)
        self.end.vector = tuple(self.resp2)

    def __mul__(self,m):
        """
        Multiplica
        """
        self.start = m.__mul__(self.start)
        self.end = m.__mul__(self.end)
        self.__int__()
        return self

    def __add__(self,m):
        """
        Soma
        """
        self.start = self.start.__add__(m)
        self.end = self.end.__add__(m)
        return self

    def __repr__(self):
        """
        Representação da matriz.
        """
        return str(self.start) + str("<-->") + str(self.end)

    def __getitem__(self,index):
        """
        Consegue um dos vetores.
        """
        if index == 0:
            return self.start
        elif index == 1:
            return self.end

class Image:
    """
    Cria a imagem 3d.
    """
    __slots__ = ("lines", "polygons", "ativate", "lines", "polygons_print", "qnt", "m")
    def __init__(self, lines, polygons = []):
        """
        Pra você iniciar uma imagem você deve passar uma lista de linhas
        """
        self.lines = []
        self.polygons = []
        self.ativate = 0
        self.m = Matrix(((0,0,0),
                         (0,0,0),
                         (0,0,0)))
        
        for i in range(len(lines)):
            if type(lines[i]) != Line:
                self.lines.append(Line(lines[i][0],lines[i][1]))
            else:
                self.lines.append(lines[i])

        for i in range(len(polygons)):
            if type(polygons[i]) != list:
                self.polygons.append(Vector(polygons[i][0]),Vector(polygons[i][1]),Vector(polygons[i][2]))
            else:
                self.polygons.append(polygons[i])
                
        #Colocando eixo no meio da imagem:
        m_x, m_y, m_z = 0, 0, 0
        l_ = len(self.lines)
        for i in range(l_):
            m_x += self.lines[i].start.vector[0]/l_
            m_y += self.lines[i].start.vector[1]/l_
            m_z += self.lines[i].start.vector[2]/l_
        norm = Vector((int(m_x), int(m_y), int(m_z)))
            
        for i in range(l_):
            self.lines[i].start = self.lines[i].start - norm
            self.lines[i].end = self.lines[i].end - norm

        for i in range(len(self.polygons)):
            self.polygons[i][0] = self.polygons[i][0] - norm
            self.polygons[i][1] = self.polygons[i][1] - norm
            self.polygons[i][2] = self.polygons[i][2] - norm

        self.polygons_print = self.polygons
        self.qnt = 0

    def draw(self):
        """
        Desenha o objeto
        """
        for lines in self.lines:
            #Projetando linhas do plano 3d pro 2d:
            x_1 = int((camera.camera.vector[0] - lines.start.vector[0])/(camera.camera.vector[2] - lines.start.vector[2]) * camera.camera.vector[2])
            x_2 = int((camera.camera.vector[0] - lines.end.vector[0])/(camera.camera.vector[2] - lines.end.vector[2]) * camera.camera.vector[2])
            y_1 = int((camera.camera.vector[1] - lines.start.vector[1])/(camera.camera.vector[2] - lines.start.vector[2]) * camera.camera.vector[2])
            y_2 = int((camera.camera.vector[1] - lines.end.vector[1])/(camera.camera.vector[2] - lines.end.vector[2]) * camera.camera.vector[2])
            
            pygame.draw.line(screen, (255, 255, 255), (x_1, y_1), (x_2, y_2))

        if self.ativate == 1:
            self.balance()
            k = 0
            for faces in self.polygons_print[self.qnt:]:
                #Projetando polygonos:
                x_1 = int((camera.camera.vector[0] - faces[0][0])/(camera.camera.vector[2] - faces[0][2]) * camera.camera.vector[2])
                x_2 = int((camera.camera.vector[0] - faces[1][0])/(camera.camera.vector[2] - faces[1][2]) * camera.camera.vector[2])
                x_3 = int((camera.camera.vector[0] - faces[2][0])/(camera.camera.vector[2] - faces[2][2]) * camera.camera.vector[2])
                y_1 = int((camera.camera.vector[1] - faces[0][1])/(camera.camera.vector[2] - faces[0][2]) * camera.camera.vector[2])
                y_2 = int((camera.camera.vector[1] - faces[1][1])/(camera.camera.vector[2] - faces[1][2]) * camera.camera.vector[2])
                y_3 = int((camera.camera.vector[1] - faces[2][1])/(camera.camera.vector[2] - faces[2][2]) * camera.camera.vector[2])

                color = colorC.corC(x_1, x_2, y_1, y_2)
                pygame.draw.polygon(screen, color, [[x_1, y_1], [x_2, y_2], [x_3, y_3]])
                k = (k + 1) % len(self.lines)

    def balance(self):
        """
        Reorganiza ordem das faces dos poligonos
        """
        self.polygons = sorted(self.polygons, key = lambda x: min(x[0].vector[2]+x[1].vector[2],
                                                                  x[1].vector[2]+x[2].vector[2],
                                                                  x[0].vector[2]+x[2].vector[2]),
                               reverse = False)
        self.polygons_print = self.polygons
        
    def translation(self,x = 0.005, y = 0.005, z = 1):
        """
        Faz a operação de translação
        """
        self.m.matrix[0].vector = (1,0,x)
        self.m.matrix[1].vector = (0,1,y)
        self.m.matrix[2].vector = (0,0,1)
        
        for i in range(len(self.lines)):
            self.lines[i] = self.lines[i].__mul__(self.m)

        for i in range(len(self.polygons)):
            self.polygons[i][0] = self.m.__mul__(self.polygons[i][0])
            self.polygons[i][1] = self.m.__mul__(self.polygons[i][1])
            self.polygons[i][2] = self.m.__mul__(self.polygons[i][2])
        
    def scaling(self,x = 1.01 ,y = 1.01 ,z = 1):
        """
        Faz a operação de escala
        """
        self.m.matrix[0].vector = (x,0,0)
        self.m.matrix[1].vector = (0,y,0)
        self.m.matrix[2].vector = (0,0,z)
                    
        for i in range(len(self.lines)):
            self.lines[i] = self.lines[i].__mul__(self.m)
            
        for i in range(len(self.polygons)):
            self.polygons[i][0] = self.m.__mul__(self.polygons[i][0])
            self.polygons[i][1] = self.m.__mul__(self.polygons[i][1])
            self.polygons[i][2] = self.m.__mul__(self.polygons[i][2])
            

    def rotation_x(self,x = 0.01):
        """
        Faz a operação de rotação no eixo x
        """
        self.m.matrix[0].vector = (1,0,       0)
        self.m.matrix[1].vector = (0,cos(x),  sin(x))
        self.m.matrix[2].vector = (0,-sin(x), cos(x))

        for i in range(len(self.lines)):
            self.lines[i] = self.lines[i].__mul__(self.m)
           
        for i in range(len(self.polygons)):
            self.polygons[i][0] = self.m.__mul__(self.polygons[i][0])
            self.polygons[i][1] = self.m.__mul__(self.polygons[i][1])
            self.polygons[i][2] = self.m.__mul__(self.polygons[i][2])

    def rotation_y(self,y = 0.01): ############
        """
        Faz a operação de rotação no eixo y
        """
        self.m.matrix[0].vector = (cos(y),0,  -sin(y))
        self.m.matrix[1].vector = (0,     1,  0)
        self.m.matrix[2].vector = (sin(y),0,  cos(y))
        
        for i in range(len(self.lines)):
            self.lines[i] = self.lines[i].__mul__(self.m)
         
        for i in range(len(self.polygons)):
            self.polygons[i][0] = self.m.__mul__(self.polygons[i][0])
            self.polygons[i][1] = self.m.__mul__(self.polygons[i][1])
            self.polygons[i][2] = self.m.__mul__(self.polygons[i][2])

    def rotation_z(self,z = 0.01): ############
        """
        Faz a operação de rotação no eixo z
        """
        self.m.matrix[0].vector = (cos(z),    sin(z),     0)
        self.m.matrix[1].vector = (-sin(z),   cos(z),     0)
        self.m.matrix[2].vector = (0,         0,          1)
        
        for i in range(len(self.lines)):
            self.lines[i] = self.lines[i].__mul__(self.m)
          
        for i in range(len(self.polygons)):
            self.polygons[i][0] = self.m.__mul__(self.polygons[i][0])
            self.polygons[i][1] = self.m.__mul__(self.polygons[i][1])
            self.polygons[i][2] = self.m.__mul__(self.polygons[i][2])

    def zoom(self,z):
        """
        Da zoom no objeto
        """
        m_ = Vector((0,0,z))
        
        for i in range(len(self.lines)):
            self.lines[i] = self.lines[i].__add__(m_)

        for i in range(len(self.polygons)):
            self.polygons[i][0] = m_.__add__(self.polygons[i][0])
            self.polygons[i][1] = m_.__add__(self.polygons[i][1])
            self.polygons[i][2] = m_.__add__(self.polygons[i][2])

    def __repr__(self):
        """
        Representação da matriz.
        """
        return str(self.start) + str("<-->") + str(self.end)

    def __getitem__(self,index):
        """
        Obtem um valor do objeto
        """
        if type(index) == int:
            return self.lines[index]

    def __repr__(self):
        """
        Representação da imagem.
        """
        return str(self.lines)

def b_(pont_1:list, pont_2:list, porc:float):
    """
    pont_1 e pont_2 é uma lista das cordenadas em duas dimensões, por exemplo [1,3] onde x=1 e y=3;
    porc é a porcentagem de 0 a 1
    """
    
    return [(pont_2[0] - pont_1[0])* porc + pont_1[0],
            (pont_2[1] - pont_1[1])* porc + pont_1[1],
            (pont_2[2] - pont_1[2])* porc + pont_1[2]]#posição do ponto

def bezier(pont_1, pont_2, pont_3, prec):
    """
    pont_1, pont_2 e pont_3 é uma lista das cordenadas em duas dimensões, por exemplo [1,3] onde x=1 e y=3;
    O pont_2 é o ponto de ajuste;
    prec é a quantidade de pontos que serão armazenados
    """
    pontos = []
    for i in range(prec):
        n = 1/(prec-1) * (i)
        pontos.append(b_(b_(pont_1, pont_2, n), b_(pont_2, pont_3 , n), n))
    return pontos


class Camera:
    """
    Define a camera que é basicamente um plano.
    """
    def __init__(self, x, y, z = 5000):
        self.camera = Vector((x,y,z))        

def join_dots(dots):
    """
    Cria, em ordem, ligações dos pontos passados.
    """
    resp = []
    
    for i in range(-1,len(dots)-1):
        resp.append(Line(dots[i],dots[i+1]))

    return resp

def generate_polygons(plane):
    """
    Gera os polygonos da imagem por meio de um plano
    """
    k = []
    inic = Vector(plane[0][0])
    for i in range(len(plane)-2):
        k.append([inic,
                  Vector(plane[i+1][0]),
                  Vector(plane[i+2][0])])

    return k

def update_fps():
    fps = str(int(clock.get_fps()))
    return font.render(fps, 1, pygame.Color("coral"))

def update_camera_position():
    fps = str(camera.camera.vector)
    return font.render(fps, 1, pygame.Color("coral"))

def buttons(obj):
    if type(obj) != list:
        obj = [obj]

    global fps_

    keys = pygame.key.get_pressed()
        
    for i in range(len(obj)):
        if keys[pygame.K_LEFT]:
            obj[i].translation(x = 0.005, y = 0, z = 1)

        if keys[pygame.K_RIGHT]:
            obj[i].translation(x = -0.005, y = 0, z = 1)

        if keys[pygame.K_UP]:
            obj[i].translation(x = 0, y = 0.005, z = 1)

        if keys[pygame.K_DOWN]:
            obj[i].translation(x = 0, y = -0.005, z = 1)

        if keys[pygame.K_r]:
            obj[i].scaling(x = 1.001 ,y = 1.001 ,z = 1)

        if keys[pygame.K_f]:
            obj[i].scaling(x = 0.999 ,y = 0.999 ,z = 1)

        if keys[pygame.K_e]:
            obj[i].rotation_z(z = radians(0.8))

        if keys[pygame.K_d]:
            obj[i].rotation_z(z = radians(-0.8))

        if keys[pygame.K_w]:
            obj[i].rotation_y(y = radians(0.8))

        if keys[pygame.K_s]:
            obj[i].rotation_y(y =radians(-0.8))

        if keys[pygame.K_q]:
            obj[i].rotation_x(x = radians(0.8))

        if keys[pygame.K_a]:
            obj[i].rotation_x(x = radians(-0.8))

        if keys[pygame.K_KP1]:
            camera.camera = camera.camera.__add__(Vector((-1,0,0)))
        if keys[pygame.K_KP3]:
            camera.camera = camera.camera.__add__(Vector((1,0,0)))
        if keys[pygame.K_KP5]:
            camera.camera = camera.camera.__add__(Vector((0,-1,0)))
        if keys[pygame.K_KP2]:
            camera.camera = camera.camera.__add__(Vector((0,1,0)))
        if keys[pygame.K_KP7]:
            camera.camera = camera.camera.__add__(Vector((0,0,-10)))
        if keys[pygame.K_KP9]:
            camera.camera = camera.camera.__add__(Vector((0,0,10)))         
        if keys[pygame.K_KP4]:
            obj[i].zoom(10)
        if keys[pygame.K_KP6]:
            obj[i].zoom(-10)

        if keys[pygame.K_SPACE]:
            obj[i].ativate = 1
        if keys[pygame.K_RALT] or keys[pygame.K_LALT]:
            obj[i].ativate = 0

        if fps_ > 5:
            if keys[pygame.K_KP_MINUS]:
                if obj[i].qnt < len(obj[i].polygons):
                    obj[i].qnt += 1
                    
            if keys[pygame.K_KP_PLUS]:
                if obj[i].qnt > 0:
                    obj[i].qnt -= 1
            fps_ = 0
            
        fps_ += 1


if __name__ == "__main__":
    #Objeto:
    quadrado_baixo = join_dots([[200,200,200],
                                [500,200,200],
                                [500,200,500],
                                [200,200,500]])

    poligonos_baixo = generate_polygons(quadrado_baixo)

    quadrado_cima = join_dots([[200,500,200],
                               [500,500,200],
                               [500,500,500],
                               [200,500,500]])

    poligonos_cima = generate_polygons(quadrado_cima)

    quadrado_lados = [Line((200,200,200),(200,500,200)),
                      Line((500,200,200),(500,500,200)),
                      Line((500,200,500),(500,500,500)),
                      Line((200,200,500),(200,500,500))]

    q_inteiro = []
    q_inteiro.extend(quadrado_baixo)
    q_inteiro.extend(quadrado_cima)
    q_inteiro.extend(quadrado_lados)

    quadrado = Image(lines = q_inteiro,
                     polygons = [*poligonos_cima,
                                 *poligonos_baixo,
                                 [Vector((200,200,200)), Vector((200,500,200)), Vector((500,200,200))],
                                 [Vector((500,500,200)), Vector((200,500,200)), Vector((500,200,200))],
                                 [Vector((200,200,500)), Vector((200,500,500)), Vector((500,200,500))],
                                 [Vector((500,500,500)), Vector((200,500,500)), Vector((500,200,500))],
                                 [Vector((200,200,500)), Vector((200,500,200)), Vector((200,500,500))],
                                 [Vector((200,200,200)), Vector((200,500,200)), Vector((200,200,500))],
                                 [Vector((500,200,500)), Vector((500,500,200)), Vector((500,500,500))],
                                 [Vector((500,200,200)), Vector((500,500,200)), Vector((500,200,500))]])

    #-----------------------------------------------------------

    triangulo = Image(lines = [Line((250,500,0),(0,0,0)),
                       Line((0,0,0),(500,0,0)),
                       Line((500,0,0),(250,500,0)),
                       Line((250,500,0),(250,250,500)),
                       Line((0,0,0),(250,250,500)),
                       Line((500,0,0),(250,250,500))],
                      polygons = [[Vector((250,500,0)),Vector((0,0,0)),Vector((500,0,0))],
                                  [Vector((500,0,0)),Vector((250,500,0)),Vector((250,250,500))],
                                  [Vector((0,0,0)),Vector((250,500,0)),Vector((250,250,500))],
                                  [Vector((0,0,0)),Vector((500,0,0)),Vector((250,250,500))]])

    #-----------------------------------------------------------

    np = 40
    p1 = join_dots(bezier([0,0,500],[500,1000,500],[1000,0,500],np))
    p2 = join_dots(bezier([0,0,500],[500,-1000,500],[1000,0,500],np))
    p3 = join_dots(bezier([0,0,500],[500,0,1500],[1000,0,500],np))
    p4 = join_dots(bezier([500,500,500],[500,0,1500],[500,-500,500],np))
    
    circulo = Image(lines = [*p1, *p2, *p3, *p4],
                    polygons = [*generate_polygons(p1),
                                *generate_polygons(p2),
                                *generate_polygons(p3),
                                *generate_polygons(p4)])    

    #-----------------------------------------------------------


    import pygame

    #Camera:
    pygame.init()
    v_x = 1000
    v_y = 1000
    camera = Camera(int(v_x/2), int(v_y/2))
    screen = pygame.display.set_mode([v_x, v_y])

    #Clock
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    fps_ = 0
    
    running = True
    while running:
        #Botão fechar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Update da tela:
        #Fundo:
        screen.fill((0, 0, 0))

        #FPS:
        screen.blit(update_fps(), (10,0))
        screen.blit(update_camera_position(), (5, v_y - 25))

        #Objetos:
        quadrado.draw()
        #triangulo.draw()
        #circulo.draw()
        
        #Botões:
        buttons([quadrado])
        #buttons([triangulo])
        #buttons([circulo])
        
        clock.tick(75)

        #Tela
        pygame.display.flip()

    #Para fechar
    pygame.quit()  

    

