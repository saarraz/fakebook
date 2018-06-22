# -*- coding: utf-8 -*-
from random import *

import os

import model
from bots.post_bot import PostBot


class bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

formatPath = os.path.join(os.path.dirname(__file__), 'formats.txt')
rootPictures = os.path.join(os.path.dirname(__file__), 'images', 'articles') + os.path.sep
formats = []

wordPaths ={
    'names_female':  os.path.join(os.path.dirname(__file__), 'Texts', 'names_female.txt'),
    'names_male'   : os.path.join(os.path.dirname(__file__), 'Texts', 'names_male.txt'),
    'places'       : os.path.join(os.path.dirname(__file__), 'Texts', 'places.txt'),
    'verbs'        : os.path.join(os.path.dirname(__file__), 'Texts', 'verbs.txt')
}

formatTable = {
    'names_male'    : '_NM_',
    'names_female'  : '_NF_',
    'places'        : '_P_',
    'verbs'         : '_V_'
}

characterChangeTable = {

}

genericStuff = {
    '_N_' : ['_NF_', '_NM_']
}

stuffWithSubjects = ['names_female', 'names_male']


headlineMark = '_H_'
wordLists = {}
seperatorMark = '--'



def getNumberOfFilesInDir(p):
    return len(os.listdir(p))

def replaceWordInString(str, wordToReplace, wordWillReplace):

    wordLoc = str.find(wordToReplace)

    if wordLoc == -1: # We dont have anymore words to replace
        return -1

    newStr = str[:wordLoc] + wordWillReplace + str[wordLoc + len(wordToReplace):]
    return newStr

def pickRandomItem(lis):
    return lis[randrange(0, len(lis))]

def extractFile(filePath):

    # Returnign a table assigning each sentence to the character it refers to

    with open(filePath, 'rb') as f:
        contentFile = f.readlines()

    # Stripping the lines from any bad stuff and making hebrew possible !
    content = [x.decode('utf-8').split(seperatorMark)[0].strip() for x in contentFile]
    contentToCharacter = [x.decode('utf-8').strip() for x in contentFile]

    # Checking if we have a character change and if so moving it to the table
    for i in contentToCharacter:
        splitted = [x.strip() for x in i.split(seperatorMark)]
        if len(splitted) == 2:
            # We have a character change
            sentence, character = splitted
        else:
            # We dont have a character change
            sentence = splitted[0]
            character = 'default'

        characterChangeTable[sentence] = character


    return content

# Extracting the formats from the file
formats = extractFile(formatPath)

# Extracting the words from the files
for key in wordPaths:
    wordLists[key] = extractFile(wordPaths[key])

def getRandomGossip():
    # DESCRIPTION: Returns a tuple if there is a subtitle and one var if not
    currentFormat = pickRandomItem(formats)
    sentence = currentFormat
    character = 'default'

    # Turning the generic format into a constent format
    for key in genericStuff:
        toReplace = key
        toPut = pickRandomItem(genericStuff[key])

        changedSentence = replaceWordInString(sentence, toReplace, toPut)

        while changedSentence != -1:
            sentence = changedSentence
            toPut = pickRandomItem(genericStuff[key])
            changedSentence = replaceWordInString(sentence, toReplace, toPut)

    for key in formatTable:
        # Going over each format element and replacing it
        puttedList = []
        toPut = pickRandomItem(wordLists[key])
        toReplace = formatTable[key]

        changedSentence = replaceWordInString(sentence, toReplace, toPut)
        puttedList.append(toPut)

        while changedSentence != -1:

            if character == 'default': character = characterChangeTable[toPut]

            while True: # I know its bad programming - we are choosing a toPut we havent used yet
                toPut = pickRandomItem(wordLists[key])
                if puttedList.count(toPut) == 0: break # If our toPut is not used

            # We have our toPut !!
            puttedList.append(toPut)

            sentence = changedSentence
            changedSentence = replaceWordInString(sentence, toReplace, toPut)

    character = character.lower()
    character = 'default'
    imagePath = rootPictures + character + '\\'

    numOfFiles = getNumberOfFilesInDir(imagePath)

    if os.path.isfile(imagePath + character + str(randrange(0, numOfFiles) + 1) + '.jpg'):
        imagePath += character + str(randrange(0, numOfFiles) + 1) + '.jpg'
    else:
        imagePath += character + str(randrange(0, numOfFiles) + 1) + '.png'

    intro = choice([
        'שערוריה',
        'חשיפה',
        'חוצפה',
        'צפו',
        'תדהמה',
        'לא להאמין',
        'מזעזע',
        'דיווח',
        'צה"ל',
        'ארה"ב',
        'אחרי עשור',
        'סוף סוף',
        'פלילי',
        'היסטוריה',
        'הרבנות',
        'מבזק',
        'טראמפ',
        'מרקל',
        'נתניהו',
        'ליברמן',
        'בנט',
        'חשד',
        'נקבע',
        'מחקר חדש קובע'
    ])

    sentence = '{}: {}'.format(intro, sentence)

    str(randrange(0, 4)) + '.jpg'
    return sentence.split(headlineMark), os.path.join(rootPictures, imagePath)


def replaceWordInString(str, wordToReplace, wordWillReplace):

    wordLoc = str.find(wordToReplace)

    if wordLoc == -1: # We dont have anymore words to replace
        return -1

    newStr = str[:wordLoc] + wordWillReplace + str[wordLoc + len(wordToReplace):]
    return newStr

def pickRandomItem(lis):
    return lis[randrange(0, len(lis))]

def extractFile(filePath):

    # Returnign a table assigning each sentence to the character it refers to

    with open(filePath, 'rb') as f:
        content = f.readlines()
        # Stripping the lines from any bad stuff and making hebrew possible !
    content = [x.decode('utf-8').split(seperatorMark)[0].strip() for x in content]

    '''
    contentTable = {}

    for i in content:
        splitted = i.split(seperatorMark)

        # In case the code is not splitable
        if len(splitted) == 1:
            sentence = splitted[0]
            character = ' '
        else:
            sentence, character = splitted

        sentence = sentence.decode('utf-8')
        contentTable[sentence] = character
    '''

    return content

# Extracting the formats from the file
formats = extractFile(formatPath)

# Extracting the words from the files
for key in wordPaths:
    wordLists[key] = extractFile(wordPaths[key])

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')


class HebrewFakeNewsBot(PostBot):

    def __init__(self):
        self.sources = [
            model.Page('mako', model.Image(os.path.join(IMAGE_DIR, 'mako.png'))),
            model.Page('Haaretz הארץ', model.Image(os.path.join(IMAGE_DIR, 'haaretz.png'))),
            model.Page('חדשות 10', model.Image(os.path.join(IMAGE_DIR, '10.png'))),
            model.Page('וואלה! תרבות ובידור', model.Image(os.path.join(IMAGE_DIR, 'walla.png'))),
            model.Page('ynet', model.Image(os.path.join(IMAGE_DIR, 'ynet.jpg')))
        ]

    def generate(self, user, date):
        (a, b), c = getRandomGossip()
        news_outlet = choice(self.sources)
        post = model.Post(date, a,
                          model.Image(c),
                          news_outlet, None)
        comment = model.Comment(b, user, post)
        post.comments.append(comment)
        return post


if __name__ == '__main__':
    gossip = getRandomGossip()

    toPrint = bcolors.BOLD + gossip[0] + bcolors.ENDC + '\n'
    if len(gossip) >  1: toPrint += gossip[1] # Adding subtitle if needed
    print(toPrint)
