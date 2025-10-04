

def parse_generator(string: str):
	cmds = []
	quotes = []
	current = ""
	q_string = ""
	inquote = False
	for cha in string:
		if not inquote and cha == " ":
			if current:
				cmds.append(current)
				quotes.append(q_string)
			q_string = ""
			current = ""
			continue
		if cha == "\"":
			inquote ^= True

		current += cha

		if inquote and cha != "\"":
			q_string += cha

	if current:
		cmds.append(current)
		quotes.append(q_string)

	return cmds, quotes, inquote