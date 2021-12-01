import pygame

pygame.init()

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = color_active if self.active else color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button():
    def __init__(self, x, y, width, height,font, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.text = text
        self.color = color
        
        
    def draw(self):
        pygame.draw.rect(screen,self.color, (self.x, self.y, self.width, self.height),0)
        text = self.font.render(self.text, 1, (255,255,255))
        screen.blit(text,(self.x +(self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def click(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

WIDTH = 750
HEIGHT = 750
SIZE = WIDTH, HEIGHT
FONT = pygame.font.Font(None, 32)
FPS = 120
screen = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()

algo_width = 500
algo_height = 500
algo_size =(algo_width,algo_height)
algo_screen = pygame.Surface(algo_size)

#colors
color_button = (170,170,170)
clicked_color_button = (100,100,100)
color_inactive = (150,150,150)
color_active = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 150, 0)
DARKER_GREEN = (0,100,0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

title_font = pygame.font.SysFont("comicsans", 70)
small_font = pygame.font.SysFont("comicsans", 25)
game_name = title_font.render("Pathfinding algorithms", 1, (255,255,255))
author = small_font.render("Maxence Marqui", 1, (255,255,255))


#Main menu
row_input_box = InputBox((WIDTH/10*2)-(175/2),225,250,30)
column_input_box = InputBox((WIDTH/10*2)-(175/2),350,250,30)

row = small_font.render("Nombre de rangées",1,(255,255,255))
columns = small_font.render("Nombre de colonnes",1,(255,255,255))
launch_label = small_font.render("Appuyez sur espace pour lancer",1,(255,255,255))

breadth_first_button= Button((WIDTH/4*3.25)-(150/2),200,150,50,small_font,"Breadth First",color_button)
deep_search_first_button= Button((WIDTH/4*3.25)-(150/2),275,150,50,small_font,"Depth Search First",color_button)
dijkstra_button= Button((WIDTH/4*3.25)-(150/2),350,150,50,small_font,"Dijkstra",color_button)
A_star_button= Button((WIDTH/4*3.25)-(150/2),425,150,50,small_font,"A*",color_button)

custom_grid_button= Button((WIDTH/10*2)-(175/2),500,175,50,small_font,"Grille customisée",color_button)
premade_grid_button= Button((WIDTH/10*5)-(175/2),500,175,50,small_font,"Grille prédeterminée",color_button)

launch_button = Button((WIDTH/10*3.5)-(350/2),600,350,50,small_font,"Lancer la simulation",clicked_color_button)
quit_button = Button(612,700,100,35,small_font,"Quitter",color_button)

reset_all_button = Button((WIDTH/10*8.75)-(175/2),50,175,50,small_font,"Reset la map",color_button)
reset_algo_button = Button((WIDTH/10*8.75)-(175/2),125,175,50,small_font,"Reset l'algorithme",color_button)

save_label = small_font.render("Nom de la map:",1,(255,255,255))
map_name_input_box = InputBox((WIDTH/10*8.75)-(175/2),250,174,50)
save_button = Button((WIDTH/10*8.75)-(175/2),315,175,50,small_font,"Sauvegarder la map",color_button)

breadth_first_button_algo = Button(450,600,125,40,small_font,"Breadth first",color_button)
deep_first_button_algo = Button(450+150,600,125,40,small_font,"Depth first",color_button)
dijkstra_button_algo = Button(450,650,125,40,small_font,"Dijkstra",color_button)
a_star_button_algo = Button(450+150,650,125,40,small_font,"A*",color_button)
