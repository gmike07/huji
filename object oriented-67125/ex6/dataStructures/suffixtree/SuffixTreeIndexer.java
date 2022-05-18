package dataStructures.suffixtree;

import dataStructures.Aindexer;
import dataStructures.ObjectWriter;
import processing.parsingRules.IparsingRule;
import processing.searchStrategies.SuffixTreeSearch;
import processing.textStructure.Block;
import processing.textStructure.Corpus;
import processing.textStructure.Entry;
import utils.Stopwords;
import utils.WrongMD5ChecksumException;
import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class SuffixTreeIndexer extends Aindexer<SuffixTreeSearch>  {
    /* the pattern to find words in the text */
    private static final Pattern pattern = Pattern.compile("(\\w+)\\s+");
    /* the dict to store all words by blocks */
    private Map<Block, GeneralizedSuffixTree> trees;
    /**
     * Basic constructor, sets origin Corpus and initializes backing hashmap
     * @param origin    the Corpus to be indexed by this DS.
     */
    public SuffixTreeIndexer(Corpus origin) {
        super(origin);
        this.dataStructType = IndexTypes.SUFFIX_TREE;
    }

    @Override
    /*
     * get the backing search interface.
     * @return  The search interface implementation used by this indexer.
     */
    public SuffixTreeSearch asSearchInterface() {
        return new SuffixTreeSearch(trees);
    }

    @Override
    /*
     * Index the Corpus internally using the parsing rules defined for this datastructure.
     */
    protected void indexCorpus() {
        trees = new HashMap<>();
        for (Entry entry : origin)
            for (Block block : entry)
                processBlock(block);
    }

    /**
     * @param block the block to process
     * adds all the words in the block to the data structure
     */
    private void processBlock(Block block){
        Matcher matcher = pattern.matcher(block.toString());
        while(matcher.find()) {
            String word = matcher.group(1);
            String noStopWord = Stopwords.removeStopWords(word);
            if (!noStopWord.equals("")) {
                if (!trees.containsKey(block))
                    trees.put(block, new GeneralizedSuffixTree());
                trees.get(block).put(noStopWord, matcher.start());
            }
        }
    }

    @Override
    @SuppressWarnings("unchecked")
    /*
     * Try to read a cached index file if one already exists.
     * @throws FileNotFoundException
     * @throws WrongMD5ChecksumException
     */
    protected void readIndexedFile() throws FileNotFoundException, WrongMD5ChecksumException {
        trees = (Map<Block, GeneralizedSuffixTree>) ObjectWriter.readIndexedFile(this);
    }

    @Override
    /*
     * Write the internal index into file.
     */
    protected void writeIndexFile() {
        ObjectWriter.writeIndexedFile(this, trees);
    }

    @Override
    /*
     * Extract the parsing rule used for indexing this data structure.
     * @return  an instance of a parser implementing IparsingRule
     */
    public IparsingRule getParseRule() {
        return this.origin.getParsingRule();
    }
}