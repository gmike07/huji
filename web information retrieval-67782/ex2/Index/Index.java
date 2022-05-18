package Index;

import CompressionV2.AbstractIntegerCompression;
import CompressionV2.GammaCompression;
import CompressionV2.InputStreamHelper;
import CompressionV2.OutputStreamHelper;
import Dictionary.ConcatenatedStringDict;
import Dictionary.DictOutputType;
import tools.index_tools;

import java.io.*;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;

import static Dictionary.ConcatenatedStringDict.NOT_EXISTS;

public class Index
{
    //the name of the index
    protected String name;
    //the directory we create all the files in
    protected String dir;
    //the path to the index content
    protected String path;


    //should we compress the data
    private boolean compressData = false;
    //how to compress the data
    private AbstractIntegerCompression integerCompression;
    // reader and writer of the index
    private RandomAccessFile index_rw;

    // for each field keep the first index where to read
    private HashMap<String, Integer> fields_first_index;
    private HashMap<String, Integer> fields_size;
    private HashMap<String, ConcatenatedStringDict> dictionaries;

    // the size of each row in the index in bytes.
    private int row_size;
    // the amount of rows in the index
    private int num_rows;

    // the values in the index
    // relevant when building the dictionary
    private ArrayList<byte[]> temp_index;
    // relevant when reading from the dictionary
    protected byte[] index;

    // relevant for building the index
    private byte[] current_row;

    private boolean autoWrite = false;
    private OutputStream writerFields = null;

    private ArrayList<Integer> sortedIndexes = null;

    /**
     * @param p_name the path name
     * @param p_dir the path directory
     */
    public Index(String p_name, String p_dir)
    {
        this.name = p_name;
        this.dir = p_dir;
        path = get_path();
        fields_first_index = new HashMap<>();
        fields_size = new HashMap<>();
        dictionaries = new HashMap<>();
        row_size = 0;
        num_rows = 0;
        temp_index = new ArrayList<>();
        try {
            new File(path).createNewFile();
            index_rw = new RandomAccessFile(path, "rw");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String currentString = "";
    private int currentPointer = 0;
    /**
     * @param p_name the path name
     * @param p_dir the path directory
     * @param toCompressData should we compress the data
     * @param compression the compression to use
     */
    public Index(String p_name, String p_dir, boolean toCompressData, AbstractIntegerCompression compression)
    {
        this(p_name, p_dir);
        compressData = toCompressData;
        integerCompression = compression;
    }

    private OutputStreamHelper helperWriterFields;
    /**
     * @param p_name the path name
     * @param p_dir the path directory
     * @param toCompressData should we compress the data
     * @param compression the compression to use
     */
    public Index(String p_name, String p_dir, boolean toCompressData,
                 AbstractIntegerCompression compression, boolean _autoWrite)
    {
        this(p_name, p_dir);
        compressData = toCompressData;
        integerCompression = compression;
        autoWrite = _autoWrite;
        try {
            if(autoWrite)
            {
                writerFields = new BufferedOutputStream(new FileOutputStream(index_rw.getFD()), 16384);
                helperWriterFields = new OutputStreamHelper(writerFields);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * adds a field and his size to the index
     * @param field_name the field name
     * @param size the field size
     */
    public void add_field(String field_name, int size)
    {
        fields_first_index.put(field_name, row_size);
        fields_size.put(field_name, size);
        row_size += size;
    }

    /**
     * adds a dictionary under name
     * @param name the name of the dictionary
     * @param dict the dictionary to add
     */
    public void add_dictionary(String name, ConcatenatedStringDict dict)
    {
        dictionaries.put(name, dict);
    }


    /**
     * creates a new row
     */
    public void new_row()
    {
        if(compressData && sortedIndexes == null)
        {
            sortedIndexes = new ArrayList<>(fields_first_index.values());
            sortedIndexes.add(row_size);
            sortedIndexes.sort(Integer::compareTo);
        }
        current_row = new byte[row_size];
    }

    /**
     * update a field in the current row
     * @param field_name the field to update
     * @param val the value of the field
     */
    public void update_field_in_row(String field_name, byte[] val)
    {
        int first_index = fields_first_index.get(field_name);
        int size = fields_size.get(field_name);
        for (int i = 0; i  < size; i++)
            current_row[first_index + i] = val[i];
    }

    /**
     * update the structure after finishing a row
     */
    public void finish_row()
    {
        if(autoWrite)
        {
            try{
                if(compressData)
                {
                    //TODO: handle compression
                    for(int j = 0; j < sortedIndexes.size() - 1; j++)
                    {
                        byte[] b = new byte[sortedIndexes.get(j + 1) - sortedIndexes.get(j)];
                        System.arraycopy(current_row, sortedIndexes.get(j), b, 0, b.length);
                        writerFields.write(index_tools.byte_to_int(b) + 1);
                    }
                    //for field in fields: compress(writerFields, get_field() + 1)
                }
                else {
                    writerFields.write(current_row);
                }
            }catch (IOException e)
            {
                e.printStackTrace();
            }
        }
        else
        {
            temp_index.add(current_row);
        }
        num_rows++;
    }

    /**
     * // ! not relevant function
     * adds the row the the index
     * @param row the row to add
     */
    public void append_row(byte[] row)
    {
        // ! maybe check row.length == row_size
        temp_index.add(row);
        num_rows++;
    }

    /**
     * saves the dict to disk
     */
    public void save_to_disk()
    {
        for (ConcatenatedStringDict dict: dictionaries.values())
            dict.save_to_disk();

        if(!autoWrite) {
            index = new byte[row_size * num_rows];
            for (int i = 0; i < num_rows; i++)
                for (int j = 0; j < row_size; j++)
                    index[j + i * row_size] = temp_index.get(i)[j];
        }

        try {
            if(autoWrite)
            {
                if(compressData)
                {
                    integerCompression.flushEncoding(helperWriterFields);
                }
                helperWriterFields.close();
                writerFields.close();
            }
            else if(compressData)
            {
                writeEncodedData();
            }
            else
            {
                index_rw.write(index);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        // save row_size and num_rows
        String meta_path = get_meta_path();
        byte[] current_int = new byte[index_tools.INT_SIZE];
        FileOutputStream writer;
        try {
//            new File(meta_path).createNewFile();
            writer = new FileOutputStream(meta_path);
            index_tools.int_to_byte(current_int, row_size);
            writer.write(current_int);
            index_tools.int_to_byte(current_int, num_rows);
            writer.write(current_int);
            writer.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * loads the dict from disk
     */
    public void load_from_disk()
    {
        // load meta data
        String meta_path = get_meta_path();
//        RandomAccessFile reader;
        FileInputStream reader;
        byte[] current_int = new byte[4];
        try {
            reader = new FileInputStream(meta_path);
            reader.read(current_int);
            row_size = index_tools.byte_to_int(current_int);
            reader.read(current_int);
            num_rows = index_tools.byte_to_int(current_int);
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        // load the index
        index = new byte[row_size * num_rows];
        try {
            if(compressData)
            {
                decodeData(index, row_size);
            }
            else
            {
                index_rw.read(index);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        for (ConcatenatedStringDict dict: dictionaries.values())
            dict.load_from_disk();
    }

    /**
     * @return path to the meta data of the index
     */
    private String get_meta_path()
    {
        return dir + File.separatorChar + name + "_index_meta_data.ind";
    }

    /**
     * @param field_name the field name we want to get from the dictionary
     * @param row_number the row we want to get
     * @return the field in the row number place
     */
    public byte[] get_field(String field_name, int row_number)
    {
        if (row_number >= num_rows || row_number < 0)
        {
            return null;
        }
        int first = fields_first_index.get(field_name);
        int size = fields_size.get(field_name);
        return get_sub_array(index, first + row_size * row_number, size);
    }

    /**
     * @param field_name the field name we want to get from the dictionary
     *                   assuming the rows of the dictionary synced with
     *                   the rows of the index
     * @param i the row we want to get
     * @return the field in the i'th place
     */
    public byte[] get_synced_dict_field(String field_name, int i)
    {
        ConcatenatedStringDict dict = dictionaries.get(field_name);
        if (dict.get_dict_type() == DictOutputType.ByteArray_out)
        {
            return dict.read(i);
        }
        else if (dict.get_dict_type() == DictOutputType.String_out)
        {
            return dict.read(i, "");
        }
        return dict.read(i, 0);
    }

    /**
     * @param field_name the field name we want to get from the dictionary
     * @param i the row we want to get
     * @return the field in the i'th place
     */
    public byte[] get_dict_field(String field_name, int i)
    {
        ConcatenatedStringDict dict = dictionaries.get(field_name);
        int ind = index_tools.byte_to_int(get_field(field_name, i));
        if (dict.get_dict_type() == DictOutputType.ByteArray_out)
        {
            return dict.read(ind);
        }
        else if (dict.get_dict_type() == DictOutputType.String_out)
        {
            return dict.read(ind, "");
        }
        return dict.read(ind, 0);
    }


    /**
     * @param dict_name the dictionary to search the index with
     * @param field_name the field we want to get from the index
     * @param word_in_dict the word to search in the dictionary
     * @return the byte[] of the wanted data
     */
    public byte[] get_field_by_dict(String dict_name, String field_name, byte[] word_in_dict)
    {
        ConcatenatedStringDict dict = dictionaries.get(dict_name);
        int i = dict.get_index_by_string(word_in_dict);
        if (i == NOT_EXISTS)
        {
            return null;
        }
        return get_field(field_name, i);
    }

    /**
     * @param dict_name the dictionary to search the index with
     * @param field_name the field we want to get from the dict, assuming
     *                   the dictionary's rows synced with the rows
     *                   of the index
     * @param word_in_dict the word to search in the dictionary
     * @return the byte[] of the wanted data
     */
    public byte[] get_synced_dict_field_by_dict(String dict_name, String field_name, byte[] word_in_dict)
    {
        ConcatenatedStringDict dict = dictionaries.get(dict_name);
        int i = dict.get_index_by_string(word_in_dict);
        if (i == NOT_EXISTS)
        {
            return null;
        }
        return get_synced_dict_field(field_name, i);
    }

//    public Enumeration<Integer> get_list_by_dict(String dict_name, String field_name, byte[] word_in_dict)
//    {
//        ConcatenatedStringDict dict = dictionaries.get(dict_name);
//        int i = dict.get_index_by_string(word_in_dict);
//        ConcatenatedStringDict dict = dictionaries.get(field_name);
//    }

    /**
     * @param dict_name the dictionary to search the index with
     * @param field_name the field we want to get from the dict
     * @param word_in_dict the word to search in the dictionary
     * @return the byte[] of the wanted data
     */
    public byte[] get_dict_field_by_dict(String dict_name, String field_name, byte[] word_in_dict)
    {
        ConcatenatedStringDict dict = dictionaries.get(dict_name);
        int i = dict.get_index_by_string(word_in_dict);
        if (i == NOT_EXISTS)
        {
            return null;
        }
        return get_dict_field(field_name, i);
    }

    /**
     * @param a an array of bytes
     * @param first_inedx the first index from which to cipy
     * @param size the size to copy
     * @return return a[first_index: first_index + size]
     */
    private byte[] get_sub_array(byte[] a, int first_inedx, int size)
    {
        byte[] sub_array = new byte[size];
        for(int i = 0; i < size; i++)
            sub_array[i] = a[first_inedx + i];
        return sub_array;
    }

    /**
     * @return path to the index content
     */
    private String get_path()
    {
        return dir + File.separatorChar + name + ".index_content";
    }

    /**
     * encodes indexes to file and stores it in index_rw
     */
    private void writeEncodedData()
    {
        ArrayList<Integer> indexes = new ArrayList<>(fields_first_index.values());
        indexes.add(row_size);
        indexes.sort(Integer::compareTo);
        ArrayList<Integer> lst = new ArrayList<>();
        for(int i = 0; i < num_rows; i++)
        {
            for(int j = 0; j < indexes.size() - 1; j++)
            {
                byte[] b = new byte[indexes.get(j + 1) - indexes.get(j)];
                System.arraycopy(temp_index.get(i), indexes.get(j), b, 0, b.length);
                lst.add(index_tools.byte_to_int(b) + 1);
            }
        }
        try{
            integerCompression.encode(new OutputStreamHelper(new FileOutputStream(path)), lst);
        }catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    /**
     * @param bytes gets an array to write to
     * @param row_size the row size of each term
     * reads index_rw and writes everything to bytes
     */
    private void decodeData(byte[] bytes, int row_size)
    {
        ArrayList<Integer> indexes = new ArrayList<>(fields_first_index.values());
        indexes.add(row_size);
        indexes.sort(Integer::compareTo);

        int currentIndex = 0;
        int currField = 0;
        InputStreamHelper h = null;
        try
        {
            h = new InputStreamHelper(new BufferedInputStream(new FileInputStream(index_rw.getFD())));
        } catch (IOException e)
        {
            e.printStackTrace();
        }
        integerCompression.startReading(h);
        int next = integerCompression.getNext(h);
        while (next != -1) {
            byte[] num = index_tools.int_to_byte(next - 1);
            int fieldSize = indexes.get(currField + 1) - indexes.get(currField);
            System.arraycopy(num, 0, bytes, currentIndex, fieldSize);
            currentIndex += fieldSize;
            currField = (currField + 1) % (indexes.size() - 2);
            next = integerCompression.getNext(h);
        }
    }


    public void initPointer(String dictName, boolean writeString)
    {
        currentPointer = 0;
        if(writeString)
        {
            currentString = new String(get_synced_dict_field(dictName, currentPointer));
        }
    }

    public void advancePointer(String dictName, boolean writeString)
    {
        currentPointer++;
        if(writeString && !reachedEnd(dictName))
        {
            currentString = new String(get_synced_dict_field(dictName, currentPointer));
        }
    }

    public boolean reachedEnd(String dictName)
    {
        return currentPointer >= getDictionary(dictName).getNumRows();
    }

    public String getCurrentString()
    {
        return currentString;
    }


    public ConcatenatedStringDict getDictionary(String name)
    {
        return dictionaries.get(name);
    }


    public int getCurrentPointer()
    {
        return currentPointer;
    }

    public int getNumRows(){
        return num_rows;
    }

    public void close() throws IOException {
        if(writerFields != null)
        {
            writerFields.close();
        }
        index_rw.close();
        for(ConcatenatedStringDict dict : dictionaries.values())
        {
            if(!dict.isClosed())
            {
                dict.close();
            }
        }
    }
}
