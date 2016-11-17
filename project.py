import nltk, re, pprint, string
from nltk.corpus import stopwords


def chunk(sentence):
    #TODO: Come up with some interesting grammars for noun
    #phrase chunking.
    grammar = 'NP: {<DT>?<JJ.*>*<NN.*>+}'
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(sentence)
    #result.draw()  #This will draw the NP tree
    print(result)


def ie_preprocess(doc):
    """Generate sentence segments."""
    sentences = nltk.sent_tokenize(doc)
    sentences = [word for word in sentences if word not in stopwords.words('english')]
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]

    for sentence in sentences:
        yield sentence


if __name__ == '__main__':
    f = open('/home/noel/school/sustainable_societies/papers/benchmarking_approaches_and_methods_in_the_field_of_urban_waste_management.txt').read()

    for sentence in ie_preprocess(f):
        chunk(sentence)

