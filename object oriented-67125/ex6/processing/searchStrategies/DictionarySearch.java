package processing.searchStrategies;

import processing.textStructure.Block;
import processing.textStructure.Word;
import processing.textStructure.WordResult;
import utils.ToolBox;

import java.util.*;

public class DictionarySearch implements IsearchStrategy {

	private Map<Integer, List<Word>> dict;

	public DictionarySearch(HashMap<Integer, List<Word>> dict) {
		this.dict = dict;
	}

	@Override
	/*
	 * The main abstract method - Search a quary string (could be multiple words) and return a result list.
	 * @param query The query string to search for.
	 * @return  A list of result objects
	 */
	public List<? extends WordResult> search(String query) {
		Map<Block, Map<String, List<WordContainer>>> fittingWords = new HashMap<>();
		List<String> patterns = SearchHelper.filterByLambda(query, stemmer::stem);
		patterns.removeIf((String s) -> s.equals(""));


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
		for (String pattern : stemmedWords) {
			if(dict.get(pattern.hashCode()) == null)
				continue;
			for (Word word : dict.get(pattern.hashCode())){
					String result = ToolBox.readFromFileNoIO(word.getSrcBlk().getRAF(), word.getEntryIndex(),
							pattern.length());
					if (pattern.equals(result)) {
						SearchHelper.addToMap(fittingWords, word.getSrcBlk(), result,
								(int) (word.getEntryIndex() - word.getSrcBlk().getStartIndex()));
					}
			}
		}
		LinkedList<Block> toDelete = new LinkedList<>();
		for (Block block : fittingWords.keySet()){
			//if doesn't contain all words, delete it
			if (!SearchHelper.ContainsAll(fittingWords.get(block), stemmedWords))
				toDelete.add(block);
		}
		for(Block block : toDelete)
			fittingWords.remove(block);
	}
}
