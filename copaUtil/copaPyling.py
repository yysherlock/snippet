import nltk
from nltk.corpus import wordnet
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()

def getCorrectLemmatizerWord(sentence, errindex):
    correctSenList = lemmatizer(sentence);
    return correctSenList[errindex];

def lemmatizer(sentence):
        result = "";
        tokens = word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        for item in tagged:
                postag = get_wordnet_pos(item[1])
                if postag=='':
                        word = lmtzr.lemmatize(item[0])
                else:
                        word = lmtzr.lemmatize(item[0],postag)
                result += word;
                result += " ";
                
        return result.lower()

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

if __name__=="__main__":
        print lemmatizer('The cook stirred the ingredients in the bowl .')
	print lemmatizer('The ingredients blended together .')
	print lemmatizer("The woman tolerated the woman friend 's difficult behavior . ")
	print lemmatizer('He felt content.')
