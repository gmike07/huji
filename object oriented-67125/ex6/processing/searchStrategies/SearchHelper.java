package processing.searchStrategies;

import processing.textStructure.Block;
import processing.textStructure.MultiWordResult;
import processing.textStructure.WordResult;

import java.util.*;
import java.util.function.Function;

class SearchHelper {

    /**
     * @param fittingWords a map
     * @return generates all valid combinations from the map and returns them
     */
    static List<? extends WordResult> updateResults(
            Map<Block, Map<String, List<WordContainer>>> fittingWords, List<String> stemmedWords) {
        List<WordResult> results = new LinkedList<>();
        for (Block block : fittingWords.keySet())
            generateAllOptions(fittingWords.get(block), block, new LinkedList<>(), new LinkedList<>(),
                    results, stemmedWords);
        return results;
    }

    /**
     * @param map gets the map
     * @param block gets the block to generate for
     * @param listString gets a list of strings
     * @param listLong gets a list of longs
     * @param results gets the results as a list
     * generates all valid combinations from the map and stores them in result
     */
    private static void generateAllOptions(Map<String, List<WordContainer>> map, Block block,
                                           List<String> listString, List<Long> listLong,
                                           List<WordResult> results, List<String> stemmedWords){

        if (listString.size() > map.keySet().size()) return;

        if (listString.size() == map.keySet().size()) {
            results.add(generateMultiWordResult(listString, listLong, block));
            return;
        }
        String pattern = stemmedWords.get(listString.size());
        for (WordContainer wordResult : map.get(pattern)){
            listString.add(wordResult.getWord());
            listLong.add(wordResult.getStartIndex());

            generateAllOptions(map, block, listString, listLong, results, stemmedWords);

            listString.remove(wordResult.getWord());
            listLong.remove(wordResult.getStartIndex());
        }
    }

    /**
     * @param listString gets a list of strings
     * @param listLong gets a list of the startIndexes of the words in the correct in the same order as the
     *                strings
     * @param block gets a block where the words were found in
     * @return a multiWordResult that represent those indexes, string and the block
     */
    private static MultiWordResult generateMultiWordResult(List<String> listString, List<Long> listLong,
                                                           Block block){
        String[] query = listString.toArray(new String[listString.size()]);
        Long[] locsLong = listLong.toArray(new Long[listLong.size()]);
        long[] locs = new long[locsLong.length];
        for (int i = 0; i < locs.length; i++)
            locs[i] = locsLong[i];
        return new MultiWordResult(query, block, locs);
    }

    /**
     * @param fittingWords gets the giant map
     * @param block gets a block to add an element in
     * @param pattern gets a string to add the word in
     * @param startIndex gets the start index from which to create the word container
     * this function add the block, pattern, startIndex to the correct place in the fittingWords
     */
    static void addToMap(Map<Block, Map<String, List<WordContainer>>> fittingWords, Block block,
                         String pattern, Integer startIndex) {
        //if the block key wasn't created
        if (!fittingWords.containsKey(block))
            fittingWords.put(block, new HashMap<>());
        //if the pattern is not in the block map
        if (!fittingWords.get(block).containsKey(pattern))
            fittingWords.get(block).put(pattern, new LinkedList<>());
        //add the new word
        fittingWords.get(block).get(pattern).add(new WordContainer(block, pattern, startIndex));
    }

    /**
     * @param wordList gets a map of string to all the places the word appeared
     * @return true if the map contains all the patterns, else false
     */
    static boolean ContainsAll(Map<String, List<WordContainer>> wordList, List<String>  patterns){
        if(wordList == null)
            return false;
        for (String pattern : patterns){
            if (!wordList.containsKey(pattern))
                return false;
        }
        return true;
    }


    /**
     * @param words gets a list of word results
     * @return the list sorted by the entry name
     */
    static List<WordResult> sortByLexicographic(List<WordResult> words){
        Collections.sort(words, Comparator.comparing((WordResult o) -> o.getBlock().getEntryName()));
        return words;
    }

    /**
     * @param query a query to search
     * @param func a function that chooses whether to leave the word in the query
     * @return a lost of the filtered strings
     */
    static List<String> filterByLambda(String query, Function<String, String> func){
        String[] wordsToSearch = query.split("\\s");
        for(int i = 0; i < wordsToSearch.length; i++)
            wordsToSearch[i] = func.apply(wordsToSearch[i]);
        List<String> patterns = new LinkedList<>(Arrays.asList(wordsToSearch));
        patterns.removeIf((String s) -> s.equals(""));
        return patterns;
    }
}
