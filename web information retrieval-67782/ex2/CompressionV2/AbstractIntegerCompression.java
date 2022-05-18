package CompressionV2;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.Enumeration;

public abstract class AbstractIntegerCompression implements Enumeration<Integer>
{
    // the current byte to decode \ encode
    protected int currentByte = 0;
    // the current pointer in the file
    protected int pointerByte = 0;

    protected InputStreamHelper current_enumration;

    public void start_enumaration(RandomAccessFile inStream, int startPointer)
    {
        current_enumration = new InputStreamHelper(inStream);
        try {
            current_enumration.seek(startPointer);
        } catch (IOException e) {
            e.printStackTrace();
        }
        try
        {
            advanceByte(current_enumration);
        }catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    @Override
    public boolean hasMoreElements()
    {
        if (hasMoreToRead())
            return true;
        try {
            current_enumration.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return false;
    }

    @Override
    public Integer nextElement(){
        try {
            return decodeNumber(current_enumration);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return -1;
    }

    /**
     * @return the current pointer in the file
     */
    public int getPointerByte()
    {
        return pointerByte;
    }

    /**
     * @param n an integer
     * @return the place of the largest bit of 1 in n
     */
    protected int findLargestBit(int n)
    {
        for(int j = 31; j >= 0; j--)
        {
            if(((n >> j) & 1) == 1)
            {
                return j;
            }
        }
        return 0;
    }

    /**
     * writes the current byte to the stream
     * @param outputStream the stream helper to write the bit into
     * @param currentByte the byte to write
     * @throws IOException if failed to write
     */
    protected void writeByte(OutputStreamHelper outputStream, int currentByte) throws IOException {
        outputStream.write((byte) (currentByte & 255));
        pointerByte++;
    }

    /**
     * @return if there are more bytes to read
     */
    protected boolean hasMoreToRead()
    {
        return currentByte != -1;
    }

    /**
     * encodes the number to the stream
     * @param outStream the stream to write the encoded to
     * @param n the number to encode
     * @throws IOException if failed to write
     */
    public abstract void encode(OutputStreamHelper outStream, int n) throws IOException;

    /**
     * encodes the list to the stream
     * @param outStream the stream to write the encoded to
     * @param lst the numbers to encode
     * @throws IOException if failed to write
     */
    public void encode(OutputStreamHelper outStream, ArrayList<Integer> lst) throws IOException {
        for(int num: lst)
        {
            encode(outStream, num);
        }
        flushEncoding(outStream);
    }

    /**
     * @param lst the numbers to encode
     * @throws IOException if failed to write
     * @return the encoded bytes of the lst numbers
     */
    public byte[] encode(ArrayList<Integer> lst) throws IOException {
        OutputStreamHelper outStream = new OutputStreamHelper();
        for(int num: lst)
        {
            encode(outStream, num);
        }
        flushEncoding(outStream);
        return outStream.toByteArray();
    }

    /**
     * @param inStream the stream to read from
     * @return the next byte in the stream
     * @throws IOException if failed to read
     */
    protected byte advanceByte(InputStreamHelper inStream) throws IOException
    {
        byte b = (byte) (currentByte & 255);
        currentByte = inStream.read();
        if(currentByte != -1)
        {
            pointerByte++;
        }
        return b;
    }

    /**
     * @param inputStream an encoded stream to decode
     * @return the next number encoded in the stream
     * @throws IOException if failed to read
     */
    public abstract int decodeNumber(InputStreamHelper inputStream) throws IOException;

    /**
     * @param inputStream an encoded stream to decode
     * @return an array list of integers of the encoded stream
     * @throws IOException if failed to read
     */
    public ArrayList<Integer> decode(InputStreamHelper inputStream) throws IOException
    {
        ArrayList<Integer> bytes = new ArrayList<>();
        advanceByte(inputStream);
        while(hasMoreToRead())
        {
            try{
                int n = decodeNumber(inputStream);
                bytes.add(n);
            }catch(Exception e)
            {
                return bytes;
            }
        }
        return bytes;
    }

    /**
     * @param bytes an array of bytes of integers to decode
     * @return an array list of integers of the encoded bytes
     * @throws IOException if failed to read
     */
    public ArrayList<Integer> decode(byte[] bytes) throws IOException
    {
        return decode(new InputStreamHelper(new ByteArrayInputStream(bytes)));
    }

    /**
     * @param inStream the stream to read from
     * @param startPointer the point to start reading from
     * @param endPointer the point to end reading
     * @return the list of integers written from start to end in inStream
     * @throws IOException if failed to read
     */
    public ArrayList<Integer> decodeList(RandomAccessFile inStream, int startPointer, int endPointer) throws IOException {
        ArrayList<Integer> lst = new ArrayList<>();
        InputStreamHelper inputStreamHelper = new InputStreamHelper(inStream);
        inputStreamHelper.seek(startPointer);
        if(inStream.length() <= endPointer)
        {
            return decode(inputStreamHelper);
        }
        advanceByte(inputStreamHelper);
        int value = decodeNumber(inputStreamHelper);
        while(inStream.getFilePointer() <= endPointer)
        {
            lst.add(value);
            value = decodeNumber(inputStreamHelper);
        }
        lst.add(value);
        return lst;
    }


    public ArrayList<Integer> decodeList(InputStream inStream, int startPointer, int endPointer,
                                         long length) throws IOException {

        int maxPointer = (int) Math.min(length, endPointer);
//        byte[] bytes = new byte[(int)(maxPointer - startPointer)];
//        inStream.read(bytes);
        return decode(new InputStreamHelper(inStream, maxPointer - startPointer));
    }

    /**
     * writes everything to the stream and saves it
     * @param outStream the stream to flush to
     * @throws IOException if failed to write
     */
    public void flushEncoding(OutputStreamHelper outStream) throws IOException {
        //outStream.flush();
    }

    public void startReading(InputStreamHelper h)
    {
        try
        {
            advanceByte(h);
        }catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    public int getNext(InputStreamHelper h)
    {
        if(!hasMoreToRead())
        {
            return -1;
        }
        try
        {
            return decodeNumber(h);
        }catch (IOException e)
        {
            return -1;
        }
    }
}
