from converter import VectorConverter

if __name__ == '__main__':

    converter = VectorConverter('/home/c/gema/word2vec/word2vector-py/data/vectors.gigaword.bin')
    
    print 'converting word sentences to vector sentences...'
    metadata = converter.convert_from_file('/home/c/gema/word2vec/word2vector-py/data/output')
    
    print 'saving vector metadata to a file...'
    converter.save_metadata_to_file(metadata, 'output')



