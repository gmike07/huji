package processing.parsingRules;

import processing.textStructure.Block;
import processing.textStructure.WordResult;
import utils.ToolBox;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.io.Serializable;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class STmovieParsingRule implements IparsingRule, Serializable {
	public static final long serialVersionUID = 1L;
	/* a list of all the metadata for the entry */
	private List<String> metadataEntry;

	private static final Pattern scenePattern = Pattern.compile("[\\n\\r]\\s*(\\d+)\\s*(.*?)\\s*\\1");
	private static final Pattern actorsPattern = Pattern.compile("[\\n\\r]\\s{43}(\\w.*)\\s*");
	private static final Pattern byPattern = Pattern.compile("\\s*(.*)?by:\\s*(.*)");
	/* the number group that holds the prefix of by (writen for example) */
	private static final int BY = 1;
	/* the number group of the writers */
	private static final int WRITE_BY = 2;
	public STmovieParsingRule() {
	}



	@Override
	/*
	 * A parser for a single block of text
	 * @param inputFile A RandomAccessFile from which we are reading
	 * @param startPos  The starting position of the block within the file
	 * @param endPos    The end position of the block within the file
	 * @return          A Block Object.
	 */
	public Block parseRawBlock(RandomAccessFile inputFile, long startPos, long endPos) {
		Block block = new Block(inputFile, startPos, endPos);
		ParsingHelper.addMetadataToBlock(block, metadataEntry, actorsPattern);
		return block;
	}


	@Override
	/*
	 * A parser for the entire file.
	 * @param inputFile The RandomAccessFile from which we are reading.
	 * @return  A list of Block objects describing the file.
	 */
	public List<Block> parseFile(RandomAccessFile inputFile) throws IOException {
		Matcher sceneMatcher = scenePattern.matcher(ToolBox.readFile(inputFile));
		if(!sceneMatcher.find())
			throw new IOException("no scenes in the file");
		createEntryMetadata(inputFile, sceneMatcher.start());
		return ParsingHelper.parseScenes(inputFile, sceneMatcher, this);
	}


	/**
	 * @param inputFile the input file
	 * @param endHeader up to where is the header
	 * @throws IOException if reading from the file caused an error
	 * fills all the metadata of the file to the metadataEntry list
	 */
	private void createEntryMetadata(RandomAccessFile inputFile, int endHeader) throws IOException {
		metadataEntry = new LinkedList<>();
		Matcher byMatcher = byPattern.matcher(ToolBox.readFromFile(inputFile, 0, endHeader));
		while(byMatcher.find()) {
			String by = byMatcher.group(BY);
			if(by == null)
				by = "";
			metadataEntry.add(by + "by: " + byMatcher.group(WRITE_BY));
		}
	}

	@Override
	/*
	 * Print a WordResult object according to the parsing rules.
	 * @param wordResult    The WordResult to be printed
	 * @throws IOException  If the RAF misbehaves.
	 */
	public void printResult(WordResult wordResult) throws IOException {
		System.out.println("The result: \n" + wordResult.resultToString());
	}
}