import re 
import sys 


next_available_register = 16

dest_table = {'null':'000', 'M':'001','D':'010',
				'MD': '011', 'A': '100', 'AM': '101',
				'AD': '110', 'AMD': '111'}

jump_table = {'null':'000', 'JGT':'001', 'JEQ':'010',
				'JGE': '011', 'JLT': '100', 'JNE': '101',
				'JLE': '110', 'JMP' : '111'}

comp_table = {'A': '110000', '-D': '001111', '-A': '110011', 'D': '001100', 'D+1': '011111', '-M': '110011', 'M-1': '110010', 'A+1': '110111', 'M': '110000', 'A-D': '000111', 'D-1': '001110', 'D|A': '010101', 'M+1': '110111', 'M-D': '000111', 'D|M': '010101', '!A': '110001', 'D-A': '010011', '!D': '001101', '!M': '110001', 'D-M': '010011', '1': '111111', '0': '101010', '-1': '111010', 'D+A': '000010', 'A-1': '110010', 'D&M': '000000', 'D+M': '000010', 'D&A': '000000'}

a_bit_off_comp_table = {'A': '110000', '-D': '001111', '-A': '110011', 'D': '001100', 'D+1': '011111', 'A+1': '110111', 'A-D': '000111', 'D-1': '001110', 'D|A': '010101', '!A': '110001', 'D-A': '010011', '!D': '001101', '1': '111111', '0': '101010', '-1': '111010', 'D+A': '000010', 'A-1': '110010', 'D&A': '000000'}

a_bit_on_comp_table = {'-M': '110011', 'M': '110000', '!M': '110001', 'D-M': '010011', 'M-1': '110010', 'D&M': '000000', 'M+1': '110111', 'M-D': '000111', 'D+M': '000010', 'D|M': '010101'}

symbols_table = {'THAT': '0000000000000100', 'R14': '0000000000001110', 'R15': '0000000000001111', 'R12': '0000000000001100', 'R13': '0000000000001101', 'R10': '0000000000001010', 'R11': '0000000000001011', 'KBD': '0110000000000000', 'R4': '0000000000000100', 'R5': '0000000000000101', 'R6': '0000000000000110', 'R7': '0000000000000111', 'R0': '0000000000000000', 'R1': '0000000000000001', 'R2': '0000000000000010', 'R3': '0000000000000011', 'SCREEN': '0100000000000000', 'R8': '0000000000001000', 'R9': '0000000000001001', 'THIS': '0000000000000011', 'SP': '0000000000000000', 'ARG': '0000000000000010', 'LCL': '0000000000000001'}


def num_to_bin16(num):
	if num < 0:
		num = 2**16+num
	base = bin(num)[2:]
	padding_size = 16 - len(base)
	return '0' * padding_size + base
	

def num_to_bin(num, wordsize):
    if num < 0:
        num = 2**wordsize+num
    base = bin(num)[2:]
    padding_size = wordsize - len(base)
    return '0' * padding_size + base


def readfile(filename):
	with open(filename) as f:
		return [x.strip() for x in f.readlines()]


def lit(art):
	return "{" +art+ "}"


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def clear_whitespace(lines):
	return [re.sub("\s+", "", line) for line in [re.sub("//.+", "", line) for line in lines] if line != ""]


def is_label(code_line):
	if re.search("^\(.+\)$", code_line):
		return True 
	return False


def parse(asm_filename):
	lines = readfile(asm_filename)
	lines_of_code = clear_whitespace(lines)
	add_labels(lines_of_code)
	lines_of_code = clear_labels(lines_of_code)
	for line in lines_of_code:
		if read_opcode(line) == "A_instruction":
			print read_A_instruction(line)
		elif read_opcode(line) == "C_instruction":
			print read_C_instruction(line)


def clear_brackets(label):
	return re.sub("[()]", "", label)


def add_labels(lines_of_code):
	labels_marked = int()
	for i, line in enumerate(lines_of_code):
		if is_label(line):
			symbols_table[clear_brackets(line)] = num_to_bin16(i-labels_marked)
			labels_marked += 1


def clear_labels(lines_of_code):
	return [line for line in lines_of_code if not is_label(line)]


def read_opcode(line_of_code):
	if line_of_code[0] == "@":
		return "A_instruction"
	else:
		return "C_instruction"


def read_A_instruction(A_instruction):
	global next_available_register
	val = A_instruction[1:]
	if all([c.isdigit() for c in val]):
		return num_to_bin16(int(val))
	else:
		if val in symbols_table:
			return symbols_table[val]
		else:
			symbols_table[val] = num_to_bin16(next_available_register)
			next_available_register += 1
			return symbols_table[val]


def read_C_instruction(C_instruction):
	# dest=comp;jump 
	# dest or jump can be omitted
	dest = "null" if "=" not in C_instruction else C_instruction.split("=")[0] 
	jump =  "null" if ";" not in C_instruction else C_instruction.split(";")[-1]
	lexed = re.split("(=|;)", C_instruction)
	comp = [cmd for cmd in lexed if cmd not in [dest, jump, "=", ";"]][0]
	a_bit = "0" if comp in a_bit_off_comp_table else "1"
	return "111"+a_bit+"".join([comp_table[comp], dest_table[dest], jump_table[jump]])


if __name__=="__main__":
	try:
		parse(sys.argv[1])
	except Exception as e:
		print "USAGE: python assembler.py code.asm"
		print e
	quit()

	# parsed =  parse("add/Add.asm")
	parsed = parse("../04/fill/Fill.asm")
	quit()
	for line in parsed:
		if read_opcode(line) == "A_instruction":
			print read_A_instruction(line)
		elif read_opcode(line) == "C_instruction":
			print read_C_instruction(line)

	quit()
	add_labels(parsed)
	print symbols_table["OUTPUT_FIRST"]
	quit()
	symbols = {} 
	for i in range(0, 16):
		symbols["R"+str(i)] = num_to_bin16(i)
	symbols["SCREEN"] = num_to_bin16(16384)
	symbols["KBD"] = num_to_bin16(24576)
	for i, sym in enumerate(['SP', 'LCL', 'ARG', 'THIS', 'THAT']):
		symbols[sym] = num_to_bin16(i)

	for k, v in symbols.iteritems():
		print k, v 
	print symbols
	quit()
	print len(comp_table), len(a_bit_off_comp_table), len(a_bit_on_comp_table)
	quit()
	# for k, v in comp_table.iteritems():
	# 	print k, v
	# quit()
	f = readfile('mnemo')
	d = {}
	a_bit_off_comp_table = {}
	a_bit_on_comp_table = {}
	for i in f:
		print len(d)
		if ";" in i:
			new_d = eval(lit(i.split(";")[0]))
			print "new d1", new_d
			new_d2 = {i.split(";")[1]: new_d[new_d.keys()[0]]}
			print "new d2", new_d2
			d = merge_two_dicts(d, new_d)
			a_bit_off_comp_table = merge_two_dicts(a_bit_off_comp_table, new_d)
			d = merge_two_dicts(d, new_d2)
			a_bit_on_comp_table = merge_two_dicts(a_bit_on_comp_table, new_d2)
			continue
		d = merge_two_dicts(d, eval(lit(i)))
		a_bit_off_comp_table = merge_two_dicts(a_bit_off_comp_table, eval(lit(i)))

	print d
	print "a bit off:"
	print a_bit_off_comp_table
	print "a bit on"
	print a_bit_on_comp_table
	print f
	A_instruction = '@21'
	print a_instruction_read(A_instruction)
	print 
	for i in range(7, -9, -1):
	    print num_to_bin(i, 4)

# for i in range(7, -9, -1):
# 	print num_to_bin16(i)
# print len(num_to_bin16(21