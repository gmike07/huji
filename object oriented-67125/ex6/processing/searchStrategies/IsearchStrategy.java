package processing.searchStrategies;
import processing.textStructure.WordResult;
import utils.Stemmer;

import java.util.List;

/**
 * A functional interface describing the contract any search Strategy must implement.
 */
public interface IsearchStrategy {
	/**
	 * A Stemmer object to be used internally for manipulating words.
	 */
    final Stemmer stemmer = new Stemmer();

	/**
	 * The main abstract method - Search a quary string (could be multiple words) and return a result list.
	 * @param query The query string to search for.
	 * @return  A list of result objects
	 */
	List<? extends WordResult> search(String query);
}
