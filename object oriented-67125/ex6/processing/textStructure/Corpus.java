package processing.textStructure;

import processing.parsingRules.IparsingRule;
import processing.parsingRules.ParsingFactory;
import utils.MD5;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.Serializable;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

/**
 * This class represents a body of works - anywhere between one and thousands of documents sharing the same
 * structure and that can be parsed by the same parsing rule.
 */
public class Corpus implements Iterable<Entry>, Serializable {
	public static final long serialVersionUID = 1L;
	/* represents the entries in the corpus as a list */
    private List<Entry> entryList;
	/* represents the parsing rule used in the corpus */
    private IparsingRule parsingRule;
	/* represents the path to the corpus */
    private String corpusPath;

	/**
	 * @param path the path to the corpus
	 * @param parserName the string representation of the parser
	 */
    public Corpus(String path, String parserName){
   		this.corpusPath = path;
   		this.parsingRule = ParsingFactory.getParsingRule(parserName);
		this.entryList = new LinkedList<>();
		generateEntries(new File(this.corpusPath), entryList);
    }

	/**
	 * @param entries all the entries up to now
	 * @param file the current file to check
	 *  adds all the files in file to the entries
	 */
	private void generateEntries(File file, List<Entry> entries){
		if (file.isFile() && !file.getName().endsWith(".cache")){
			entries.add(new Entry(file.getPath(), parsingRule));
		}else if (file.isDirectory()){
			File[] directory = file.listFiles();
			if (directory != null)
				for (File f : directory)
					generateEntries(f, entries);
		}
	}


	/**
	 * This method populates the Block lists for each Entry in the corpus.
	 */
	public void populate() throws IOException {
    	for (Entry entry : entryList)
    		entry.populate();
    }
    

	/**
	 * The path to the corpus folder
	 * @return A String representation of the absolute path to the corpus folder
	 */
	public String getPath() {
		return this.corpusPath;
    }

	/**
	 * Iterate over Entry objects in the Corpus
	 * @return An entry iterator
	 */
	@Override
    public Iterator<Entry> iterator() {
        return this.entryList.iterator();
    }

	/**
	 * Return the checksum of the entire corpus. This is an MD5 checksum which represents all the files in the corpus.
	 * @return A string representing the checksum of the corpus.
	 * @throws IOException if any file is invalid.
	 */
	public String getChecksum() throws IOException {
		StringBuilder checkSum = new StringBuilder();
		for (Entry entry : entryList)
			checkSum.append(entry.getChecksum());
		return MD5.getMd5(checkSum.toString());
    }

	/**
	 * Return the parsing rule used for this corpus
	 * @return the parsing rule used for this corpus
	 */
	public IparsingRule getParsingRule() {
        return this.parsingRule;
    }

	/**
	 * Update the RandomAccessFile objects for the Entries in the corpus, if it was loaded from cache.
	 */
	public void updateRAFs() throws FileNotFoundException {
		for (Entry entry : entryList)
			entry.updateRAF();
	}
}
