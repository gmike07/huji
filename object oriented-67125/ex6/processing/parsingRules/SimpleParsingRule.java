package processing.parsingRules;

import processing.textStructure.Block;
import processing.textStructure.WordResult;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.io.Serializable;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class SimpleParsingRule implements IparsingRule, Serializable {
	public static final long serialVersionUID = 1L;


	public SimpleParsingRule() {

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
		return new Block(inputFile, startPos, endPos);
	}

	@Override
	/*
	 * A parser for the entire file.
	 * @param inputFile The RandomAccessFile from which we are reading.
	 * @return  A list of Block objects describing the file.
	 */
	public List<Block> parseFile(RandomAccessFile inputFile) {

		final Pattern p = Pattern.compile(getSplitRegex(), Pattern.DOTALL);
		final Matcher m = p.matcher("");

		List<Block> entryBlocks = new LinkedList<>();
		int rawChunkSize = MAXLINELENGTH * 15;
		byte[] rawBytes = new byte[rawChunkSize];
		try {
			long endOfBlockOffset = 0, curBlockEnd;
			Long lastIndex = inputFile.length();
			for (long i = endOfBlockOffset; i < lastIndex; i += rawChunkSize) {
				inputFile.seek(i);
				int bytesRead = inputFile.read(rawBytes);
				String rawBlock = new String(rawBytes);
				m.reset(rawBlock);
				while (m.find()) {
					if (m.end()-m.start() > 1) {
						entryBlocks.add(parseRawBlock(inputFile, m.start() + i, m.end() + i));
					}
					endOfBlockOffset = m.end();
				}
				i -= (rawChunkSize - endOfBlockOffset);
			}

		} catch (IOException e) {
			e.printStackTrace();
		}
		return entryBlocks;

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

	//TODO: check this works
	private String getSplitRegex() {
		return "(.*[\\n\\r][\\n\\r]){1,5}";
	}



}
