package CompressionV2;


import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;

public class OutputStreamHelper {
    // an array list of bytes to store the written bytes
    private ArrayList<Byte> bytes = null;
    // a file output stream
    private OutputStream fileOutputStream = null;
    // the current pointer
    private int bytePointer = 0;

    /**
     * @param fileOutputStream an output stream
     */
    public OutputStreamHelper(OutputStream fileOutputStream)
    {
        this.fileOutputStream = fileOutputStream;
    }

    public OutputStreamHelper()
    {
        this.bytes = new ArrayList<>();
    }

    /**
     * writes the current byte
     * @param b the byte to write
     * @throws IOException if failed to write
     */
    public void write(byte b) throws IOException {
        bytePointer++;
        if(fileOutputStream != null)
        {
            fileOutputStream.write(b);
        }
        else
        {
            bytes.add(b);
        }
    }

    /**
     * @return the array list of bytes
     */
    public ArrayList<Byte> getBytes() {return bytes;}

    /**
     * flushes the outputStream if open
     * @throws IOException if failed to flush
     */
    public void flush() throws IOException {
        if(fileOutputStream != null)
        {
            fileOutputStream.flush();
        }
    }

    /**
     * closes the outputStream if open
     * @throws IOException if failed to close
     */
    public void close() throws IOException {
        if(fileOutputStream != null)
        {
            fileOutputStream.close();
        }
    }

    /**
     * @return the array list as byte[]
     */
    public byte[] toByteArray()
    {
        byte[] bytesArr = new byte[bytes.size()];
        for(int i = 0; i < bytes.size(); i++)
        {
            bytesArr[i] = bytes.get(i);
        }
        bytes.clear();
        return bytesArr;
    }

    /**
     * @return the current bytePointer
     */
    public int getBytePointer()
    {
        return bytePointer;
    }
}
