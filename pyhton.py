import sys

realArg = False
debug = False
fpath = ""


class Septit:
	"""Oh hey, the Septit"""
	
	_ATA = {0 : 3,
			1 : 1,
			2 : 2,
			3 : 6,
			4 : 5,
			5 : 6,
			6 : 0}
	
	_ATB = {0 : 2,
			1 : 3,
			2 : 6,
			3 : 5,
			4 : 1,
			5 : 0,
			6 : 4}
	
	_ATC = {0 : 6,
			1 : 2,
			2 : 3,
			3 : 1,
			4 : 5,
			5 : 0,
			6 : 4}
	
	def __init__(self, value : int):
		self.value = value % 7
	
	def ATA(self):
		self.value = self._ATA[self.value]
		
	def ATB(self):
		self.value = self._ATB[self.value]
		
	def ATC(self):
		self.value = self._ATC[self.value]

class Register:
	""" the 7 bit register """
	
	def __init__(self):
		self.register = [Septit(0),Septit(0),Septit(0),Septit(0),Septit(0),Septit(0),Septit(0)]
	
	def ATA(self, index : int):
		self.register[index].ATA()
	
	def ATB(self, index : int):
		self.register[index].ATB()
	
	def ATC(self, index : int):
		self.register[index].ATC()
		
	def to_int(self) -> int:
		ret_val : int = 0
		for i in self.register:
			ret_val *= 7
			ret_val += i.value
		return ret_val
	
	def to_str(self) -> str:
		retval : str = ""
		for i in self.register:
			retval += str(i.value)
		return retval
	
	def update(self, instr : str):
		inval : int = int(instr)
		for i in range (6, -1, -1):
			self.register[i] = Septit(inval % 7)
			inval //= 7

conversion = {"]" : 0,
			  "#" : 1,
			  "+" : 2,
			  "^" : 3,
			  ";" : 4,
			  "{" : 5,
			  ":" : 6,
			  ")" : 7,
			  "<" : 8,
			  "," : 9,
			  "6" : 10,
			  "\t" : 11,
			  "h" : 12,
			  "'" : 13,
			  "(" : 14,
			  "5" : 15,
			  ">" : 16,
			  "@" : 17,
			  "0" : 18,
			  "?" : 19,
			  "I" : 20,
			  "9" : 21,
			  "3" : 22,
			  "1" : 23,
			  "/" : 24,
			  "7" : 25,
			  "." : 26,
			  " " : 27,
			  "i" : 28,
			  "l" : 29,
			  "|" : 30,
			  "!" : 31,
			  "~" : 32,
			  "8" : 33,
			  "-" : 34,
			  "=" : 35,
			  "$" : 36,
			  "[" : 37,
			  "4" : 38,
			  "&" : 39,
			  "}" : 40,
			  "`" : 41,
			  "_" : 42,
			  "*" : 43,
			  "\"" : 44,
			  "\\" : 45,
			  "2" : 46,
			  "%" : 47,
			  "\n" : 48
			  }

def NOP():
	global ip
	ip += 1

def ATA():
	global ip, r, program
	dbg_print(" " + str(program[ip + 1].value))
	r.ATA(program[ip + 1].value)
	ip += 2

def ATB():
	global ip, r, program
	dbg_print(" " + str(program[ip + 1].value))
	r.ATB(program[ip + 1].value)
	ip += 2

def ATC():
	global ip, r, program
	dbg_print(" " + str(program[ip + 1].value))
	r.ATC(program[ip + 1].value)
	ip += 2

def op_4():
	global ip, op_code4, program
	ip += 1
	dbg_print(program[ip].value)
	op_code4[program[ip].value]()

def RDI():
	global r, ip
	r.update(input())
	ip += 1

def WRT():
	global ip, ip_len, program
	dbg_print(" ")
	wp : int = 0
	for i in range(0, ip_len):
		ip += 1
		dbg_print(program[ip].value)
		wp *= 7
		wp += program[ip].value
	while (wp >= len(program)):
		program.append(Septit(0))
	for i in r.register:
		if (wp == len(program)):
			if (get_ip_len(wp) > ip_len):
				return # This would expand the program too much.
			else:
				program.append(i)
		else:
			program[wp] = i
		wp += 1
		
	ip += 1 # I need to find the program length for starters.

def OUT():
	global out_width, outted, outvals, program, ip
	tmp = 1 / (1 + out_width) # this line exists only to cause a error if out_width is 0.
	for i in range (0, out_width):
		outted += 1
		#print (i)
		outvals *= 7
		outvals += program[i].value
		if (outted == 3):
			outted = 0
			print(chr(outvals), end='')
			outvals = 0
	ip += 1

def PLP():
	global ip, program, ip_len
	program.append(Septit(0))
	ip_len = get_ip_len(len(program))
	# adjust program length.
	ip += 1

def AOS():
	global out_width, r, ip
	out_width = r.to_int()
	#print (out_width)
	ip += 1

def END():
	exit()

def RNR():
	global ip, program, r, op_code,
	dbg_print(" " + str(program[ip + 1].value))
	ip += 1
	if (debug):
		input()
	dbg_print(r.to_str() + " - r > " + str(r.register[program[ip + 1].value].value))
	op_code[r.register[program[ip + 1].value].value]()
	ip += 1

def SLP():
	while (True):
		pass

def JMP():
	global ip, program, ip_len
	new_ip = 0
	dbg_print(" ")
	for i in range(0, ip_len):
		ip += 1
		dbg_print(program[ip].value)
		new_ip *= 7
		new_ip += program[ip].value
	ip = new_ip

op_code = {
	0 : NOP,
	1 : ATA,
	2 : ATB,
	3 : ATC,
	4 : op_4,
	5 : SLP,
	6 : JMP
	}
op_code4 = {
	0 : RDI,
	1 : WRT,
	2 : OUT,
	3 : PLP,
	4 : AOS,
	5 : END,
	6 : RNR
	}

def dbg_print (s):
	if (debug):
		print (s,end='')
		
def get_ip_len(l : int) -> int:
	retval : int = 0
	while (l > 0):
		retval += 1
		l //= 7
	return retval

def loadProgram(fpath):
	global program
	file = open(fpath, "r", newline='')
	codeText : str = file.read()
	for char in codeText:
		tmp : int = conversion[char]
		program.append(Septit(tmp // 7))
		program.append(Septit(tmp % 7))

for arg in sys.argv:
	if (realArg):
		if (arg == "--debug"):
			debug = True
		elif (arg.endswith(".py")):
			fpath = arg
	else:
		realArg = True
program=[]
loadProgram(fpath)
r = Register()
out_width = -1
outted = 0
outvals = 0
ip = 0
ip_len = get_ip_len(len(program))

while (True):
	dbg_print(r.to_str() + " - " + str (ip) + " > " + str(program[ip].value))
	op_code[program[ip].value]()
	if (debug):
		input()