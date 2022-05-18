
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * A utilities class for ex4 in oop.
 *
 */
public class Ex4Utils {

	/**
	 * Reads a text file (such that each line contains a single word), 
	 * and returns a string array of its lines.
	 * @param fileName Text file to read.
	 * @return Array with the file's content (returns null if the IOException occurred).
	 */
	public static String[] file2array(String fileName) {
		// A list to hold the file's content
		List<String> fileContent = new ArrayList<String>();

		// Reader object for reading the file
		BufferedReader reader = null;

		try {
			// Open a reader
			reader = new BufferedReader(new FileReader(fileName));

			// Read the first line
			String line = reader.readLine();

			// Go over the rest of the file
			while (line != null) {

				// Add the line to the list
				fileContent.add(line);

				// Read the next line
				line = reader.readLine();
			}

		} catch (FileNotFoundException e) {
			System.err.println("ERROR: The file: " + fileName + " is not found.");
			return null; 
		} catch (IOException e) {
			System.err.println("ERROR: An IO error occurred.");
			return null; 
		} finally {
			// Try to close the file
			try {
				if(reader != null)
					reader.close();
				else
					return null;
			} catch (IOException e) {
				System.err.println("ERROR: Could not close the file " + fileName + ".");
			}
		}

		// Convert the list to an array and return the array
		String[] result = new String[fileContent.size()];
		fileContent.toArray(result);
		return result;
	}
}
