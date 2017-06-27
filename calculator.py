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
	token_pattern = re.compile("\d+|\n|\+|\-|\/|\*|\(|\)")
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
		if re.compile("\*").match(match.group()):
			tokens.append(["MULTIPLY"])
			input_position += len(match.group())
		if re.compile("\/").match(match.group()):
			tokens.append(["DIVIDE"])
			input_position += len(match.group())
		if re.compile("\(").match(match.group()):
			tokens.append(["LEFTPAREN"])
			input_position += len(match.group())
		if re.compile("\)").match(match.group()):
			tokens.append(["RIGHTPAREN"])
			input_position += len(match.group())
		if re.compile("\n").match(match.group()):
			tokens.append(match.group())
			input_position += len(match.group())
	if not len(user_input) == input_position:
		tokens.append(["INVALID CHARACTER", user_input[input_position:len(user_input)], input_position])
	return tokens

# Make parse tree.
def parse(tokens):
	result, tokens = parse_calculation(tokens);
	if len(tokens) != 0:
		return "SYNTAX ERROR. Remaining invalid character at " + str(tokens[0][2]) + ": \"" + tokens[0][1] + "\""
	return result

def parse_calculation(tokens):
	parsetree = []
	tokens_parsed = 0
	result, tokens = parse_term(tokens)
	while len(tokens) > 0:
		if tokens[0][0] == "PLUS":
			tokens.pop(0)
			plus, tokens = parse_term(tokens)
			result += plus
		elif tokens[0][0] == "MINUS":
			tokens.pop(0)
			minus, tokens = parse_term(tokens)
			result -= minus
		else:
			break
	return result, tokens

def parse_term(tokens):
	result, tokens = parse_factor(tokens)
	while len(tokens) > 0:
		if tokens[0][0] == "MULTIPLY":
			tokens.pop(0)
			multiply, tokens = parse_factor(tokens)
			result *= multiply
		elif tokens[0][0] == "DIVIDE":
			tokens.pop(0)
			divide, tokens = parse_factor(tokens)
			result /= divide
		else:
			break
	return result, tokens

def parse_factor(tokens):
	if len(tokens) == 0:
		print("SYNTAX ERROR: EXPECTED FACTOR, GOT NULL")
		sys.exit()
	elif tokens[0][0] == "NUMBER":
		result = int(tokens.pop(0)[1])
	elif tokens[0][0] == "LEFTPAREN":
		tokens.pop(0)
		result, tokens = parse_calculation(tokens)
		if not tokens[0][0] == "RIGHTPAREN":
			print("SYNTAX ERROR: EXPECTED RIGHT PARENTHESES, GOT " + tokens[0][0])
		else:
			tokens.pop(0)
	else:
		print("SYNTAX ERROR: EXPECTED FACTOR, GOT: " + tokens[0][0])
	return result, tokens

if __name__ == "__main__":
	main()
