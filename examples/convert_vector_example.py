from Converter import VectorConverter

if __name__ == '__main__':

    converter = VectorConverter('/home/c/gema/word2vec/word2vector-py/data/vectors.gigaword.bin')
    
    metadata = converter.convert_from_file('/home/c/gema/word2vec/word2vector-py/data/output')
    
    sentences, labels = metadata.get_metadata()
    
    print sentences.get_sentences()
    print labels.get_labels()

