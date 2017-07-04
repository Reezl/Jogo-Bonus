from threading import Thread
import pygame
import socket
import pickle
import sys
import threading

class Th(Thread):
	def __init__(self, func,args=()):
		Thread.__init__(self)
		self.func = func
		self.args = args
	def run(self):
		self.func(*self.args)

class Game:
	def __init__(self):
		self.screen = pygame.display.set_mode((600,600))
		pygame.display.set_caption('Cliente 2')
	def keyboard_close(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
class Player(Game):
	def __init__(self,nome='None',):
		Game.__init__(self)
		self.nome = nome
		self.x = 0
		self.y = 0
		self.jogador = pygame.rect.Rect((self.x,self.y, 25,25))
	
	def moves(self):
		k = pygame.key.get_pressed()
		if k[pygame.K_UP]:
			self.jogador.y -=1
		elif k[pygame.K_DOWN]:
			self.jogador.y +=1
		if k[pygame.K_LEFT]:
			self.jogador.x -=1
		elif k[pygame.K_RIGHT]:
			self.jogador.x +=1
		if self.jogador.y <0:
			self.jogador.y = 0
		elif self.jogador.y > 580:
			self.jogador.y = 580
		if self.jogador.x < 0:
			self.jogador.x = 0
		elif self.jogador.x > 580:
			self.jogador.x = 580
	
	def collideRect(self,player_2):
		if (self.jogador.colliderect(player_2)):
			print('Oloco Meu')
	
	
	
class Enemys:
	def __init__(self):
		self.cord = [(0,0)]
		self.inimigo = {}
	def criar_inimigos(self,player):
		if len(self.inimigo) <11:
			for ind,el in enumerate(self.cord):
				self.x,self.y = el
				self.inimigo[ind] = pygame.rect.Rect((self.x,self.y, 10,10))
			if (self.cord[0][0] != 0) and (self.cord[0][1] != 0):
				for key in self.inimigo:
					pygame.draw.rect(player.screen,(1,1,255),self.inimigo[key])

class Player_2:
	def __init__(self):
		#self.cord = [(0,0)]
		self.x,self.y = 0,0
		self.player_2 = pygame.rect.Rect((self.x,self.y,20,20))
	def desenhar_player_2(self,player):
		#if (self.x != 0) and (self.y != 0):
			#for ind, el in enumerate(self.cord):
				#self.x,self.y = el
				#pygame.draw.rect(player.screen,(255,0,134),self.player_2)
				#return self.player_2
		pygame.draw.rect(player.screen,(255,0,134),self.player_2)
		return self.player_2
				
	def collideRect(self,player):
		if (self.player_2.colliderect(player)):
			print('Oloco 222')
			


	
def enviar_pos(udp,dest, player):
	msg = [('Player')]
	msg.append((player.jogador[0],player.jogador[1]))
	msg_st = pickle.dumps(msg)
	udp.sendto(msg_st, dest)
	
def receber_desenhar(udp,player_2,enemy):
	msg, servidor = udp.recvfrom(65536)
	msg_ds = pickle.loads(msg)
	if msg_ds[0] == 'Player':
		msg_ds.remove(msg_ds[0])
		player_2.player_2.x,player_2.player_2.y = msg_ds[0][0],msg_ds[0][1]
	if msg_ds[0] == 'Inimigos':
		msg_ds.remove(msg_ds[0])
		enemy.cord = msg_ds
		
			
			
			
	
def loop_principal():
	#game = Game()
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	player = Player()
	enemy = Enemys()
	player_2 = Player_2()
	dest = ('192.168.1.252',65025,)
	clock = pygame.time.Clock()
	recon = False
	while True:
		#game.screen.fill((50,50,50))
		player.screen.fill((100,100,100))
		enemy.criar_inimigos(player)
		if recon == False:
			msg = pickle.dumps('C2')
			udp.sendto(msg,dest)
			recon = True
		#
		player.moves()
		t_1 = threading.Thread(target=enviar_pos,args=(udp,dest,player,))
		t_1.start()
		t_1.join()
		pygame.draw.rect(player.screen,(255,1,1),player.jogador)
		
		player_2.desenhar_player_2(player)
		t_2 = threading.Thread(target=receber_desenhar,args=(udp,player_2,enemy,))
		t_2.start()
		t_2.join()
		'''
		if rect_player_2 != None:
			player.collideRect(rect_player_2)
		player_2.collideRect(player.jogador)
		'''
		
		
		
		
		
		
		'''
		t_enviarPos = Th(enviar_pos,(udp,dest,player,))
		t_enviarPos.start()
		#t_enviarPos.join()
		
		t_receber_desenhar = Th(receber_desenhar,(udp,player,))
		t_receber_desenhar.start()
		#t_receber_desenhar.join()
		
		msg, servidor = udp.recvfrom(4096)
		msg_ds = pickle.loads(msg)
		
		if type(msg_ds) == pygame.Rect:
			pygame.draw.rect(player.screen, (255,255,1),msg_ds)'''
		
	
		
		
		player.keyboard_close()
		clock.tick(60)
		pygame.display.flip()
		

loop_principal()
