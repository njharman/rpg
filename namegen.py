#!/usr/bin/env python

'''Context-free grammar random name generator

Jeremy Thurgood <jerith@is.und.ac.za>
Highly experimental at present, but sort of working
'''

import random
import re

# This should be done using gettext for i18n, but I can't be bothered to figure
# out how to do it properly, so I'm using replacement strings for now.
stringUndefinedNonTerminal = "Undefined non-terminal \"%(undefinedNonTerminal)s\" in rule \"%(rule)s\"."

# Test grammar -- will be read from a file when I decide how to do it properly
# with minimum effort (for the user and the code)
orkGrammar = {
    "name": ["<nameStart><nameMiddle0to3><nameEnd>"],
    "nameMiddle0to3": ["", "<nameMiddle>", "<nameMiddle><nameMiddle>", "<nameMiddle><nameMiddle><nameMiddle>"],
    "nameStart": ["<nsCons><nmVowel>", "<nsCons><nmVowel>", "<nsCons><nmVowel>", "<nsVowel>"],
    "nameMiddle": ["<nmCons><nmVowel>"],
    "nameEnd": ["<neCons><neVowel>", "<neCons>", "<neCons>"],
    "nsCons": ["D", "G", "K", "T", "Gr"],
    "nsVowel": ["E", "U"],
    "nmCons": ["d", "g", "k", "t", "r", "s", "z", "kt", "rs", "gr"],
    "nmVowel": ["a", "e", "i", "o", "u"],
    "neCons": ["r", "s", "z"],
    "neVowel": ["a", "u"]
    }

fooGrammar = {
    "name": ["<nameStart><nameMiddle0to2><nameEnd>"],
    "nameMiddle0to2": ["", "<nameMiddle>", "<nameMiddle><nameMiddle>"],
    "nameStart": ["<nsCons><nmVowel>", "<nsCons><nmVowel>", "<nsCons><nmVowel>", "<nsVowel>"],
    "nameMiddle": ["<nmCons><nmVowel>"],
    "nameEnd": ["<neCons><neVowel>", "<neCons>", "<neCons>"],
    "nsCons": ["J", "M", "P", "N", "Y", "D", "F"],
    "nmCons": ["l", "m", "lm", "th", "r", "s", "ss", "p", "f", "mb", "b", "lb", "d", "lf"],
    "neCons": ["r", "n", "m", "s", "y", "l", "th", "b", "lb", "f", "lf"],
    "nsVowel": ["A", "Au", "Ei"],
    "nmVowel": ["a", "e", "i", "o", "u", "au", "oa", "ei"],
    "neVowel": ["e", "i", "a", "au"]
    }

# Regular expression to catch non-terminals, used frequently, so global
reNonTerminal = re.compile(r"<(\w+)>")

# checkTypes() is only useful while testing with internally specified
# grammars.
# Once we're parsing an external file it becomes unnecessary since we generate
# the data types ourselves instead of asking a human to do it.  As such, error
# strings are hardcoded.  Anyone who sees them would be messing around in here
# anyway.


def checkTypes(nameGrammar):
    """Check given grammar object for correct datatypes.

    This function is only really necessary while the grammar's still being
    specified in here.  It will likely disappear when we parse the grammar from a
    data file.
    """
    if not isinstance(nameGrammar, dict):
        return "Grammar data is not a dictionary!"
    for rule, rhs in nameGrammar.items():
        if not isinstance(rhs, list):
            return "Rule \"%s\" is not a list!" % rule
        for option in rhs:
            if not isinstance(option, str):
                return "Rule \"%s\" does not contain only strings!" % rule

# Grammar verification stuff follows.  We can probably make this throw
# warnings
# and correct problems, but that's a job for another day.  Incorrect grammars
# probably won't provide useful output anyway.  If this stuff gets big enough
# it may be pushed into its own module.


def checkUndefinedNonTerminals(nameGrammar):
    """Check given grammar for undefined non-terminals.

    An undefined non-terminal is a non-terminal symbol used in a symbol
    definition that has no definition of its own and cannot therefore be
    expanded.  Undefined non-terminals can lead to ugly error messages
    instead of beautifully generated names.
    """
    for rule, rhs in nameGrammar.items():
        for option in rhs:
            tempStr = option
            matchNonTerminal = reNonTerminal.search(tempStr)
            while matchNonTerminal:
                if matchNonTerminal.group(1) not in nameGrammar:
                    return {"undefinedNonTerminal":
                            matchNonTerminal.group(1), "rule": rule}
                tempStr = reNonTerminal.sub("", tempStr, 1)
                matchNonTerminal = reNonTerminal.search(tempStr)


def checkUnproductiveNonTerminals(nameGrammar):
    """Check grammar for possibly unproductive non-terminals.

    An unproductive non-terminal is a non-terminal symbol that cannot be
    converted to a terminal symbol in the given grammar.  A good example of this
    is a non-terminal symbol that includes itself in its definition.

    This function is currently very basic and should be extended (rewritten?) to
    allow warnings for _possible_ unproductive non-terminals and errors for
    _definite_ unproductive non-terminals.  Volunteers?

    XXX: INCOMPLETE
    """
    def recurse(a):
        if a == 5:
            return a
        return recurse(a + 1)

    grammarUnchecked = dict([(rule, "".join(rhs))
                            for (rule, rhs) in nameGrammar.items()])
    grammarProductive = []
    finished = False
    while not finished:
        print "grammarProductive:"
        print grammarProductive
        print "grammarUnchecked:"
        print grammarUnchecked
        print
        finished = True
        for rule, rhs in grammarUnchecked.items():
            matchNonTerminal = reNonTerminal.search(rhs)
            while matchNonTerminal:
                matchString = matchNonTerminal.group(1)
                if matchString not in grammarProductive:
                    break
                rhs = rhs.replace("<" + matchString + ">", "")
                finished = False
                matchNonTerminal = reNonTerminal.search(rhs)
            if not matchNonTerminal:
                grammarProductive.append(rule)
                del grammarUnchecked[rule]
                finished = False
                continue
            grammarUnchecked[rule] = rhs

# More grammar checking functions to come:
#   Unused non-terminals
# Loop detection would be nice, but currently a little impractical.


def checkUnusedNonTerminals(nameGrammar):
    """Check grammar for non-terminals that can never be reached.

    While unused non-terminals are irrelevant in the generation of sentences,
    their presence usually implies an error in the grammar.

    XXX: INCOMPLETE
    """
    pass


def verifyGrammar(nameGrammar):
    '''verifyGrammar() uses the above functions to verify the correctness of a
    grammar.  This isn't perfect, but it should catch the most common problems.
    '''
    error = checkTypes(nameGrammar)
    if error:
        return error
    error = checkUndefinedNonTerminals(nameGrammar)
    if error:
        return stringUndefinedNonTerminal % error
    if "name" not in nameGrammar:
        return "Rule \"name\" not present!"


def nameGen(nameGrammar):
    nameStr = random.choice(nameGrammar["name"])
    matchNonTerminal = reNonTerminal.search(nameStr)
    while matchNonTerminal:
        subStr = random.choice(nameGrammar[matchNonTerminal.group(1)])
        nameStr = reNonTerminal.sub(subStr, nameStr, 1)
        matchNonTerminal = reNonTerminal.search(nameStr)
    return nameStr

# Main body
# checkUnproductiveNonTerminals(fooGrammar)
#errorStr = verifyGrammar(fooGrammar)
# if errorStr:
#    sys.exit(errorStr)
# print nameGen(fooGrammar)

for i in range(10):
    print nameGen(fooGrammar)
