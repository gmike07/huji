package processing.searchStrategies;

import processing.textStructure.Block;
import processing.textStructure.Corpus;
import processing.textStructure.Entry;
import processing.textStructure.WordResult;

import java.util.*;

public class NaiveSearch implements IsearchStrategy {
	private Corpus origin;
	public NaiveSearch(Corpus origin) {
		this.origin = origin;
	}


	/**
	 * The main search method to comply with the IsearchStrategy interface
	 * @param query The query string to search for.
	 * @return  A list of wordResults
	 */
	@Override
	public List<WordResult> search(String query) {
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
	protected void searchBlock(Block block, List<WordResult> results, String pattern){
		int m = pattern.length();
		String text = block.toString();
		int n = text.length();
		for (int i = 0; i + m <= n; i++) {
			if (text.substring(i, i + m).equals(pattern))
				results.add(new WordResult(block, new String[]{pattern}, i));
			}
		}
	}
