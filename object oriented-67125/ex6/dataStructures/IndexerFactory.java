package dataStructures;

import dataStructures.custom.CustomIndexer;
import dataStructures.suffixtree.SuffixTreeIndexer;
import dataStructures.dictionary.DictionaryIndexer;
import dataStructures.naive.NaiveIndexer;
import dataStructures.naive.NaiveIndexerRK;
import processing.textStructure.Corpus;

public class IndexerFactory {
    /**
     * @param indexer gets the indexer type
     * @param corpus gets the corpus to give the indexer
     * @return the indexer of the correct type with the corpus that was given
     */
    public static Aindexer getIndexer(Aindexer.IndexTypes indexer, Corpus corpus){
        switch (indexer){
            case NAIVE:
                return new NaiveIndexer(corpus);
            case NAIVE_RK:
                return new NaiveIndexerRK(corpus);
            case DICT:
                return new DictionaryIndexer(corpus);
            case SUFFIX_TREE:
                return new SuffixTreeIndexer(corpus);
            case CUSTOM:
                return new CustomIndexer(corpus);

            default:
                return null;
        }
    }
}
