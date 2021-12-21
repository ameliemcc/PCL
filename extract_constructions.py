import spacy, sys, re
from spacy.matcher import DependencyMatcher
from spacy.tokens import DocBin

nlp = spacy.load('en_core_web_sm')
matcher = DependencyMatcher(nlp.vocab)

# files = (sys.argv[1], sys.argv[2], sys.argv[3])



def dependency_match(file, dependency):    
    re_groups = re.search('^(\w+)_(\w+)_(\d+)_', file)
    word = re_groups.group(1)
    type = re_groups.group(2)
    year = re_groups.group(3)
    dep = dependency[0]['RIGHT_ATTRS']['DEP']
    matcher.add(f'{word}_{dep}', [dependency])
    with open(f'{word}_profile_{dependency}_{type}_{year}_data.tsv', 'w') as f:
        docbin = DocBin().from_disk(f'C:\\Users\\mhess\\Documents\\UZH\\PCL\\PCL_PROJECT\\part_1\\{file}')
        doc_in_docbin = docbin.get_docs(nlp.vocab)
        for doc in doc_in_docbin:
            matches = matcher(doc)
            if matches != []:
                f.write(doc.text)
    matcher.remove(f'{word}_{dependency}')
        
def extraction_automation():
    prep = [ {'RIGHT_ID': 'off_prep', 'RIGHT_ATTRS': {'DEP': 'prep'}}]
    prt = [ {'RIGHT_ID': 'off_prt', 'RIGHT_ATTRS': {'DEP': 'prt'}}]
    amod = [ {'RIGHT_ID': 'ref_amod', 'RIGHT_ATTRS': {'DEP': 'amod'}}]
    nmod = [ {'RIGHT_ID': 'ref_nmod', 'RIGHT_ATTRS': {'DEP': 'nmod'}}]
    aux = [ {'RIGHT_ID': 'be_aux', 'RIGHT_ATTRS': {'DEP': 'aux'}}]
    auxpass = [ {'RIGHT_ID': 'be_auxpass', 'RIGHT_ATTRS': {'DEP': 'auxpass'}}]
    auxpass = [ {'RIGHT_ID': 'be_auxpass', 'RIGHT_ATTRS': {'DEP': 'auxpass'}}]
    dep_pattern = [ {'RIGHT_ID': 'verb', 'RIGHT_ATTRS': {'IS_ALPHA': True}},
                {'LEFT_ID': 'verb', 'REL_OP': '>', 'RIGHT_ID': 'subject', 'RIGHT_ATTRS':{'DEP': 'nsubj'}}
                ]
    # dependencies = [{'prep':prep, 'prt':prt},{'amod': amod, 'nmod':nmod}, {'aux':aux, 'auxpass':auxpass}]
    files = (
        (('off_news_2014_corpus.spacy', 'off_news_2020_corpus.spacy'),(prep, prt))
        # ,(('refugee_news_2007_corpus.spacy', 'file2'), (amod, nmod))
        # ,(('was_news_20xx_corpus.spacy', 'file2'),(aux, auxpass))
    )

    for wordtuple in files:
        for file in wordtuple[0]:
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