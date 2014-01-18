
# helperFunction:  uses all the other functions
#permList is the final list or array of all possible permutations
def helperFunction(inputString):
 	permList = [];
 	permList.append(permutateReverse(inputString))
 	permList += permutateInitials(inputString)
 	permList += permutateNumbers(inputString)
 	permList += firstAndLastName(inputString)
 	permList += dots(inputString)

 	return permList 	
 	


# permutateNumbers: inserts #s 1-10 at the end
# Used to have 65-99 and 1965-1999, but not anymore
def permutateNumbers(inputString):
	numPermutationList = [];

	if(inputString.find(' ') != -1):
		space = inputString.find(' ')
		noSpaceName = inputString[0:space] + inputString[space+1:-1] + inputString[-1]
		for i in range(0, 10):
			numPermutationList.append(noSpaceName + str(i));x
	else:
		upperCase = [up for up in inputString if up.isupper()]
		space = inputString.find(upperCase[1])
		noSpaceName = inputString[0:space] + inputString[space+1:-1] + inputString[-1]
		for i in range(0, 10):
			numPermutationList.append(noSpaceName + str(i));
		for i in range(65, 100):
			numPermutationList.append(noSpaceName + str(i));
			numPermutationList.append(noSpaceName + '19' + str(i));


	return numPermutationList;


#permutateReverse: Switchis first and last name
def permutateReverse(inputString):
	if(inputString.find(' ') != -1):
		space = inputString.find(' ')
		return inputString[space+1:-1]+ inputString[-1] + inputString[0:space]
	else:
		upperCase = [up for up in inputString if up.isupper()]
		space = inputString.find(upperCase[1])
		return inputString[space+1:-1]+ inputString[-1] + inputString[0:space]
			

#permutateInitials: Gets first initial last name, and first name last initial
def permutateInitials(inputString):		
	if(inputString.find(' ') != -1):
		space = inputString.find(' ')
		initials = [inputString[0] + inputString[space+1:-1] + inputString[-1], inputString[0:space] + inputString[space+1]]
		return initials
		
	else:
		upperCase = [up for up in inputString if up.isupper()]
		space = inputString.find(upperCase[1])
		initials = [inputString[0] + inputString[space+1:-1] + inputString[-1], inputString[0:space] + inputString[space+1]]
		return initials


def firstAndLastName(inputString):
	firstAndLastNameList = []

	if(inputString.find(' ') != -1):
		space = inputString.find(' ')
		firstAndLastNameList.append(inputString[0:space])
		firstAndLastNameList.append(inputString[space+1:-1] + inputString[-1:])
	else:
		upperCase = [up for up in inputString if up.isupper()]
		space = inputString.find(upperCase[1])
		firstAndLastNameList.append(inputString[0:space])
		firstAndLastNameList.append(inputString[space:-1] + inputString[-1])

	return firstAndLastNameList

#dots: Adds dots. **NOT FINISHED**
def dots(inputString):
	dotsList = []

	if(inputString.find(' ')!= -1):
		space = inputString.find(' ')
		middleDot = inputString.replace(' ', '.')
		dotsList.append(middleDot)

	else:
		upperCase = [up for up in inputString if up.isupper()]
		space = inputString.find(upperCase[1])
		middleDot = inputSTring.replace(' ', '.')
		dotsList.append(middleDot)

	return dotsList
print(helperFunction("Paul Vorobyev"))