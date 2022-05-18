package Join;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public abstract class IExternalMemory {

	public abstract void sort(String in, String out, String tmpPath);

	protected abstract void join(String in1, String in2, String out, String tmpPath);
	
	protected abstract void select(String in, String out, String substrSelect, String tmpPath);
	
	
	public abstract void joinAndSelectEfficiently(String in1, String in2, String out, String substrSelect, String tmpPath);

	/**
	 * Do not modify this method!
	 * 
	 * The method sorts the input files in a lexicographic order of first column, joins the files, and
	 * saves the result in an output file.
	 * 
	 * @param in1
	 * @param in2
	 * @param out
	 * @param tmpPath
	 */

	public void sortAndJoin(String in1, String in2, String out,
			String tmpPath) {
		String outFileName = new File(out).getName();
		String tmpFileName1 = outFileName.substring(0, outFileName.lastIndexOf('.'))
				+ "_intermed1" + outFileName.substring(outFileName.lastIndexOf('.'));
		String tmpOut1 = Paths.get(tmpPath, tmpFileName1).toString();
		String tmpFileName2 = outFileName.substring(0, outFileName.lastIndexOf('.'))
				+ "_intermed2" + outFileName.substring(outFileName.lastIndexOf('.'));
		String tmpOut2 = Paths.get(tmpPath, tmpFileName2).toString();

		this.sort(in1, tmpOut1,tmpPath);
		this.sort(in2, tmpOut2,tmpPath);
		this.join(tmpOut1,tmpOut2,out,tmpPath);

		try {
			Files.deleteIfExists(Paths.get(tmpPath, tmpFileName1));
			Files.deleteIfExists(Paths.get(tmpPath, tmpFileName2));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Do not modify this method!
	 * 
	 * The method joins the files, then selects the lines that contain substrSelect, and
	 * saves the result in an output file.
	 * 
	 * @param in1
	 * @param in2
	 * @param out
	 * @param substrSelect
	 * @param tmpPath
	 */
	public void joinAndSelect(String in1, String in2, String out, String substrSelect, String tmpPath) {
		String outFileName = new File(out).getName();
		String tmpFileName = outFileName.substring(0, outFileName.lastIndexOf('.'))
				+ "_intermed" + outFileName.substring(outFileName.lastIndexOf('.'));
		String tmpOut = Paths.get(tmpPath, tmpFileName).toString();
		sortAndJoin(in1,in2,tmpOut,tmpPath);
		this.select(tmpOut,out,substrSelect,tmpPath);
		try {
			Files.deleteIfExists(Paths.get(tmpPath, tmpFileName));
		} catch (IOException e) {
			e.printStackTrace();
		}
				
	}
}
