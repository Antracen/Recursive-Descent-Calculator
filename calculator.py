import sys
import re

def main():
	print("Enter calculation:")
	user_input = sys.stdin.read().rstrip("\r\n")
	tokens = tokenize(user_input)
	result = parse(tokens)
	print(result)

# Make input into tokens.
def tokenize(user_input):
	input_position = 0
	tokens = []
	token_pattern = re.compile("\d+|\n|\+|\-")
	token_matches = token_pattern.finditer(user_input)
	
	for match in token_matches:
		if not input_position == match.start():
			tokens.append(["INVALID CHARACTER", user_input[input_position:match.start()], input_position])
		if re.compile("\d+").match(match.group()):
			tokens.append(["NUMBER", match.group()])
			input_position += len(match.group())
		if re.compile("\+").match(match.group()):
			tokens.append(["PLUS"])
			input_position += len(match.group())
		if re.compile("\-").match(match.group()):
			tokens.append(["MINUS"])
			input_position += len(match.group())
		if re.compile("\n").match(match.group()):
			tokens.append(match.group())
			input_position += len(match.group())
	if not len(user_input) == input_position:
		tokens.append(["INVALID CHARACTER", user_input[input_position:len(user_input)], input_position])
	return tokens

# Make parse tree.
def parse(tokens):
	result = parse_calculation(tokens);
	return result

def parse_calculation(tokens):
	parsetree = []
	tokens_parsed = 0
	result, tokens = parse_number(tokens)
	while len(tokens) > 0:
		next = tokens.pop(0)
		if next[0] == "PLUS":
			plus, tokens = parse_number(tokens)
			result += plus
		elif next[0] == "MINUS":
			minus, tokens = parse_number(tokens)
			result -= minus
		else:
			result = "SYNTAX ERROR, EXPECTED PLUS OR MINUS, GOT \"" + next[0] + "\""
			break
	return result

def parse_number(tokens):
	if len(tokens) == 0:
		print("SYNTAX ERROR: EXPECTED NUMBER, GOT NULL")
		sys.exit()
	elif tokens[0][0] != "NUMBER":
		print("SYNTAX ERROR: EXPECTED NUMBER, GOT " + tokens[0][0])
		sys.exit()
	else:
		return int(tokens.pop(0)[1]), tokens

if __name__ == "__main__":
	main()
