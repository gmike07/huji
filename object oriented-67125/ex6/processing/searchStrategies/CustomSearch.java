package processing.searchStrategies;

import processing.textStructure.Block;
import processing.textStructure.Corpus;
import processing.textStructure.Entry;
import processing.textStructure.WordResult;

import java.util.ArrayList;
import java.util.List;

import static java.lang.Math.max;

/**
 * Custom Search based on Boyer Moore Algorithm
 */
public class CustomSearch implements IsearchStrategy {
    private Corpus origin;
    static int NO_OF_CHARS = 256;


    public CustomSearch(Corpus origin){
        this.origin = origin;
    }
    @Override
    /*
     * The main search method to comply with the IsearchStrategy interface
     * @param query The query string to search for.
     * @return  A list of wordResults
     */
    public List<? extends WordResult> search(String query) {
        List<WordResult> goodResults = new ArrayList<>();
        for (Entry entry : origin) {
            for (Block block : entry)
                searchBlock(block, goodResults, query);
        }
        return SearchHelper.sortByLexicographic(goodResults);
    }

    /**
     * @param block the block to search in
     * @param results the results list to append results to
     * @param pattern the pattern to search
     * adds all results to the results list
     */
    private void searchBlock(Block block, List<WordResult> results, String pattern) {

        int m = pattern.length();
        String text = block.toString();
        int n = text.length();

        int[] badChars = badCharHeuristic(pattern);

        int shift = 0;

        while (shift <= (n - m))
        {
            int j = m - 1;
            // Search from end to start for matching characters
            while (j >= 0 && pattern.charAt(j) == text.charAt(shift + j))
                j--;

            // All characters matched
            if (j < 0) {
                results.add(new WordResult(block, new String[]{pattern}, shift));
                shift += (shift + m < n) ? m - badChars[text.charAt(shift + m)] : 1;
            }

            // Shift to last appearance
            else
                shift += max(1, j - badChars[text.charAt(shift + j)]);
        }
    }

    /**
     * Computes a table for the bad char heuristic
     * @param str String to create table for
     */
    private static int[] badCharHeuristic(String str) {
        int i;
        int[] badChars = new int[NO_OF_CHARS];

        for (i = 0; i < NO_OF_CHARS; i++)
            badChars[i] = -1;

        // Last appearance of each character
        for (i = 0; i < str.length(); i++)
            badChars[(int)str.charAt(i)] = i;
        
        return badChars;
    }
}
