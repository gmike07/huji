package webdata;

public class IndexWriter {
    SlowIndexWriter writer;
    /**
     * Given product review data, creates an on disk index
     * inputFile is the path to the file containing the review data
     * dir is the directory in which all index files will be created
     * if the directory does not exist, it should be created
     */
    public void write(String inputFile, String dir)
    {
        writer = new SlowIndexWriter();
        writer.slowWrite(inputFile, dir);
    }
    /**
     * Delete all index files by removing the given directory
     */
    public void removeIndex(String dir)
    {
        writer.removeIndex(dir);
    }
}
