package dataStructures.naive;

import dataStructures.Aindexer;
import processing.parsingRules.IparsingRule;
import processing.searchStrategies.NaiveSearch;
import processing.searchStrategies.NaiveSearchRK;
import processing.textStructure.Corpus;
import utils.WrongMD5ChecksumException;

/**
 * A "naive" indexer. This approach forgoes actually preprocessing the file,
 * and simply loads the text and searches directly on it.
 */
public class NaiveIndexer extends Aindexer<NaiveSearch> {
	/* contains whether to use rk metohd or not */
	private final boolean isRK;

	/**
	 * Basic constructor
	 * @param corpus    The corpus to search over
	 * @param RK        Whether or not to use Rabin-Karp search strategy
	 */
	public NaiveIndexer(Corpus corpus, boolean RK){
		super(corpus);
		this.isRK = RK;
		this.dataStructType = isRK ? IndexTypes.NAIVE_RK : IndexTypes.NAIVE;
	}

	/**
	 * Basic constructor
	 * @param corpus    The corpus to search over
	 */
	public NaiveIndexer(Corpus corpus) {
		super(corpus);
		this.isRK = false;
	}

	@Override
	/*
	 * Index the Corpus internally using the parsing rules defined for this datastructure.
	 */
	protected void indexCorpus() {
		// does nothing
	}

	@Override
	/*
	 * Try to read a cached index file if one already exists.
	 */
	protected void readIndexedFile() throws WrongMD5ChecksumException {
		throw new WrongMD5ChecksumException();
	}

	@Override
	/*
	 * Write the internal index into file.
	 */
	protected void writeIndexFile() {
		//does nothing
	}


	public Corpus getOrigin() {
		return this.origin;
	}


	@Override
	/*
	 * Extract the parsing rule used for indexing this data structure.
	 * @return  an instance of a parser implementing IparsingRule
	 */
	public IparsingRule getParseRule() {
		return this.origin.getParsingRule();
	}


	@Override
	/*
	 * get the backing search interface.
	 * @return  The search interface implementation used by this indexer.
	 */
	public NaiveSearch asSearchInterface() {
		return this.isRK ? new NaiveSearchRK(this.origin) : new NaiveSearch(this.origin);
	}


}
