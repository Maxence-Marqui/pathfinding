import pygame
import heapq
import sys
import time
import json

from pygame.sprite import groupcollide

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

pygame.init()

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
deep_search_first_button= Button((WIDTH/4*3.25)-(150/2),275,150,50,small_font,"Deep Search First",color_button)
dijkstra_button= Button((WIDTH/4*3.25)-(150/2),350,150,50,small_font,"Dijkstra",color_button)
A_star_button= Button((WIDTH/4*3.25)-(150/2),425,150,50,small_font,"A*",color_button)

custom_grid_button= Button((WIDTH/10*2)-(175/2),500,175,50,small_font,"Grille customisée",color_button)
premade_grid_button= Button((WIDTH/10*5)-(175/2),500,175,50,small_font,"Grille prédeterminée",color_button)

launch_button = Button((WIDTH/10*3.5)-(350/2),600,350,50,small_font,"Lancer la simulation",clicked_color_button)
quit_button = Button(612,700,100,35,small_font,"Quittez",color_button)

grayed_buttons_algo = []
grayed_buttons_grid = []

#Algo menu
reset_all_button = Button((WIDTH/10*8.75)-(175/2),50,175,50,small_font,"Reset la map",color_button)
reset_algo_button = Button((WIDTH/10*8.75)-(175/2),125,175,50,small_font,"Reset l'algorithme",color_button)

save_label = small_font.render("Nom de la map:",1,(255,255,255))
map_name_input_box = InputBox((WIDTH/10*8.75)-(175/2),250,174,50)
save_button = Button((WIDTH/10*8.75)-(175/2),315,175,50,small_font,"Sauvegarder la map",color_button)

breadth_first_button_algo = Button(450,600,125,40,small_font,"Breadth first",color_button)
deep_first_button_algo = Button(450+150,600,125,40,small_font,"Deep first",color_button)
dijkstra_button_algo = Button(450,650,125,40,small_font,"Dijkstra",color_button)
a_star_button_algo = Button(450+150,650,125,40,small_font,"A*",color_button)


class Node():
    def __init__(self,row,column,node_dimension,total_rows,total_columns):
        self.row = row
        self.column = column
        self.node_dimension = node_dimension
        self.total_rows = total_rows
        self.total_columns = total_columns
        self.neighbors = []
        self.x = row * self.node_dimension
        self.y = column * self.node_dimension
        self.color = color_active
        self.ancestor = set()
        self.generation = None
        self.weight = 1
        self.distance_from_start = 0
        self.distance_from_end = 9999999
        self.heuristic_distance = None
    
    def get_pos(self):
        return self.row, self.column

    def blocked(self):
        self.color = RED

    def open_path(self):
        self.color = DARKER_GREEN 

    def explored(self):
        self.color = GREEN
    
    def wall(self):
        self.color = BLACK
    
    def start(self):
        self.color = YELLOW
    
    def end(self):
        self.color = TURQUOISE

    def reset(self):
        self.color = color_active

    def draw(self):
        rect = pygame.Rect((self.row*self.node_dimension)+50,(self.column*self.node_dimension)+50,self.node_dimension,self.node_dimension)
        pygame.draw.rect(screen,self.color,rect)
        pygame.draw.rect(screen,(150,150,150),rect,1)

    def update_neighbor(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.column][self.row + 1].color == BLACK: # DOWN
            self.neighbors.append(grid[self.column][self.row + 1])

        if self.row > 0 and not grid[self.column][self.row - 1].color == BLACK: # UP
            self.neighbors.append(grid[self.column][self.row - 1])

        if self.column < self.total_columns - 1 and not grid[self.column + 1][self.row].color == BLACK: # RIGHT
            self.neighbors.append(grid[self.column + 1][self.row])

        if self.column > 0 and not grid[self.column - 1][self.row].color == BLACK: # LEFT
            self.neighbors.append(grid[self.column - 1][self.row])

    def click(self, pos):
        if pos[0] > self.x+50 and pos[0] < self.x+50 + self.node_dimension:
            if pos[1] > self.y+50 and pos[1] < self.y+50 + self.node_dimension:
                return True
        return False

    def father(self,generation):
        self.generation = generation

    def get_distance_from_start(self):
        return self.distance_from_start

    def __lt__(self, other):
	    return False

def create_grid(rows, columns,node_dimension):
    grid = []
    for column in range(columns):
        grid.append([])
        for row in range(rows):
            node = Node(row,column,node_dimension,rows,columns)
            grid[column].append(node)
    return grid

def draw(grid,rows,columns):
    rows = int(rows)
    columns = int(columns)

    for row in grid:
        for node in row:
            node.draw()
    
    pygame.display.update()

def coloring(grid,start_node,end_node):
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0]:
        for row in grid:
            for node in row:
                if node.click(pos) and start_node is None:
                    node.start()
                    start_node = node
                    
                elif node.click(pos) and node.color != YELLOW and not end_node:
                    node.end()
                    end_node = node

                elif node.click(pos) and node.color != YELLOW and node.color != TURQUOISE:
                    node.wall()
    if click[2]:
        for row in grid:
            for node in row:
                if node.click(pos):
                    if node.color == YELLOW:
                        start_node = None
                    if node.color == TURQUOISE:
                        end_node = None
                    node.color = color_active
                

    return start_node,end_node
    
def pathfinding(rows, columns,algo,grid):
    
    def reset_algo(end,starting, finished,generation,back_track):
        end = None
        starting = 0
        finished = 0

        generation = 1
        visited
        back_track = set()

        for row in grid:
            for node in row:
                node.neighbors = []
                if node.color == GREEN or node.color == DARKER_GREEN or node.color == RED:
                    node.color = color_active
                node.generation = 0
        starting_loop = True
        return end,starting, finished,generation,back_track,starting_loop
    
    def reset_all(end,start_node,end_node,starting,finished,generation,back_track):
        end = None
        start_node = None
        end_node = None
        starting = 0
        finished = 0

        generation = 1
        back_track = []

        for row in grid:
            for node in row:
                node.neighbors = []
                node.color = color_active
                node.generation = 0
        return end,start_node,end_node,starting,finished,generation,back_track

    run = True

    grayed_buttons_algo = []
    if algo == "BFS":
        breadth_first_button_algo.color = clicked_color_button
        grayed_buttons_algo.append(breadth_first_button_algo)

    if algo == "DFS":
        deep_first_button_algo.color = clicked_color_button
        grayed_buttons_algo.append(deep_first_button_algo)
    
    if algo == "DIJ":
        dijkstra_button_algo.color = clicked_color_button
        grayed_buttons_algo.append(dijkstra_button_algo)
    
    if algo == "A*":
        a_star_button_algo.color = clicked_color_button
        grayed_buttons_algo.append(a_star_button_algo)
    
    start_node = None
    end_node = None

    for row in grid:
        for node in row:
            if node.color == YELLOW:
                start_node = node
            if node.color == TURQUOISE:
                end_node = node
    
    visited = set()
    explored_next = set()
    rows = int(rows)
    columns = int(columns)
    back_track = set()
    
    start_time_breadth = 0.000
    start_time_deep = 0.000
    start_time_dij = 0.000
    start_time_a_star = 0.000

    current_time_breadth = start_time_breadth
    current_time_deep = start_time_deep
    current_time_dij = start_time_dij
    current_time_a_star = start_time_a_star

    breadth_count = str(0)
    deep_count = str(0)
    dij_count = str(0)
    a_star_count = str(0)

    breadth_back_track = str(0)
    deep_back_track = str(0)
    dij_back_track = str(0)
    a_star_back_track = str(0)

    starting = None
    end = None

    generation = 1
    finished = 0
        
    while run:
        keys = pygame.key.get_pressed()

        screen.fill((30,30,30))
        reset_all_button.draw()
        reset_algo_button.draw()
        screen.blit(save_label,(587,225))
        save_button.draw()
        map_name_input_box.draw()
        screen.blit(launch_label,(450,575))

        quit_button.draw()

        temps = small_font.render("Durée",1,(255,255,255))
        explored = small_font.render("Explorées",1,(255,255,255))
        trajet = small_font.render("Trajet",1,(255,255,255))
        
        screen.blit(temps,(220,575))
        screen.blit(explored,(280,575))
        screen.blit(trajet,(370,575))

        timer_breadth = small_font.render(str(round(current_time_breadth-start_time_breadth,2))+"s",1,(255,255,255))
        timer_deep = small_font.render(str(round(current_time_deep-start_time_deep,2))+"s",1,(255,255,255))
        timer_dijsktra = small_font.render(str(round(current_time_dij-start_time_dij,2))+"s",1,(255,255,255))
        timer_a_star = small_font.render(str(round(current_time_a_star-start_time_a_star,2))+"s",1,(255,255,255))

        screen.blit(timer_breadth,(230,600))
        screen.blit(timer_deep,(230,625))
        screen.blit(timer_dijsktra,(230,650))
        screen.blit(timer_a_star,(230,675))

        breadth_expanded = small_font.render(str(breadth_count),1,(255,255,255))
        deep_expanded = small_font.render(str(deep_count),1,(255,255,255))
        dij_expanded = small_font.render(str(dij_count),1,(255,255,255))
        a_star_expanded = small_font.render(str(a_star_count),1,(255,255,255))

        screen.blit(breadth_expanded,(310,600))
        screen.blit(deep_expanded,(310,625))
        screen.blit(dij_expanded,(310,650))
        screen.blit(a_star_expanded,(310,675))

        breadth_back_track_count = small_font.render(str(breadth_back_track),1,(255,255,255))
        deep_back_track_count = small_font.render(str(deep_back_track),1,(255,255,255))
        dij_back_track_count = small_font.render(str(dij_back_track),1,(255,255,255))
        a_star_back_track_count = small_font.render(str(a_star_back_track),1,(255,255,255))

        screen.blit(breadth_back_track_count,(388,600))
        screen.blit(deep_back_track_count,(388,625))
        screen.blit(dij_back_track_count,(388,650))
        screen.blit(a_star_back_track_count,(388,675))

        breadth_first_button_algo.draw()
        dijkstra_button_algo.draw()
        deep_first_button_algo.draw()
        a_star_button_algo.draw()

        breadth_name = small_font.render("Breadth First Search:",1,(255,255,255))
        deep_name = small_font.render("Depth First Search:",1,(255,255,255))
        dijkstra_name = small_font.render("Dijkstra:",1,(255,255,255))
        a_star_name = small_font.render("A* :",1,(255,255,255))
        
        screen.blit(breadth_name,(50,600))
        screen.blit(deep_name,(50,625))
        screen.blit(dijkstra_name,(50,650))
        screen.blit(a_star_name,(50,675))

        if keys[pygame.K_SPACE]:
            end,starting,finished,generation,back_track,starting_loop = reset_algo(end,starting, finished,generation,back_track)
            if start_node and end_node:
                starting_loop = True
                starting = 1

                if algo == "BFS":
                    visited = set()
                    explored_next = set()
                    start_time_breadth = time.time()
                if algo == "DFS":
                    visited = []
                    explored_next = []
                    start_time_deep = time.time()
                
                if algo == "DIJ":
                    explored_next = []
                    visited = set()
                    start_time_dij = time.time()
                
                if algo == "A*":
                    explored_next = []
                    visited = set()
                    start_time_a_star = time.time()

        draw(grid,rows,columns)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            map_name_input_box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if breadth_first_button_algo.click(pos):
                    algo = "BFS"
                    for button in grayed_buttons_algo:
                        button.color = color_button
                    breadth_first_button_algo.color = clicked_color_button
                    grayed_buttons_algo.append(breadth_first_button_algo)
                    end,starting,finished,generation, back_track,starting_loop= reset_algo(end,starting,finished,generation, back_track)

                if deep_first_button_algo.click(pos):
                    algo = "DFS"
                    for button in grayed_buttons_algo:
                        button.color = color_button
                    deep_first_button_algo.color = clicked_color_button
                    grayed_buttons_algo.append(deep_first_button_algo)
                    end,starting,finished,generation, back_track,starting_loop= reset_algo(end,starting,finished,generation, back_track)
                
                if dijkstra_button_algo.click(pos):
                    algo = "DIJ"
                    for button in grayed_buttons_algo:
                        button.color = color_button
                    dijkstra_button_algo.color = clicked_color_button
                    grayed_buttons_algo.append(dijkstra_button_algo)
                    end,starting,finished,generation, back_track,starting_loop= reset_algo(end,starting,finished,generation, back_track)

                if a_star_button_algo.click(pos):
                    algo = "A*"
                    for button in grayed_buttons_algo:
                        button.color = color_button
                    a_star_button_algo.color = clicked_color_button
                    grayed_buttons_algo.append(a_star_button_algo)
                    end,starting,finished,generation, back_track,starting_loop= reset_algo(end,starting,finished,generation, back_track)
                
                if reset_algo_button.click(pos):
                    end,starting,finished,generation, back_track,starting_loop= reset_algo(end,starting,finished,generation, back_track)

                if reset_all_button.click(pos):
                    end,start_node,end_node,starting,finished,generation,back_track= reset_all(end,start_node,end_node,starting,finished,generation,back_track)
                    grayed_buttons_algo = []

                    breadth_count = str(0)
                    deep_count = str(0)
                    dij_count = str(0)
                    a_star_count = str(0)

                    breadth_back_track = str(0)
                    deep_back_track = str(0)
                    dij_back_track = str(0)
                    a_star_back_track = str(0)

                    start_time_breadth = 0.000
                    start_time_deep = 0.000
                    start_time_dij = 0.000
                    start_time_a_star = 0.000
                
                if save_button.click(pos):
                    save_map(grid,map_name_input_box.text)
                            
                if quit_button.click(pos):
                    finished = 1
                    starting = 0
                    breadth_first_button_algo.color = color_button
                    deep_first_button_algo.color = color_button
                    dijkstra_button_algo.color = color_button
                    a_star_button_algo.color = color_button

                    run = False
                    

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                    
        if starting:
            if algo == "BFS":
                if starting_loop:
                    start_node.generation = 0
                explored_next.add(start_node)
                starting_loop = False
                explored_next,visited, end,generation,back_track = breadth_first(grid,explored_next,visited,end,generation,back_track)
                start_node.color, end_node.color = YELLOW, TURQUOISE
                for node in start_node.neighbors:
                    if node.color == RED:
                        starting = 0
                        finished = 1
                current_time_breadth = time.time()
                breadth_count = str(len(visited))
                breadth_back_track = str(len(back_track))


            if algo == "DFS":
                if starting_loop:
                    explored_next.append(start_node)
                    current_node = start_node
                    current_node.generation = 0
                starting_loop = False
                explored_next,visited,end,generation,current_node,back_track = deep_first(grid,explored_next,visited,end,generation,current_node,back_track)
                start_node.color,end_node.color = YELLOW,TURQUOISE

                for node in start_node.neighbors:
                    if node.color == RED:
                        starting = 0
                        finished = 1
                        back_track.remove(node)

                current_time_deep = time.time()
                deep_count = str(len(visited))
                deep_back_track = str(len(back_track)-1)
            
            if algo == "DIJ":
                if starting_loop:
                    heapq.heappush(explored_next,(start_node.get_distance_from_start(),start_node))
                    current_node = (start_node.distance_from_start,start_node)
                starting_loop = False
                explored_next,visited,current_node,end,back_track = dijktra(grid,current_node,explored_next,visited,end,back_track)
                start_node.color,end_node.color = YELLOW,TURQUOISE

                for node in start_node.neighbors:
                    if node.color == RED:
                        starting = 0
                        finished = 1
                        back_track.remove(node)

                current_time_dij = time.time()
                dij_count = str(len(visited))
                dij_back_track = str(len(back_track)-1)
            
            if algo == "A*":
                
                if starting_loop:
                    for row in grid:
                        for node in row:
                            if node.color == TURQUOISE:
                                pos_end_node = (node.row,node.column)

                    start_node.distance_from_end = abs(start_node.row - pos_end_node[0]) + abs(start_node.column - pos_end_node[1])
                    start_node.heuristic_distance = start_node.distance_from_start + start_node.distance_from_end
                    heapq.heappush(explored_next,(start_node.heuristic_distance,start_node))
                    current_node = (start_node.heuristic_distance,start_node)
                    
                starting_loop = False
                explored_next,visited,current_node,end,back_track = a_star(grid,current_node,explored_next,visited,end,back_track,pos_end_node)
                start_node.color,end_node.color = YELLOW,TURQUOISE

                for node in start_node.neighbors:
                    if node.color == RED:
                        starting = 0
                        finished = 1
                        back_track.remove(node)
                        


                current_time_a_star = time.time()
                a_star_count = str(len(visited))
                a_star_back_track = str(len(back_track))

        if not starting and not finished:
            start_node, end_node = coloring(grid,start_node,end_node)
        
        pygame.display.update()

def breadth_first(grid,explored_next,visited,end,generation,back_track):
    if not end :
        queue = []
        for current in explored_next:
            current.update_neighbor(grid)
            if not current.generation:
                current.father(generation)
            for node in current.neighbors:
                if node not in visited:
                    queue.append(node)
                if node.color == TURQUOISE:
                    end = current
                    end.color = RED
                node.open_path()
            visited.add(current)
        explored_next = set()
        generation += 1

        for node in queue:
            explored_next.add(node)
            node.open_path()

        for node in visited:
            node.explored()
    else:
        back_track.add(end)
        if end.generation > 0:
            for back_node in end.neighbors:
                back_node.update_neighbor(grid)
                back_node.explored()
                if back_node.generation:
                    if back_node.generation < end.generation:
                        end = back_node
        for node in back_track:
            node.color = RED
    return explored_next,visited,end,generation,back_track

def deep_first(grid,explored_next,visited,end,generation,current_node,back_track):
    if not end :
        current_node.update_neighbor(grid)
        for node in current_node.neighbors:
            if not node.generation:
                node.generation = generation
            if node.color == TURQUOISE:
                end = node
                end.update_neighbor(grid)
            if node not in visited and node not in explored_next:
                explored_next.insert(0,node)
            node.open_path()
        
        visited.append(current_node)
        explored_next.remove(current_node)
        current_node = explored_next[0]

        for node in visited:
            node.explored()
        generation += 1
        
    else:
        back_track.add(end)
        if end.generation > 0:
            for back_node in end.neighbors:
                back_node.update_neighbor(grid)
                back_node.explored()

                if back_node.generation:
                    if back_node.generation < end.generation:
                        end = back_node
        for node in back_track:
            node.color = RED
    return explored_next,visited,end,generation,current_node,back_track

def dijktra(grid,current_node,explored_next,visited,end,back_track):
    if not end:
        current_node[1].update_neighbor(grid)
        for node in current_node[1].neighbors:
            if not node.distance_from_start:
                node.distance_from_start = current_node[1].distance_from_start + node.weight
            if node.color == TURQUOISE:
                end = node
                end.update_neighbor(grid)
            if not any(node in node_tuple for node_tuple in visited) and not any(node in node_tuple for node_tuple in explored_next):
                heapq.heappush(explored_next,(node.distance_from_start,node))
            node.open_path()

        visited.add(current_node)
        current_node = heapq.heappop(explored_next)

        for node in visited:
            node[1].explored()
    
    else:
        back_track.add(end)
        if end.distance_from_start > 0:
            for neighbor in end.neighbors:
                neighbor.update_neighbor(grid)
                if neighbor.distance_from_start:
                    if neighbor.distance_from_start <= end.distance_from_start:
                        end = neighbor
                        diff_to_end=end.distance_from_start - neighbor.distance_from_start 
                        end.distance_from_start = end.distance_from_start - diff_to_end
            for node in back_track:
                node.color = RED

    return explored_next,visited,current_node,end,back_track

def a_star(grid,current_node,explored_next,visited,end,back_track,pos_end_node):
    if not end:
        current_node[1].update_neighbor(grid)
        for node in current_node[1].neighbors:
            node.distance_from_end = abs(node.row - pos_end_node[0]) + abs(node.column - pos_end_node[1])
            if not node.distance_from_start:
                node.distance_from_start = current_node[1].distance_from_start + node.weight
            if not node.heuristic_distance:
                node.heuristic_distance = node.distance_from_start + node.distance_from_end
            if node.color == TURQUOISE:
                end = node
                end.update_neighbor(grid)
            if not any(node in node_tuple for node_tuple in visited) and not any(node in node_tuple for node_tuple in explored_next):
                heapq.heappush(explored_next,(node.heuristic_distance,node))
            node.open_path()

        visited.add(current_node)
        current_node = heapq.heappop(explored_next)

        for node in visited:
            node[1].explored()
    
    else:
        back_track.add(end)
        if end.distance_from_start > 0:
            for neighbor in end.neighbors:
                neighbor.update_neighbor(grid)
                if neighbor.distance_from_start:
                    if neighbor.distance_from_start <= end.distance_from_start:
                        end = neighbor
                        diff_to_end=end.distance_from_start - neighbor.distance_from_start 
                        end.distance_from_start = end.distance_from_start - diff_to_end
            for node in back_track:
                node.color = RED

    return explored_next,visited,current_node,end,back_track
    
def main_menu():
    algo = None
    grid_columns = 0
    grid_row = 0
    grid = None

    while True:

        screen.fill((30, 30, 30))
        screen.blit(game_name, (WIDTH/2 - game_name.get_width()/2, 50))
        screen.blit(author, (WIDTH/2 - author.get_width()/2,100))

        breadth_first_button.draw()
        A_star_button.draw()
        dijkstra_button.draw()
        deep_search_first_button.draw()

        row_input_box.draw()
        column_input_box.draw()

        screen.blit(row, (WIDTH/2 - game_name.get_width()/2, 200))
        screen.blit(columns, (WIDTH/2 - game_name.get_width()/2, 325))

        premade_grid_button.draw()
        custom_grid_button.draw()

        launch_button.draw()
        quit_button.draw()
        if algo and grid_columns and grid_row:
            launch_button.color = color_button

        for event in pygame.event.get():
            row_input_box.handle_event(event)
            column_input_box.handle_event(event)
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if breadth_first_button.click(pos):
                    for button in grayed_buttons_algo:
                        button.color = color_button
                    breadth_first_button.color = clicked_color_button
                    grayed_buttons_algo.append(breadth_first_button)
                    algo = "BFS"

                if A_star_button.click(pos):
                    for button in grayed_buttons_algo:
                        button.color = color_button
                    A_star_button.color = clicked_color_button
                    grayed_buttons_algo.append(A_star_button)
                    algo = "A*"

                if dijkstra_button.click(pos):
                    for button in grayed_buttons_algo:
                        button.color = color_button
                    dijkstra_button.color = clicked_color_button
                    grayed_buttons_algo.append(dijkstra_button)
                    algo = "DIJ"

                if deep_search_first_button.click(pos):
                    for button in grayed_buttons_algo:
                        button.color = color_button
                    deep_search_first_button.color = clicked_color_button
                    grayed_buttons_algo.append(deep_search_first_button)
                    algo = "DFS"

                if custom_grid_button.click(pos):
                    if row_input_box.text and column_input_box.text:
                        try:

                            grid_columns,grid_row = int(row_input_box.text),int(column_input_box.text)
                            for button in grayed_buttons_grid:
                                button.color = color_button
                                custom_grid_button.color = clicked_color_button
                            grayed_buttons_grid.append(custom_grid_button)
                        except ValueError:
                            print("error")
                            pass

                
                if premade_grid_button.click(pos):
                    grid_row,grid_columns,grid = load_map()

                    if grid_row != 0 and grid_columns != 0 and grid != 0:
                        for button in grayed_buttons_grid:
                            button.color = color_button
                        premade_grid_button.color = clicked_color_button
                        grayed_buttons_grid.append(premade_grid_button)
                
                if launch_button.click(pos):
                    if algo and grid_columns and grid_row:
                        for button in grayed_buttons_grid:
                            button.color = color_button
                        for button in grayed_buttons_algo:
                            button.color = color_button
                        if grid_row >= grid_columns:
                            node_dimension = algo_width // grid_row
                        else:
                            node_dimension = algo_height // grid_columns
                        if not grid:
                            grid = create_grid(grid_row, grid_columns,node_dimension)
                        pathfinding(grid_row,grid_columns,algo,grid)
                        grid = []
                        grid_row,grid_columns = None, None
                        if row_input_box.text and column_input_box.text:
                            grid_row, grid_columns = int(row_input_box.text),int(column_input_box.text)

                if quit_button.click(pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        CLOCK.tick(FPS)

def save_map(grid,map_name):

    grid_representation = []
    column = 0

    with open("map.json","r+") as file:
        for row in grid:
            grid_representation.append([])
            for node in row:
                if node.color == color_active:
                    grid_representation[column].append((" ",node.weight))
                if node.color == YELLOW:
                    grid_representation[column].append(("v",node.weight))
                if node.color == TURQUOISE:
                    grid_representation[column].append(("x",node.weight))
                if node.color == BLACK:
                    grid_representation[column].append(("#",node.weight))
            column +=1

        maps = json.load(file)
        maps[map_name] = grid_representation
        file.seek(0)
        json.dump(maps,file)

def load_map():

    grayed_button = []
    map_list = []
    dimensions_list = []
    delete_list = []
    rows = 0
    columns = 0
    x = 50
    y = 100
    grid = 0

    current_map = ""
    actual_choice = small_font.render(current_map, 1, (255,255,255))
    validate_button = Button(750/2-125,660,200,50,small_font,"Valider la map",color_button)

    with open("map.json","r+") as file:
        maps = json.load(file)
    
    for key in maps:
        key_map = Button(x,y,125,50,small_font,str(key),color_button)
        map_list.append(key_map)
        dimensions = small_font.render(str(len(maps[key]))+"x"+ str(len(maps[key][1])), 1, (255,255,255))
        dimensions_list.append(dimensions)

        y += 75
        if y > 600:
            y = 100
            x += 225
        
        if x > 600:
            break
    
    run = True
    
    while run == True:

        screen.fill((30, 30, 30))
        quit_button.draw()
        validate_button.draw()
        actual_choice = small_font.render(current_map, 1, (255,255,255))
        map_choice = small_font.render("Choix de map:", 1, (255,255,255))
        screen.blit(map_choice,(200,625))
        screen.blit(actual_choice,(325,625))

        for map in map_list:
            map.draw()
        
        for button in grayed_button:
            button.color = clicked_color_button

        
        x = 190
        y = 115
    
        for dimensions in dimensions_list:
            screen.blit(dimensions,(x,y))
            y += 75
            if y > 600:
                y = 115
                x += 225
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for element in zip(map_list,maps):
                    if element[0].click(pos):
                        for button in grayed_button:
                            button.color = color_button
                        grayed_button = []
                        element[0].color = clicked_color_button
                        grayed_button.append(element[0])
                        rows = len(maps[element[1]])
                        columns = len(maps[element[1]][1])
                        map_representation = maps[element[1]]
                        current_map = str(element[1]) + " " +  str(rows) + "x" + str(columns)
                        
                if quit_button.click(pos):
                    run = False
                    return int(rows), int(columns),grid

                if validate_button.click(pos):
                    if current_map:
                        if rows >= columns:
                                node_dimension = algo_width // rows
                        else:
                            node_dimension = algo_height // columns
                            
                        grid = create_grid(columns, rows,node_dimension)

                        for row in grid:
                            for node in row:
                                if map_representation[grid.index(row)][row.index(node)][0] == "v":
                                    node.color = YELLOW
                                if map_representation[grid.index(row)][row.index(node)][0] == "x":
                                    node.color = TURQUOISE
                                if map_representation[grid.index(row)][row.index(node)][0] == "#":
                                    node.color = BLACK
                                node.weight = map_representation[grid.index(row)][row.index(node)][1]

                        return int(rows),int(columns),grid

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        CLOCK.tick(FPS)

main_menu()