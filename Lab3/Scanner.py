import re
from SymbolTable import SymbolTable


digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
nonZeroDigits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def check_boolean(givenInput):
    if givenInput == "0" or givenInput == "1":
        return True
    return False


def __check_number(givenInput):
    if givenInput == "":
        return False
    if givenInput[0] not in nonZeroDigits:
        return False
    for character in givenInput[1:]:
        if character not in digits:
            return False
    return True


def check_integer(givenInput):
    if givenInput == "":
        return False
    if givenInput == "0":
        return True
    elif givenInput[0] == '+' or givenInput[0] == '-':
        if __check_number(givenInput[1:]):
            return True
    elif __check_number(givenInput):
        return True
    return False


def __check_fractionalPart(givenInput):
    if givenInput == "":
        return False
    for character in givenInput:
        if character not in digits:
            return False
    return True


def check_real(givenInput):
    if givenInput == "":
        return False
    inputElements = givenInput.split('.')
    if len(inputElements) != 2:
        return False
    integerPart = inputElements[0]
    fractionalPart = inputElements[1]
    if check_integer(integerPart) and __check_fractionalPart(fractionalPart):
        return True
    return False


def check_character(givenInput):
    if len(givenInput) != 3:
        return False
    elif givenInput[0] == '\'' and (givenInput[1].isalpha() or givenInput[1] in digits) and givenInput[2] == '\'':
        return True
    return False


def __check_base_string(givenInput):
    for character in givenInput:
        if not (character.isalpha() or character in digits):
            return False
    return True


def check_string(givenInput):
    if len(givenInput) < 2:
        return False
    elif len(givenInput) == 2 and givenInput[0] == '\"' and givenInput[1] == '\"':
        return True
    elif givenInput[0] == '\"' and __check_base_string(givenInput[1:-1]) and givenInput[-1] == '\"':
        return True
    return False


def __check_base_name(givenInput):
    for character in givenInput:
        if not (character.islower()):
            return False
    return True


def check_name(givenInput):
    if len(givenInput) < 4:
        return False
    elif givenInput[0] == '\"' and givenInput[1].isupper() and \
            __check_base_name(givenInput[2:-1]) and givenInput[-1] == '\"':
        return True
    return False


def check_special_symbol(givenInput, symbolsList):
    if givenInput in symbolsList:
        return True
    return False


def check_identifier(givenInput):
    if len(givenInput) < 1:
        return False
    if not givenInput[0].isalpha():
        return False
    for character in givenInput:
        if not (character.isalpha() or character in digits):
            return False
    return True


def check_identifier_regex(givenInput):
    if re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', givenInput):
        return True
    return False


def check_constant(givenInput):
    if check_boolean(givenInput) or check_integer(givenInput) or check_real(givenInput) or \
            check_character(givenInput) or check_string(givenInput) or check_name(givenInput):
        return True
    return False


def scan(programFileName, tokenFileName):
    programFile = open(programFileName, "r")
    tokenFile = open(tokenFileName, "r")
    pifFile = open("PIF.out", "w")
    stFile = open("ST.out", "w")

    pif = []
    symbolTableIdentifiers = SymbolTable()
    symbolTableConstants = SymbolTable()

    lexicallyCorrect = True
    lexicalErrors = set()

    # put all special symbols in a list
    specialSymbols = []

    operators = tokenFile.readline().split()
    for operator in operators:
        specialSymbols.append(operator)

    separators = tokenFile.readline().split()
    for separator in separators:
        specialSymbols.append(separator)

    reservedWords = tokenFile.readline().split()
    for reservedWord in reservedWords:
        specialSymbols.append(reservedWord)

    # print(specialSymbols)
    # print(operators)
    # print(separators)
    # print(reservedWords)

    # put all tokens in a list
    tokens = []
    lineNumber = 0
    # a variable used to skip next character
    skipNextCharacter = False
    for line in programFile:
        lineNumber += 1
        lineElements = line.split()
        for lineElement in lineElements:
            token = ""
            for characterIndex in range(len(lineElement)):
                if skipNextCharacter:
                    skipNextCharacter = False
                    continue

                character = lineElement[characterIndex]

                if character in operators:
                    if characterIndex != len(lineElement) - 1:
                        if character == '+' or character == '-':
                            if token == "" and len(tokens) != 0 and tokens[-1] == ")":
                                tokens.append((character, lineNumber))
                            elif len(token) != 0 and (check_identifier(token) or check_constant(token)):
                                tokens.append((token, lineNumber))
                                tokens.append((character, lineNumber))
                                token = ""
                            else:
                                token += character
                                continue

                        if character == '<' and \
                                (lineElement[characterIndex + 1] == '=' or lineElement[characterIndex + 1] == '>'):
                            if token != "":
                                tokens.append((token, lineNumber))
                            currentOperator = character + lineElement[characterIndex + 1]
                            skipNextCharacter = True
                            tokens.append((currentOperator, lineNumber))
                            token = ""
                        elif character == '=' and lineElement[characterIndex + 1] == '=':
                            if token != "":
                                tokens.append((token, lineNumber))
                            currentOperator = character + lineElement[characterIndex + 1]
                            skipNextCharacter = True
                            tokens.append((currentOperator, lineNumber))
                            token = ""
                        elif character == '>' and lineElement[characterIndex + 1] == '=':
                            if token != "":
                                tokens.append((token, lineNumber))
                            currentOperator = character + lineElement[characterIndex + 1]
                            skipNextCharacter = True
                            tokens.append((currentOperator, lineNumber))
                            token = ""
                        else:
                            if token != "":
                                tokens.append((token, lineNumber))
                            tokens.append((character, lineNumber))
                            token = ""
                    else:
                        if token != "":
                            tokens.append((token, lineNumber))
                        tokens.append((character, lineNumber))
                        token = ""

                elif character in separators:
                    if token != "":
                        tokens.append((token, lineNumber))
                    tokens.append((character, lineNumber))
                    token = ""

                else:
                    token += character

            if token != "":
                tokens.append((token, lineNumber))

    # Check if code is lexically correct or not + update PIF, ST
    for token in tokens:
        # print(token)
        if check_special_symbol(token[0], specialSymbols):
            position = -1
            pif.append((token[0], position))
        elif check_identifier(token[0]):
            position = symbolTableIdentifiers.add(token[0])
            if position == (-1, -1):
                position = symbolTableIdentifiers.search(token[0])
            pif.append(("id", position))
        elif check_constant(token[0]):
            position = symbolTableConstants.add(token[0])
            if position == (-1, -1):
                position = symbolTableConstants.search(token[0])
            pif.append(("const", position))
        else:
            lexicallyCorrect = False
            lexicalErrors.add((token[0], token[1]))

    if lexicallyCorrect:
        stFile.write("ST (Only Identifiers)" + "\n")
        stFile.write("Position --> Symbol" + "\n\n")
        stFile.write(symbolTableIdentifiers.displayText())
        stFile.write("\n" + "-----" + "\n\n")

        stFile.write("ST (Only Constants)" + "\n")
        stFile.write("Position --> Symbol" + "\n\n")
        stFile.write(symbolTableConstants.displayText())

        pifFile.write("Token --> ST_Position" + "\n\n")
        for pifElement in pif:
            pifFile.write(str(pifElement[0]) + " --> " + str(pifElement[1]) + "\n")

        print("lexically correct")
    else:
        for lexicalError in lexicalErrors:
            print("lexical error -> token: " + str(lexicalError[0]) + " on line: " + str(lexicalError[1]))

    programFile.close()
    tokenFile.close()
    pifFile.close()
    stFile.close()


scan("p2.txt", "Token.in")
