package webdata;

import java.io.File;

public class IndexWriter {
    /**
     * Given product review data, creates an on disk index
     * inputFile is the path to the file containing the review data
     * dir is the directory in which all index files will be created
     * if the directory does not exist, it should be created
     */
    public void write(String inputFile, String dir)
    {
        SlowIndexWriter ind_w = new SlowIndexWriter();
        ind_w.slowWrite(inputFile, dir, 0, true);
    }


    /**
     * Delete all index files by removing the given directory
     */
    public void removeIndex(String dir)
    {
        File index = new File(dir);
        if(!index.exists())
        {
            return;
        }
        String[] entries = index.list();
        if(entries != null)
        {
            for(String s: entries){
                File currentFile = new File(index.getPath(), s);
                currentFile.delete();
            }
        }
        index.delete();
    }
}

