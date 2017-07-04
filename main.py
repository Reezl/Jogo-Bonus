from threading import Thread
from random import randint
import socket
import pygame
import pickle

class Th(Thread):
	def __init__(self, func, args=()):
		Thread.__init__(self)
		self.func = func
		self.args = args
	def run(self):
		self.func(*self.args)
class Enemys:
	def __init__(self):
		self.inimigos = [('Inimigos')]
		self.x = 0
		self.y = 0
	def criar_inimigos(self):
		for i in range(10):
			self.x = randint(0,590)
			self.y = randint(0,590)
			self.inimigos.append((self.x,self.y))
		return self.inimigos

def enviar_pos(udp,msg,cliente):
	udp.sendto(msg,cliente)
	#print('Enviando para ',cliente)
def enviar_pos2(udp,msg,cliente):
	udp.sendto(msg,cliente)
	#print('Enviando para 2 ',cliente)
	
def ouvir_receber(udp,cliente1,cliente2):
	msg, cliente = udp.recvfrom(4096)
	msg_ds = pickle.loads(msg)
	
	if cliente == cliente1:
		t_eTrocado = Th(enviar_pos,(udp,msg,cliente2))
		t_eTrocado.start()
		#t_eTrocado.join()
		
		
	elif cliente == cliente2:
		t_eTrocado2 = Th(enviar_pos2,(udp,msg,cliente1))
		t_eTrocado2.start()
		#print("Enviando :", msg_ds)
		#t_eTrocado2.join()
		
	
def find_ips(udp,cliente1,cliente2,recon=False):
	if recon == False:
		msg, cliente = udp.recvfrom(1024)
		msg_ds = pickle.loads(msg)
		if msg_ds == 'C1':
			cliente1 = cliente
			if cliente2 != None:
				recon =  True
		if msg_ds == 'C2':
			cliente2 = cliente
			if cliente1 != None:
				recon = True
	if (cliente1 != None) and (cliente2 != None):
		return cliente1, cliente2
	if cliente1 != None:
		return cliente1, None
	elif cliente2 != None:
		return None,cliente2
def enviar_ini(udp,cliente1,cliente2,ini):
	msg_ini = pickle.dumps(ini)
	udp.sendto(msg_ini,cliente1)
	udp.sendto(msg_ini,cliente2)
def loop_principal():
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp.bind(('192.168.1.252',65025))
	cliente1, cliente2 = None,None
	recon = False
	enemys = Enemys()
	change = False
	
	while True:
		cliente1, cliente2 = find_ips(udp,cliente1,cliente2,recon)
		if (cliente1 != None) and (cliente2 != None):
			recon = True
			#t_2 = Th(enviar_ini,(udp,cliente1,cliente2,ini))
			#t_2.daemon = True
			#t_2.start()
			#t_2.join()
			#ini = enemys.criar_inimigos()
			if change == False:
				ini = enemys.criar_inimigos()
				ini = pickle.dumps(ini)
				Th(udp.sendto,(ini,cliente1)).start()
				Th(udp.sendto,(ini,cliente2)).start()
				change = True
			
			#t_1 = Th(ouvir_receber,(udp,cliente1,cliente2))
			#t_1.daemon = True
			#t_1.start()
			#t_1.join()
			ouvir_receber(udp,cliente1, cliente2)

		
	udp.close()

loop_principal()
