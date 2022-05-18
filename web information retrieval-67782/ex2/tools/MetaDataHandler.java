package tools;

import java.io.*;


import static tools.index_tools.*;

public class MetaDataHandler
{
    public String path;
    public static final String SUFFIX = ".metadata";
    protected boolean for_writing;
    public int num_fields;

    protected byte[] current_val = new byte[INT_SIZE];

    protected FileOutputStream writer;
    protected FileInputStream reader;

    public MetaDataHandler(String path, boolean for_writing){
        this.path = path;
        this.for_writing = for_writing;
        try
        {
            if (for_writing)
            {
                writer = new FileOutputStream(this.path);
            }
            else
            {
                reader = new FileInputStream(this.path);
            }
        }
        catch (FileNotFoundException e)
        {
            e.printStackTrace();
        }

    }

    /**
     * write the given value to the metadata file
     * @param val integer;
     */
    public void add_field(int val)
    {
        try {
            writer.write(int_to_byte(val));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * @return the next integer to read from the metadata.
     * note: it is the responsibility of the user to know when to not read
     * and understand the meaning of the value
     */
    public int read_next_field()
    {
        try {
            reader.read(current_val);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return byte_to_int(current_val);
    }

    /**
     * release the streams.
     */
    public void release()
    {
        try
        {
            if (for_writing)
                writer.close();
            else
                reader.close();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }



}
