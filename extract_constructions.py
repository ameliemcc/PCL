import spacy, sys, re
from spacy.matcher import DependencyMatcher
from spacy.tokens import DocBin

nlp = spacy.load('en_core_web_sm')
matcher = DependencyMatcher(nlp.vocab)

# dep_pattern = [ {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'IS_ALPHA': True}},
#             {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS':{'DEP': 'nsubj'}}
#             ]

# files = (sys.argv[1], sys.argv[2], sys.argv[3])


def dependency_match(file, dependency):    
    re_groups = re.search(r'^(\w+)_(\w+)_(\d+)_', file)
    # wrong lemmas: keys
    # to be replaced by corresponding value
    fix_lemmas = {}
    try:
        word = re_groups.group(1)
        type = re_groups.group(2)
        year = re_groups.group(3)
    except AttributeError:
        pass

    dep = dependency[0]['RIGHT_ATTRS']['DEP']
    matcher.add(f'{word}_{dep}', [dependency])
    # opens the tsv-output file in write mode
    with open(f'{word}_profile_{dep}_{type}_{year}_data.tsv', 'w', encoding='utf-8') as f:
        # loads the parsed corpus (saved as a .spacy file)
        docbin = DocBin().from_disk(f'{file}')
        # assigns the parsed corpus to the established vocab
        doc_in_docbin = docbin.get_docs(nlp.vocab)
        # iterates through each doc (i.e. each sentence) in the loaded corpus
        for doc in doc_in_docbin:
            for matches in matcher(doc):
                print(matches)
                doc_id, match_id = matches
                # match_id.sort()
                
                f.write(f'{doc[match_id[0]].lemma_}\t{doc[match_id[1]].lemma_}\n')
    print(f'{file} / {dep}: S U C C E S S')
    matcher.remove(f'{word}_{dep}')
        
def extraction_automation():
    prep = [ {'RIGHT_ID': 'off_prep', 'RIGHT_ATTRS': {'DEP': 'prep'}},
            {'LEFT_ID': 'off_prep', 'REL_OP': '>', 'RIGHT_ID': 'prep_foot', 'RIGHT_ATTRS':{'IS_ALPHA': True}}]
    prt = [ {'RIGHT_ID': 'off_prt', 'RIGHT_ATTRS': {'DEP': 'prt'}},
            {'LEFT_ID': 'off_prt', 'REL_OP': '<', 'RIGHT_ID': 'prt_head', 'RIGHT_ATTRS':{'IS_ALPHA': True}}]

    amod = [ {'RIGHT_ID': 'ref_amod', 'RIGHT_ATTRS': {'DEP': 'amod'}},
            {'LEFT_ID': 'ref_amod', 'REL_OP': '<', 'RIGHT_ID': 'amod_head', 'RIGHT_ATTRS':{'IS_ALPHA': True}}]
    #nmod = [ {'RIGHT_ID': 'ref_nmod', 'RIGHT_ATTRS': {'DEP': 'nmod'}},
         #   {'LEFT_ID': 'ref_nmod', 'REL_OP': '<', 'RIGHT_ID': 'nmod_foot', 'RIGHT_ATTRS':{'IS_ALPHA': True}}]
    #pobj = [ {'RIGHT_ID': 'ref_nmod', 'RIGHT_ATTRS': {'DEP': 'pobj'}},
           # {'LEFT_ID': 'ref_nmod', 'REL_OP': '<<', 'RIGHT_ID': 'nmod_head', 'RIGHT_ATTRS':{'IS_ALPHA': True}}]

    pobj = [{'RIGHT_ID': 'ref_pobj', 'RIGHT_ATTRS': {'DEP': 'pobj'}},
            {'LEFT_ID': 'ref_pobj', 'REL_OP': '<<', 'RIGHT_ID': 'pobj_head',
             'RIGHT_ATTRS': {'TAG': {'IN': ['NN', 'NNP', 'NNS', 'NNPS']}}}]
    aux = [{'RIGHT_ID': 'be_aux', 'RIGHT_ATTRS': {'DEP': 'aux'}},
            {'LEFT_ID': 'be_aux', 'REL_OP': '<', 'RIGHT_ID': '', 'RIGHT_ATTRS':{'IS_ALPHA': True}}]
    auxpass = [{'RIGHT_ID': 'be_auxpass', 'RIGHT_ATTRS': {'DEP': 'auxpass'}},
            {'LEFT_ID': 'be_auxpass', 'REL_OP': '<', 'RIGHT_ID': '', 'RIGHT_ATTRS':{'IS_ALPHA': True}}]
    # dependencies = [{'prep':prep, 'prt':prt},{'amod': amod, 'nmod':nmod}, {'aux':aux, 'auxpass':auxpass}]
    files = (
        (('off_news_2014_corpus.spacy', 'off_news_2020_corpus.spacy'), (prep, prt)),
        (('refugee_news_2007_corpus.spacy', 'refugee_news_2013_corpus.spacy', 'refugee_news_2017_corpus.spacy'), (amod, pobj)),
        (('was_news_2020_corpus.spacy', 'was_web_2020_corpus.spacy'), (aux, auxpass))
    )

    for wordtuple in files:
        # print(wordtuple)
        # wordtuple =tuple(wordtuple)
        for file in wordtuple[0]:
            # print(file)
            for dependency in wordtuple[1]:
                # print(file,dependency)
                dependency_match(file, dependency)

    """tup = (
        (
            ('file1', 'file2'), ('dep1', 'dep2')
        )
        (
            ('file3', 'file4'), ('dep3', 'dep4')
        )
    )
    """


if __name__ == '__main__':
    extraction_automation()
