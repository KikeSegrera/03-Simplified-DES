#Simplified DES
import fileinput

def permute(bits,permutation):
	'''
	Función para realizar permutaciones a nivel de bits
	bits: lista de bits a permutar
	permutation: lista con la permutación a realizar
	'''
	permutation = list(permutation)
	perm = ''
	for c in permutation:
		perm = perm + bits[int(c)]
	return perm

def split(text):
	'''
	Función para dividir un texto a la mitad y regresar sus partes
	text: Texto a dividir
	'''
	length = len(text)
	l = text[0:length//2]
	r = text[length//2:length]
	return [l,r]

def shiftleft(bits,n):
	'''
	Función para realizar una rotación de bits a la izquierda
	bits: bits a rotar
	n: numero de veces a rotar
	'''
	bits = list(bits)
	for i in range(0,n):
		b = bits.pop(0)
		bits.append(b)
	return bits

def subkeys(key):
	'''
	Función para generar las subllaves
	key: llave base
	'''
	key = permute(key,'2416390785')
	[rk,lk] = split(key)
	rk = shiftleft(rk,1)
	lk = shiftleft(lk,1)
	k1 = permute(rk+lk,'52637498')
	rk = shiftleft(rk,2)
	lk = shiftleft(lk,2)
	k2 = permute(rk+lk,'52637498')
	return [k1,k2]

def xor(a,b):
	'''
	Función que realiza la operación XOR entre dos cadenas de bits
	a: cadena 1
	b: cadena 2
	'''
	c = ''
	for n in range(0,len(a)):
		c = c + str(int(a[n]) ^ int(b[n]))
	return c

def bina(number):
	'''
	Convierte un número decimal a uno hexadecimal de 2 dígitos 
	number : número a convertir
	'''
	b = bin(number).split('b')[1]
	if len(b) < 2:
		b = '0' + b
	return b

def sbox(s,input):
	'''
	Función que se encarga de retornar los valores de la S-box expecificada
	s: S-box a utilizar
	input: entrada para la S-box
	'''
	r = input[0] + input[3]
	c = input[1] + input[2]
	result = bina(s[int(r,2)][int(c,2)])
	return result

def mixingfunc(key,block):
	'''
	Función "mixing" específica del algoritmo sDES
	key: llave a utillizar
	block: bloque a cifrar
	'''
	s0 = [[1,0,3,2], [3,2,1,0], [0,2,1,3], [3,1,3,2]]
	s1 = [[0,1,2,3], [2,0,1,3], [3,0,1,0], [2,1,0,3]]

	block = permute(block,'30121230')
	cipher = xor(block,key)
	[rc,lc] = split(cipher)
	rc = sbox(s0,rc)
	lc = sbox(s1,lc)
	cipher = permute(rc + lc,'1320')
	return cipher

def sdes(option,key,text):
	'''
	Realiza el algoritmo sDES
	key : llave a utilizar
	text : mensaje a cifrar
	'''
	rounds = 2
	ip = permute(text,'15203746')
	[l,r] = split(ip)
	keys = subkeys(key)
	if option == 'D':
		keys.reverse()
	for i in range(0,rounds):
		l = xor(l,mixingfunc(keys[i],r))
		if i < (rounds - 1):
			l,r = r,l
	ciphertext = permute(l + r,'30246175')
	return ciphertext

lines = []

for line in fileinput.input():
	line = line.replace('\n','')
	lines.append(line)

print(sdes(lines[0],lines[1],lines[2]))