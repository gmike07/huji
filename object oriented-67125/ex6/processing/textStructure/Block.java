package processing.textStructure;

import utils.ToolBox;

import java.io.RandomAccessFile;
import java.io.Serializable;
import java.util.LinkedList;
import java.util.List;

/**
 * This class represents an arbitrary block of text within a file
 */
public class Block implements Serializable {
	public static final long serialVersionUID = 1L;
	/* this variable contains the metaData of this block */
	private List<String> meta = new LinkedList<>();
	/* this variable the end index of the block */
	private long endIdx;
	/* this variable the file of the block */
	transient RandomAccessFile inputFile;
	/* this variable the start index of the block */
	private long startIdx;
	/* this variable the fileName of the block */
	private String entryName;

	/**
	 * Constructor
	 * @param inputFile     the RAF object backing this block
	 * @param startIdx      start index of the block within the file
	 * @param endIdx        end index of the block within the file
	 */
	public Block(RandomAccessFile inputFile, long startIdx, long endIdx) {
		this.inputFile = inputFile;
		this.startIdx = startIdx;
		this.endIdx = endIdx;

	}

	/**
	 * The filename from which this block was extracted
	 * @return  filename
	 */
	public String getEntryName(){
		return this.entryName;
	}

	/**
	 * @param entryName the filename from which this block was extracted
	 */
	void setEntryName(String entryName){
		this.entryName = entryName;
		this.meta.add("Taken out of the entry \"" + getEntryName() + "\"");
	}



///////// getters //////////
	/**
	 * @return start index
	 */
	public long getStartIndex() {
		return startIdx;
	}
	
	/**
	 * @return  end index
	 */
	public long getEndIndex() {
		return endIdx;
	}
	
	/**
	 * Convert an abstract block into a string
	 * @return  string representation of the block (the entire text of the block from start to end indices)
	 */
	@Override
	public String toString() {
		return ToolBox.readFromFileNoIO(inputFile, startIdx, (int)(endIdx - startIdx));
	}
	
	/**
	 * Adds metadata to the block
	 * @param metaData A list containing metadata entries related to this block
	 */
	public void setMetadata(List<String> metaData) {
		this.meta = metaData;
	}

	/**
	 * @return the RAF object for this block
	 */
	public RandomAccessFile getRAF() {
		return this.inputFile;
	}
	
	/**
	 * Get the metadata of the block, if applicable for the parsing rule used
	 * @return  String of all metadata.
	 */
	public List<String> getMetadata() {
		return this.meta;
	}


	/**
	 * @param raf updates the raf in the block
	 */
	void updateRaf(RandomAccessFile raf){
		this.inputFile = raf;
	}
}
