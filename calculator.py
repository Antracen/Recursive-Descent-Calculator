import sys
import re

def main():
	print("Enter calculation:")
	user_input = input()
	tokens = tokenize(user_input)
	parsetree = parse(tokens)
	print(parsetree)

# Make input into tokens.
def tokenize(user_input):
	input_position = 0
	tokens = []
	token_pattern = re.compile("\d+|\n")
	token_matches = token_pattern.finditer(user_input)
	
	for match in token_matches:
		if not input_position == match.start():
			tokens.append(["invalid", user_input[input_position:match.start()], input_position])
		if re.compile("\d+").match(match.group()):
			tokens.append(["DIGIT", match.group()])
			input_position += len(match.group())
		if re.compile("\n").match(match.group()):
			tokens.append(match.group())
			input_position += len(match.group())
	if not len(user_input) == input_position:
		tokens.append(["invalid", user_input[input_position:len(user_input)], input_position])
	return tokens

# Make parse tree.
def parse(tokens):
	parsetree = []
	for token in tokens:
		if token[0] == "DIGIT":
			parsetree.append(token)
		elif token[0] == "\n":
			parsetree = "Newline found in input, input must be one line"
			break
		else:
			parsetree = "Syntax error at column " + str(token[2]) + ": \"" + token[1] + "\""
			break
	return parsetree

if __name__ == "__main__":
	main()
