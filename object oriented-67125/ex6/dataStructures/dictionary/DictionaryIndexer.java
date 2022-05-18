package dataStructures.dictionary;

import dataStructures.Aindexer;
import dataStructures.ObjectWriter;
import processing.parsingRules.IparsingRule;
import processing.searchStrategies.DictionarySearch;
import processing.textStructure.Block;
import processing.textStructure.Corpus;
import processing.textStructure.Entry;
import processing.textStructure.Word;
import utils.Stemmer;
import utils.WrongMD5ChecksumException;

import java.io.*;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * An implementation of the abstract Aindexer class, backed by a simple hashmap to store words and their
 * locations within the files.
 */
public class DictionaryIndexer extends Aindexer<DictionarySearch> {
	/* the pattern to find words in the text */
	private static final Pattern pattern = Pattern.compile("(\\w+)\\s+");
	/* the dict to store all words */
	private HashMap<Integer, List<Word>> dict;
	/* a stemmer to make words easier to read */
	private static final Stemmer STEMMER = new Stemmer();

	/**
	 * Basic constructor, sets origin Corpus and initializes backing hashmap
	 * @param origin    the Corpus to be indexed by this DS.
	 */
	public DictionaryIndexer(Corpus origin) {
		super(origin);
		this.dataStructType = IndexTypes.DICT;
	}

	@SuppressWarnings("unchecked")
	@Override
	/*
	 * Try to read a cached index file if one already exists.
	 * @throws FileNotFoundException
	 * @throws WrongMD5ChecksumException
	 */
	protected void readIndexedFile() throws WrongMD5ChecksumException, FileNotFoundException {
		dict = (HashMap<Integer, List<Word>>) ObjectWriter.readIndexedFile(this);
	}

	/*
	 * Write the internal index into file.
	 */
	@Override
	protected void writeIndexFile() {
		ObjectWriter.writeIndexedFile(this, dict);
	}

	@Override
	/*
	 * Index the Corpus internally using the parsing rules defined for this datastructure.
	 */
	protected void indexCorpus() {
		dict = new HashMap<>();
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
			String stemmed = STEMMER.stem(matcher.group(1));
			if (!stemmed.equals("")) {
				int hash = stemmed.hashCode();
				if (!dict.containsKey(hash))
					dict.put(hash, new LinkedList<>());
				dict.get(hash).add(new Word(block, matcher.start(1), matcher.end(1)));
			}
		}
	}

	@Override
	/*
	  Extract the parsing rule used for indexing this data structure.
	  @return  an instance of a parser implementing IparsingRule
	 */
	public IparsingRule getParseRule() {
		return origin.getParsingRule();
	}

	
	@Override
	/*
	 * get the backing search interface.
	 * @return  The search interface implementation used by this indexer.
	 */
	public DictionarySearch asSearchInterface() {
		return new DictionarySearch(dict);
	}

}
