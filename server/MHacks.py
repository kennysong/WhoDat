space = 0;

def permutateNum(inputString):
		inputString.replace('', ' ')

		print(inputString);

		for i in range(65,100):
			print(inputString + str(i))
			print(inputString + "19" + str(i))

		for i in range(0, 10):
			print(inputString + str(i))	


def permutateReverse(inputString):
		space = inputString.find(' ')
		return inputString[space:-1]+ inputString[-1] + inputString[0:space]

def permutateInitials(inputString):
		space =  inputString.find(' ')
		return inputString[0] + inputString[space+1:-1] + inputString[-1]

		space=  inputString.find(' ')
		return inputString[0:space] + inputString[space+1]



