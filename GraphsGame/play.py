import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
import dijjkstra as dj


class Pathfinder:
	def __init__(self,matrix):

		# inicial
		self.matrix = matrix
		self.grid = Grid(matrix = matrix)
		self.model_icon = pygame.image.load('GraphsGame/img/selection.png').convert_alpha()

		# busca do caminho
		self.path = []

		# Roomba
		self.game = pygame.sprite.GroupSingle(Game(self.empty_path))

	def empty_path(self):
		self.path = []

	def show_trace(self):
		mouse_pos = pygame.mouse.get_pos()
		row =  mouse_pos[1] // 32 # Posição exata do mouse na linha
		col =  mouse_pos[0] // 32 # Posição exata do mouse na coluna
		actual_value = self.matrix[row][col]
		if actual_value == 1:
			rect = pygame.Rect((col * 32,row * 32),(32,32))
			screen.blit(self.model_icon,rect)

	def create_path(self):

		# início
		begin_x, begin_y = self.game.sprite.get_coordinate()
		inicio = self.grid.node(begin_x,begin_y)

		# Fim
		mouse_pos = pygame.mouse.get_pos()
		end_x,end_y =  mouse_pos[0] // 32, mouse_pos[1] // 32
		end = self.grid.node(end_x,end_y)

		# o caminho é recalculado a cada click
		finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
		self.path,_ = finder.find_path(inicio,end,self.grid)
		self.grid.cleanup()
		self.game.sprite.define_path(self.path)

	def draw_trace(self): # Mostra o caminho a ser percorrido
		if self.path:
			points = []
			for point in self.path:
				x = (point[0] * 32) + 16
				y = (point[1] * 32) + 16
				points.append((x,y))

			pygame.draw.lines(screen,'#FF8C00',False,points,5)

	def update(self):
		self.show_trace()
		self.draw_trace()

		# roomba updating and drawing
		self.game.update()
		self.game.draw(screen)

class Game(pygame.sprite.Sprite):
	def __init__(self,empty_path):

		# base
		super().__init__()
		self.image = pygame.image.load('GraphsGame/img/character.png').convert_alpha()
		self.rect = self.image.get_rect(center = (60,60))

		# movimento
		self.pos = self.rect.center
		self.speed = 3
		self.direction = pygame.math.Vector2(0,0)

		# caminho
		self.path = []
		self.collision_rects = []
		self.empty_path = empty_path

	def get_coordinate(self): #Transforma a posição atual em uma coordenada
		col = self.rect.centerx // 32
		row = self.rect.centery // 32
		return (col,row)

	def define_path(self,path):
		self.path = path
		self.create_collision_rects()
		self.get_direction()

	def create_collision_rects(self): # Identificando colisão no mapa
		if self.path:
			self.collision_rects = []
			for point in self.path:
				x = (point[0] * 32) + 16
				y = (point[1] * 32) + 16
				rect = pygame.Rect((x - 2,y - 2),(4,4))
				self.collision_rects.append(rect)

	def get_direction(self):
		if self.collision_rects:
			begin = pygame.math.Vector2(self.pos)
			end = pygame.math.Vector2(self.collision_rects[0].center)
			self.direction = (end - begin).normalize()
		else:
			self.direction = pygame.math.Vector2(0,0)
			self.path = []

	def check_collisions(self):
		if self.collision_rects:
			for rect in self.collision_rects:
				if rect.collidepoint(self.pos):
					del self.collision_rects[0] # Remove o caminho quando alcança o objetivo
					self.get_direction()
		else:
			self.empty_path()

	def update(self):
		self.pos += self.direction * self.speed
		self.check_collisions()
		self.rect.center = self.pos

# base inicial
pygame.init()
screen = pygame.display.set_mode((1280,736))
clock = pygame.time.Clock()
# mapa

bg_surf = pygame.image.load('GraphsGame/img/pixelmap.png').convert()

matrix = [
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
pathfinder = Pathfinder(matrix)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN: # Cria o caminho a cada click
			pathfinder.create_path()

	screen.blit(bg_surf,(0,0))
	pathfinder.update()

	pygame.display.update()
	clock.tick(60)
