import nltk, re, pprint, string
from nltk.corpus import stopwords


lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  #Nouns adjectives, terminated with nouns

    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  #Above connected with in/of/etc.
"""

def chunk(sentence):
    #TODO: Come up with some interesting grammars for noun
    #phrase chunking.
    #grammar = 'NP: {<DT>?<JJ.*>*<NN.*>+}'
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


def leaves(tree):
    """Find NP leaf nodes in chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.node == 'NP'):
        yield subtree.leaves()


def normalize(word):
    """Normalize words to lowercase and stem and lammatize."""
    word = word.lower()
    word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word


def acceptable(word):
    """Check that the word is ling enough and not a stopword."""
    return bool(2 <= len(word) <= 40 and word.lower() not in stopword)


def get_terms(tree):
    for leaf in leaves(tree):
        term = [normalize(w) for w,t in leaf if acceptable(w)]
        yield term


if __name__ == '__main__':
    f = open('/home/noel/school/sustainable_societies/papers/benchmarking_approaches_and_methods_in_the_field_of_urban_waste_management.txt').read()

    for sentence in ie_preprocess(f):
        chunk(sentence)

