package Dictionary;

import java.io.*;
import java.util.ArrayList;

public abstract class ConcatenatedStringDict
{
    //remember paths to use
    protected String dir, name, path_string, path_dict, path_meta_data;
    //writes of the string and meta data
    protected RandomAccessFile reader_string, meta_data_rw;
    //reader of the dictionary
    protected FileInputStream reader_dict;
    //writer of the dictionary
    protected FileOutputStream writer_dict;
    //writer of the long string
    protected OutputStream writer_string;
    //the number of rows in the data
    protected int num_rows;
    //is the dictionary already loaded
    public boolean loaded;
    //is the dictionary already saved
    public boolean saved;
    //the type of the output of the dictionary
    protected DictOutputType dict_type;
    //does the element exists
    public static final int NOT_EXISTS = -1;

    private boolean closed = false;

    /**
     * @param dir the directory of the saved dict
     * @param field_name the field name of the dict (what it stores)
     * @param for_writing do we write the dict or read it
     * @param p_dict_type what does the dict return
     * @throws FileNotFoundException if file not found
     */
    public ConcatenatedStringDict(String dir, String field_name, boolean for_writing, DictOutputType p_dict_type)
            throws FileNotFoundException {
        this.dir = dir;
        this.name = field_name;
        this.dict_type = p_dict_type;
        this.closed = false;
        this.path_string = dir + File.separatorChar + name + ".string";
        this.path_dict = dir + File.separatorChar + name + ".concat_dict";
        this.path_meta_data = dir + File.separatorChar + name + ".mata_dict";
        try {
            new File(path_string).createNewFile();
            new File(path_dict).createNewFile();
            new File(path_meta_data).createNewFile();
            reader_string = new RandomAccessFile(path_string, "r");

            reader_dict = new FileInputStream(path_dict);
        } catch (IOException e) {
            e.printStackTrace();
        }
        if (for_writing)
            writer_string = new BufferedOutputStream(new FileOutputStream(path_string));
        else
            writer_string = null;
        loaded = false;
        saved = false;
    }

    /**
     * @return get the type of return of the dictionary
     */
    public DictOutputType get_dict_type()
    {
        return dict_type;
    }
    /**
     * append the given word to the end of the concatenated string
     * @param last_word array of bytes
     */
    public abstract void append(byte[] last_word);

    /**
     * append the given word to the end of the concatenated string with string encoding
     * @param last_word array of bytes
     */
    public abstract void append(String last_word);

    /**
     * append the given word to the end of the concatenated string with int encoding
     * @param last_word array of bytes
     */
    public abstract void append(ArrayList<Integer> last_word);

    /**
     * @param i index, represent the i'th word in the concatenated string
     * @return the i'th word in the concatenated string
     */
    public abstract byte[] read(int i);

    /**
     * @param i index, represent the i'th word in the concatenated string after decoding with string
     *          compression
     * @return the i'th word in the concatenated string
     */
    public abstract byte[] read(int i, String s);

    /**
     * @param i index, represent the i'th word in the concatenated string after decoding with int  compression
     * @return the i'th word in the concatenated string
     */
    public abstract byte[] read(int i, int j);

    /**
     * @param st the bytes to search
     * @return the index of the string represented by st if exists in the index, else -1
     */
    public abstract int get_index_by_string(byte[] st);

    /**
     * @param st the String to search
     * @return the index of the string if exists in the index, else -1
     */
    public abstract int get_index_by_string(String st);

    /**
     * saves the dict to disk
     */
    public abstract void save_to_disk();

    /**
     * loads the dict from disk
     */
    public abstract void load_from_disk();

    /**
     * @param a arr1
     * @param b arr3
     * @return true iff a < b
     */
    protected boolean is_smaller(byte[] a, byte[] b)
    {
        int min_size = Math.min(a.length, b.length);
        for (int i = 0; i < min_size; i++)
            if (a[i] != b[i])
                return a[i] < b[i];
        // otherwise the prefix is same, the longest is greater
        return a.length < b.length;
    }

    public int getNumRows(){return num_rows;}


    public void close() throws IOException {
        closed = true;
        reader_string.close();
        reader_dict.close();
        meta_data_rw.close();
        if(writer_dict != null)
        {
            writer_dict.close();
        }
        if(writer_string != null)
        {
            writer_string.close();
        }
    }

    public boolean isClosed()
    {
        return closed;
    }

    public void flush() throws IOException {
        writer_string.flush();
    }

    public abstract void append(int n);

    public abstract void finishAppending();
    public abstract void startAppending();

    public void startReading(int i){}
    public int readNext(){return -1;}
}
