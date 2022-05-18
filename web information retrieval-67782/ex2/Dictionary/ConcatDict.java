package Dictionary;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;

import CompressionV2.*;
import tools.index_tools;

public class ConcatDict extends ConcatenatedStringDict
{
    //stores ptrs while writing
    private ArrayList<Integer> ptr;
    //stores ptrs after pre processing
    private byte[] ptr_dict;
    //stores current pointer in file
    private int current_ptr;
    //the compression to use if we want to compress int
    private AbstractIntegerCompression integerCompression;
    //the compression to use if we want to compress string
    private AbstractStringCompression stringCompression;
    //stream to write with to the file for compression
    private OutputStreamHelper helper_string_writer;
    //stream to read with from file for compression
    private InputStreamHelper helper_string_reader;

    private InputStream inputStream = null;


    private InputStreamHelper readOneFromString = null;

    /**
     * @param dir the directory of the saved dict
     * @param field_name the field name of the dict (what it stores)
     * @param for_writing do we write the dict or read it
     * @param type what does the dict return
     * @param int_comp int compression
     * @param str_comp string compression
     * @throws FileNotFoundException if file not found
     */
    public ConcatDict(String dir, String field_name, boolean for_writing, DictOutputType type,
                      AbstractIntegerCompression int_comp, AbstractStringCompression str_comp) throws FileNotFoundException {
        super(dir, field_name, for_writing, type);
        ptr = new ArrayList<>();
        helper_string_writer = new OutputStreamHelper(writer_string);
        helper_string_reader = new InputStreamHelper(reader_string);
        stringCompression = str_comp;
        integerCompression = int_comp;
        current_ptr = 0;
        ptr.add(current_ptr);
    }



    public ConcatDict(String dir, String field_name, boolean for_writing, DictOutputType type,
                      AbstractIntegerCompression int_comp, AbstractStringCompression str_comp, int v) throws IOException {
        this(dir, field_name, for_writing, type, int_comp, str_comp);
        inputStream = new BufferedInputStream(new FileInputStream(reader_string.getFD()));
        helper_string_reader = new InputStreamHelper(inputStream);
    }


    /**
     * append the given word to the end of the concatenated string
     * @param last_word array of bytes
     */
    @Override
    public void append(byte[] last_word)
    {
        try {
            writer_string.write(last_word);
        } catch (IOException e) {
            e.printStackTrace();
        }
        current_ptr += last_word.length;
        // NOTE: the last ptr in the list is pointer only to the end of the last word
        ptr.add(current_ptr);;
        num_rows += 1;
    }

    /**
     * append the given word to the end of the concatenated string with string encoding
     * @param last_word array of bytes
     */
    @Override
    public void append(String last_word)
    {
        try {
            stringCompression.encode(helper_string_writer, last_word);
            // NOTE: the last ptr in the list is pointer only to the end of the last word
            ptr.add(helper_string_writer.getBytePointer());
            num_rows += 1;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * append the given word to the end of the concatenated string with int encoding
     * @param last_word array of bytes
     */
    @Override
    public void append(ArrayList<Integer> last_word)
    {
        try {
            integerCompression.encode(helper_string_writer, last_word);
            // NOTE: the last ptr in the list is pointer only to the end of the last word
            ptr.add(helper_string_writer.getBytePointer());
            num_rows += 1;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void append(int n)
    {
        try {
            integerCompression.encode(helper_string_writer, n);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void finishAppending()
    {
        try {
            integerCompression.flushEncoding(helper_string_writer);
            ptr.add(helper_string_writer.getBytePointer());
            num_rows += 1;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void startAppending(){}

    /**
     * @param i index, represent the i'th word in the concatenated string
     * @return the i'th word in the concatenated string
     */
    @Override
    public byte[] read(int i)
    {
        int next_ptr = index_tools.byte_to_int(ptr_dict, (i + 1) * index_tools.INT_SIZE);
        int current_ptr = index_tools. byte_to_int(ptr_dict, i * index_tools.INT_SIZE);
        byte[] ans = new byte[next_ptr - current_ptr];
        try {
            // reader_string = new RandomAccessFile(path_string, "r");
            reader_string.seek(current_ptr);
            reader_string.read(ans);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return ans;
    }

    /**
     * @param i index, represent the i'th word in the concatenated string after decoding with string
     *          compression
     * @return the i'th word in the concatenated string
     */
    @Override
    public byte[] read(int i, String s)
    {
        //int next_ptr = tools.index_tools.byte_to_int(ptr_dict, (i + 1) * tools.index_tools.INT_SIZE);
        int current_ptr = index_tools. byte_to_int(ptr_dict, i * index_tools.INT_SIZE);
        try{
            if(inputStream != null)
            {
                return stringCompression.decodeString(helper_string_reader, 0, 0).getBytes(StandardCharsets.UTF_8);
            }
            return stringCompression.decodeString(helper_string_reader, current_ptr).getBytes(StandardCharsets.UTF_8);
        }catch (IOException e)
        {
            e.printStackTrace();
        }
        return null; // "";
    }

    /**
     * @param i index, represent the i'th word in the concatenated string after decoding with int  compression
     * @return the i'th word in the concatenated string
     */
    @Override
    public byte[] read(int i, int j)
    {
        int next_ptr = index_tools.byte_to_int(ptr_dict, (i + 1) * index_tools.INT_SIZE);
        int current_ptr = index_tools. byte_to_int(ptr_dict, i * index_tools.INT_SIZE);
        try{
            if(inputStream != null)
            {
                return ints_to_byte(integerCompression.decodeList(inputStream, current_ptr,
                        next_ptr, reader_string.length()));
            }
            return ints_to_byte(integerCompression.decodeList(reader_string, current_ptr, next_ptr));
        }catch (IOException e)
        {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * @param a an array list of integers
     * @return the list as byte[]
     */
    private byte[] ints_to_byte(ArrayList<Integer> a)
    {
        byte[] ans = new byte[a.size() * index_tools.INT_SIZE];
        for(int i = 0; i < a.size(); i++)
        {
            for(int j = 0; j < index_tools.INT_SIZE; j++)
                ans[j + i * index_tools.INT_SIZE] = index_tools.int_to_byte(a.get(i))[j];
        }
        return ans;
    }

    /**
     * @param st the String to search
     * @return the index of the string if exists in the index, else -1
     */
    @Override
    public int get_index_by_string(byte[] st) {
        int L = 0, R = num_rows - 1;
        int m;
        byte[] current_st;
        while (L <= R)
        {
            m = (L + R) / 2;
            // NOTE: we don't have dict of only bytes and this functions relevant only for reading the strings
            current_st = read(m, "");
            if (is_smaller(current_st, st))
                L = m + 1;
            else if (is_smaller(st, current_st))
                R = m - 1;
            else
                return m;
        }
        return NOT_EXISTS;
    }

    /**
     * @param st the String to search
     * @return the index of the string if exists in the index, else -1
     */
    @Override
    public int get_index_by_string(String st) {
        int L = 0, R = num_rows - 1;
        int m;
        String current_st;
        while (L <= R)
        {
            m = (L + R) / 2;
            current_st = new String(read(m, ""));
            int comp = current_st.compareTo(st);
            if (comp < 0)
                L = m + 1;
            else if (comp > 0)
                R = m - 1;
            else
                return m;
        }
        return NOT_EXISTS;
    }

    /**
     * saves the dict to disk
     */
    @Override
    public void save_to_disk()
    {
        if (saved)
            return;
        byte[] current_int = new byte[index_tools.INT_SIZE];
        ptr_dict = new byte[ptr.size() * index_tools.INT_SIZE];
        for (int i = 0; i < ptr.size(); i++)
        {
            index_tools.int_to_byte(current_int, ptr.get(i));
            for (int j = 0; j < index_tools.INT_SIZE; j++)
                ptr_dict[j + i * index_tools.INT_SIZE] = current_int[j];
        }
        try {
            writer_dict = new FileOutputStream(path_dict);
            writer_dict.write(ptr_dict);
            writer_dict.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        // save metadata
        try {
            index_tools.int_to_byte(current_int, num_rows);
            meta_data_rw = new RandomAccessFile(path_meta_data, "rw");
            meta_data_rw.write(current_int);
            meta_data_rw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        saved = true;
        ptr = null;
    }

    /**
     * loads the dict from disk
     */
    @Override
    public void load_from_disk()
    {
        if (loaded)
            return;
        // load metadata
        byte[] num_rows_temp = new byte[index_tools.INT_SIZE];
        try {
            meta_data_rw = new RandomAccessFile(path_meta_data, "rw");
            meta_data_rw.read(num_rows_temp);
        } catch (IOException e) {
            e.printStackTrace();
        }
        num_rows = index_tools.byte_to_int(num_rows_temp);
        // the last int is ptr to the end of the last word
        ptr_dict = new byte[(num_rows + 1) * index_tools.INT_SIZE];
        // read the dictionary
        try {
            if(reader_dict != null)
            {
                reader_dict.close();
            }
            reader_dict = new FileInputStream(path_dict);
            reader_dict.read(ptr_dict);
            reader_dict.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        loaded = true;
    }

    @Override
    public void close() throws IOException
    {
        super.close();
        helper_string_writer.close();
        helper_string_reader.close();
    }

    @Override
    public void flush() throws IOException {
        helper_string_writer.flush();
    }


    public void startReading(int i){
        int next_ptr = index_tools.byte_to_int(ptr_dict, (i + 1) * index_tools.INT_SIZE);
        int current_ptr = index_tools. byte_to_int(ptr_dict, i * index_tools.INT_SIZE);
        try{
            startReading(current_ptr, next_ptr, reader_string.length());
        }catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    private void startReading(int startPointer, int endPointer, long length){
        int maxPointer = (int) Math.min(length, endPointer);
        readOneFromString = new InputStreamHelper(inputStream, maxPointer - startPointer);
        integerCompression.startReading(readOneFromString);
    }

    public int readNext()
    {
        return integerCompression.getNext(readOneFromString);
    }

}
