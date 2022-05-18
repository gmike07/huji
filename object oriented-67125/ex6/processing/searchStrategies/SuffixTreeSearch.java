package processing.searchStrategies;

import dataStructures.suffixtree.GeneralizedSuffixTree;
import processing.textStructure.Block;
import processing.textStructure.WordResult;
import utils.Stopwords;

import java.util.*;

public class SuffixTreeSearch implements IsearchStrategy {
    /* the trees mapped by blocks */
    private Map<Block, GeneralizedSuffixTree> trees;

    /**
     * @param trees the trees to usse for searching
     */
    public SuffixTreeSearch(Map<Block, GeneralizedSuffixTree> trees){
        this.trees = trees;
    }


    @Override
    /*
     * The main abstract method - Search a quary string (could be multiple words) and return a result list.
     * @param query The query string to search for.
     * @return  A list of result objects
     */
    public List<? extends WordResult> search(String query) {
        Map<Block, Map<String, List<WordContainer>>> fittingWords = new HashMap<>();
        List<String> patterns = SearchHelper.filterByLambda(query, Stopwords::removeStopWords);
        findFittingWords(fittingWords, patterns);
        return SearchHelper.updateResults(fittingWords, patterns);
}

    /**
     * @param fittingWords contains the weird structure to use later
     * @param stemmedWords contains the query words to search
     * adds all the words to the fittingWords map to generate all options later, deletes blocks that don't
     *                     contain all the words in the query
     */
    private void findFittingWords(Map<Block, Map<String, List<WordContainer>>> fittingWords,
                                  List<String> stemmedWords) {
        LinkedList<Block> toDelete = new LinkedList<>();
        for (Block block : trees.keySet()) {
            for (String pattern : stemmedWords){
                Collection<Integer> startIndexes = trees.get(block).search(pattern);
                for (Integer startIndex : startIndexes)
                    SearchHelper.addToMap(fittingWords, block, pattern, startIndex);
            }
            //if doesn't contain all words, delete it
            if (!SearchHelper.ContainsAll(fittingWords.get(block), stemmedWords)){
                toDelete.add(block);
            }
        }
        for(Block block : toDelete)
            fittingWords.remove(block);
    }

}
