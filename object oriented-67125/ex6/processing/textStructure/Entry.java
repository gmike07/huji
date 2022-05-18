package processing.textStructure;

import processing.parsingRules.IparsingRule;
import utils.MD5;
import utils.ToolBox;
import java.io.*;
import java.util.Iterator;
import java.util.List;

/**
 * This class represents a single file within a Corpus
 */
public class Entry implements Iterable<Block>, Serializable {
	public static final long serialVersionUID = 1L;
	/* represents the parsing rule used in the entry */
    private IparsingRule iparsingRule;
	/* represents the path to the entry */
    private String path;
	/* represents the blocks in the entry as a list */
    private List<Block> blockList;

	/**
	 * @param filePath the path to this entry
	 * @param parseRule the parsing rule used in the entry
	 */
	public Entry(String filePath, IparsingRule parseRule){
    	this.path = filePath;
    	this.iparsingRule = parseRule;
    }

	/**
	 * Iterate over Block objects in the Entry
	 * @return a block iterator
	 */
	@Override
    public Iterator<Block> iterator() {
    	return this.blockList.iterator();
    }


	/**
	 * creates the blocks of this entry
	 * @throws FileNotFoundException if the raf couldn't be created
	 */
	void populate() throws IOException {
		String fileName = new File(path).getName();
		this.blockList = iparsingRule.parseFile(new RandomAccessFile(this.path, "r"));
		for(Block block : blockList)
			block.setEntryName(fileName);
	}

	/**
	 * updates the raf for every block
	 * @throws FileNotFoundException if the raf couldn't be created
	 */
	void updateRAF() throws FileNotFoundException {
		RandomAccessFile raf = new RandomAccessFile(this.path, "r");
		for (Block block : blockList)
			block.updateRaf(raf);
	}

	/**
	 * @return the checksum of this entry
	 */
	String getChecksum() throws IOException {
		return MD5.getMd5(ToolBox.readFile(new RandomAccessFile(this.path, "r")));
	}


}
