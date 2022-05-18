package processing.textStructure;

import processing.parsingRules.IparsingRule;

import java.io.IOException;
import java.util.Iterator;

/**
 * This class represents a body of works - anywhere between one and thousands of documents sharing the same structure and that can be parsed by the same parsing rule.
 */
public class Corpus implements Iterable<Entry>{

    public Corpus(String path, IparsingRule parsingRule) throws IOException {
        /*
        check if the path is a folder or file.
        if file - single entry corpus.
        otherwise, recursively scan the directory for all subdirectories and files.
        each entry in a corpus should hold the folder from which the file came.
         */
	    //TODO implement me!!!

    }


	/**
	 * Return the parsing rule used for this corpus
	 * @return
	 */
	public IparsingRule getParsingRule() {
		//TODO implement me!!!
	}

    /**
     * Iterate over Entry objects in the Corpus
     * @return  An Entry iterator
     */
    @Override
    public Iterator<Entry> iterator() {
	    //TODO implement me!!!
    }

    /**
     * Return the checksum of the entire corpus.
     * Can be calculated by getting the checksum of each file, then concating them to one string and
     * returning the checksum of that string.
     * @return
     */
    public String getChecksum() {
	    //TODO implement me!!!
    }


}
