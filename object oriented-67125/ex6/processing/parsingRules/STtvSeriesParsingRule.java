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

public class STtvSeriesParsingRule implements IparsingRule, Serializable {
	public static final long serialVersionUID = 1L;
	/* a list of all the metadata for the entry */
	private List<String> metadataEntry;

	private static final Pattern scenePattern = Pattern.compile("[\\n\\r](\\d+)\\s+(.+)\\s*");
	private static final Pattern actorsPattern = Pattern.compile("[\\n\\r]\\t{5}([\"\\w].*)");
	private static final Pattern titlePattern = Pattern.compile("\\s*STAR TREK: THE NEXT GENERATION\\s*\"(" +
			".*)\"");
	private static final Pattern byPattern = Pattern.compile("\\s*(.*) by\\s+(.*)[\\s\\n\\r]+" +
			"(and[\\s\\n\\r]+(.*))?");
	/* the number group that holds the prefix of by (writen for example) */
	private static final int BY = 1;
	/* the number group of the first writer */
	private static final int FIRST_BY = 2;
	/* the number group that contains a second writer if such exists */
	private static final int IS_TWO_BY = 3;
	/* the number group of the second writer */
	private static final int SECOND_BY = 4;
	public STtvSeriesParsingRule() {
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
		String textHeader = ToolBox.readFromFile(inputFile, 0, endHeader);
		Matcher titleMatcher = titlePattern.matcher(textHeader);
		if(!titleMatcher.find())
			throw new IOException("no title for the episode, u monster!");
		metadataEntry.add("the title of the episode is: \"" + titleMatcher.group(1) + "\"");


		Matcher byMatcher = byPattern.matcher(textHeader);
		while(byMatcher.find()) {
			String by = "";
			String writers = byMatcher.group(FIRST_BY);
			if (!byMatcher.group(BY).equals(""))
				by = byMatcher.group(BY) + " ";
			if (byMatcher.group(IS_TWO_BY) != null) {
				writers = writers.trim();
				writers += " and " + byMatcher.group(SECOND_BY).trim();
			}
			metadataEntry.add(by + "by: " + writers);
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
