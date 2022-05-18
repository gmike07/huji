package Dictionary;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;

import CompressionV2.*;
import tools.index_tools;

public class BlockingDict extends ConcatenatedStringDict
{
    //stores ptrs while writing
    private ArrayList<Integer> ptr;
    //stores ptrs after pre processing
    private byte[] ptr_dict;
    //stores length while writing
    private ArrayList<byte[]> lengths;
    //stores lengths after pre processing
    private byte[] length_dict;
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
    //size of block
    private int K;
    //how many bytes it takes to store length
    private static final int BYTE_LENGTH_SIZE = 2;
    private int curr_pointer;

    /**
     * @param dir the directory of the saved dict
     * @param field_name the field name of the dict (what it stores)
     * @param for_writing do we write the dict or read it
     * @param type what does the dict return
     * @param int_comp int compression
     * @param str_comp string compression
     * @param k: the size of block
     * @throws FileNotFoundException if file not found
     */
    public BlockingDict(String dir, String field_name, boolean for_writing, DictOutputType type,
                      AbstractIntegerCompression int_comp, AbstractStringCompression str_comp, int k) throws FileNotFoundException {
        super(dir, field_name, for_writing, type);
        ptr = new ArrayList<>();
        lengths = new ArrayList<>();
        helper_string_writer = new OutputStreamHelper(writer_string);
        helper_string_reader = new InputStreamHelper(reader_string);
        stringCompression = str_comp;
        integerCompression = int_comp;
        current_ptr = 0;
        ptr.add(current_ptr);
        K = k;
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
        num_rows += 1;
        if(num_rows % K == 0)
        {
            ptr.add(current_ptr);
        }else
        {
            lengths.add(index_tools.int_to_byte(last_word.length));
        }
    }

    /**
     * append the given word to the end of the concatenated string with string encoding
     * @param last_word array of bytes
     */
    @Override
    public void append(String last_word)
    {
        try {
            int curr_pointer = helper_string_writer.getBytePointer();
            stringCompression.encode(helper_string_writer, last_word);
            // NOTE: the last ptr in the list is pointer only to the end of the last word
            num_rows += 1;
            if(num_rows % K == 0)
            {
                ptr.add(helper_string_writer.getBytePointer());
            }
            else
            {
                byte[] bytes =
                        index_tools.int_to_byte(helper_string_writer.getBytePointer() - curr_pointer);
                lengths.add(bytes);
            }
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
            int curr_pointer = helper_string_writer.getBytePointer();
            integerCompression.encode(helper_string_writer, last_word);
            // NOTE: the last ptr in the list is pointer only to the end of the last word
            num_rows += 1;
            if(num_rows % K == 0)
            {
                ptr.add(helper_string_writer.getBytePointer());
            }
            else
            {
                byte[] bytes =
                        index_tools.int_to_byte(helper_string_writer.getBytePointer() - curr_pointer);
                lengths.add(bytes);
            }
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
            num_rows += 1;
            if(num_rows % K == 0)
            {
                ptr.add(helper_string_writer.getBytePointer());
            }
            else
            {
                byte[] bytes =
                        index_tools.int_to_byte(helper_string_writer.getBytePointer() - curr_pointer);
                lengths.add(bytes);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void startAppending(){curr_pointer = helper_string_writer.getBytePointer();}

    /**
     * @param i get the i'th index
     * @return the i'th pointer in the file
     */
    private int get_current_ptr(int i)
    {
        int block = i / K;
        int ptr_ = index_tools. byte_to_int(ptr_dict, block * index_tools.INT_SIZE);
        byte[] arr = new byte[BYTE_LENGTH_SIZE];
        for(int offset_helper = 0; offset_helper < i % K; offset_helper++)
        {
            for(int j = 0; j < BYTE_LENGTH_SIZE; j++)
            {
                arr[j] = length_dict[(block * (K - 1) + offset_helper) * BYTE_LENGTH_SIZE + j];
            }
            ptr_ += index_tools.byte_to_int(arr);
        }
        return ptr_;
    }
    /**
     * @param i index, represent the i'th word in the concatenated string
     * @return the i'th word in the concatenated string
     */
    @Override
    public byte[] read(int i)
    {
        int next_ptr = get_current_ptr(i + 1);
        int current_ptr = get_current_ptr(i);
        byte[] ans = new byte[next_ptr - current_ptr];
        try {
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
        //int next_ptr = get_current_ptr(i + 1);
        int current_ptr = get_current_ptr(i);
        try{
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
        int next_ptr = get_current_ptr(i + 1);
        int current_ptr = get_current_ptr(i);
        try{
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
     * @param st the bytes to search
     * @return the index of the string represented by st if exists in the index, else -1
     */
    @Override
    public int get_index_by_string(byte[] st) {
        int block = get_index_by_string_helper(st) * K;
        String s = new String(st);
        for(int i = 0; i < K; i++)
        {
            if(s.equals(new String(read(block + i, ""))))
            {
                return block + i;
            }
        }
        return NOT_EXISTS;
    }

    /**
     * @param st the bytes to search
     * @return the index of block of the string represented by st if exists in the index
     */
    private int get_index_by_string_helper(byte[] st) {
        int L = 0, R = ptr_dict.length / index_tools.INT_SIZE - 1;
        int m = 0;
        byte[] current_st;
        while (L <= R)
        {
            m = (L + R) / 2;
            // NOTE: we don't have dict of only bytes and this functions relevant only for reading the strings
            current_st = read(m * K, "");
            if (is_smaller(current_st, st))
                L = m + 1;
            else if (is_smaller(st, current_st))
                R = m - 1;
            else
                return m;
        }
        if(L * index_tools.INT_SIZE >= ptr_dict.length)
        {
            return L - 1;
        }
        current_st = read(L * K, "");
        if(is_smaller(current_st, st))
        {
            return R;
        }
        current_st = read(R * K, "");
        if(is_smaller(st, current_st))
        {
            return L;
        }
        return R;
    }

    /**
     * @param st the String to search
     * @return the index of the string if exists in the index, else -1
     */
    @Override
    public int get_index_by_string(String st) {
        int block = get_index_by_string_helper(st) * K;
        for(int i = 0; i < K; i++)
        {
            if(st.equals(new String(read(block + i, ""))))
            {
                return block + i;
            }
        }
        return NOT_EXISTS;
    }

    /**
     * @param st the String to search
     * @return the index of block of the string if exists in the index
     */
    private int get_index_by_string_helper(String st) {
        int L = 0, R = ptr_dict.length /  index_tools.INT_SIZE - 1;
        int m = 0;
        String current_st;
        while (L <= R)
        {
            m = (L + R) / 2;
            current_st = new String(read(m*K, ""));
            int comp = current_st.compareTo(st);
            if (comp < 0)
                L = m + 1;
            else if (comp > 0)
                R = m - 1;
            else
                return m;
        }
        if(L * index_tools.INT_SIZE >= ptr_dict.length)
        {
            return L - 1;
        }
        current_st = new String(read(L * K, ""));
        if(current_st.compareTo(st) <= 0)
        {
            return R;
        }
        current_st = new String(read(R * K, ""));
        if(current_st.compareTo(st) <= 0)
        {
            return L;
        }
        return R;
    }

    /**
     * saves the dict to disk
     */
    @Override
    public void save_to_disk()
    {
        if (saved)
            return;
        ptr_dict = new byte[ptr.size() * index_tools.INT_SIZE];
        byte[] current_int = new byte[index_tools.INT_SIZE];
        for (int i = 0; i < ptr.size(); i++)
        {
            index_tools.int_to_byte(current_int, ptr.get(i));
            for (int j = 0; j < index_tools.INT_SIZE; j++)
                ptr_dict[j + i * index_tools.INT_SIZE] = current_int[j];
        }
        length_dict = new byte[lengths.size() * BYTE_LENGTH_SIZE];
        for(int i = 0; i < lengths.size(); i++)
        {
            for(int j = 0; j < BYTE_LENGTH_SIZE; j++)
            {
                length_dict[i * BYTE_LENGTH_SIZE + j] = lengths.get(i)[j];
            }
        }
        try {
            if(writer_dict != null)
            {
                writer_dict.close();
            }
            writer_dict = new FileOutputStream(path_dict);
            writer_dict.write(ptr_dict);
            writer_dict.write(length_dict);
            writer_dict.flush();
            writer_dict.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // save metadata
        try {
            index_tools.int_to_byte(current_int, ptr.size());
            meta_data_rw = new RandomAccessFile(path_meta_data, "rw");
            meta_data_rw.write(current_int);
            index_tools.int_to_byte(current_int, lengths.size() * BYTE_LENGTH_SIZE);
            meta_data_rw.write(current_int);
            index_tools.int_to_byte(current_int, num_rows);
            meta_data_rw.write(current_int);
            meta_data_rw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        saved = true;

        ptr = null;
        lengths = null;
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
        byte[] num_rows_temp2 = new byte[index_tools.INT_SIZE];
        byte[] num_rows_temp3 = new byte[index_tools.INT_SIZE];
        try {
            meta_data_rw = new RandomAccessFile(path_meta_data, "rw");
            meta_data_rw.read(num_rows_temp);
            meta_data_rw.read(num_rows_temp2);
            meta_data_rw.read(num_rows_temp3);
        } catch (IOException e) {
            e.printStackTrace();
        }
        int num_rows_ptr = index_tools.byte_to_int(num_rows_temp);
        ptr_dict = new byte[num_rows_ptr * index_tools.INT_SIZE];
        int num_rows_lengths = index_tools.byte_to_int(num_rows_temp2);
        length_dict = new byte[num_rows_lengths];
        num_rows = index_tools.byte_to_int(num_rows_temp3);
        // read the dictionary
        try {
            if(reader_dict != null)
            {
                reader_dict.close();
            }
            reader_dict = new FileInputStream(path_dict);
            reader_dict.read(ptr_dict);
            reader_dict.read(length_dict);
        } catch (IOException e) {
            e.printStackTrace();
        }
        loaded = true;
    }
}
