package CompressionV2;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;

public abstract class AbstractStringCompression {
    //the stop char (to know that the string is done)
    private static char STOP_CHAR = ';';
    //an offset bit of the current byte
    private int offsetBit = 0;
    //the current byte to read \ write
    private int currentByte = 0;

    private int pointerByte = 0;

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
     * writes the current bit to the current byte
     * @param outputStream the stream helper to write the bit into
     * @param bit the bit to write (0 or 1)
     * @throws IOException if failed to write
     */
    protected void writeBit(OutputStreamHelper outputStream, int bit) throws IOException {
        if(bit == 1)
        {
            currentByte |= (bit << (7 - offsetBit));
        }
        offsetBit++;
        if(7 < offsetBit)
        {
            writeByte(outputStream, currentByte);
            currentByte = 0;
            offsetBit = 0;
        }
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
        offsetBit = 0;
        pointerByte++;
        return b;
    }

    /**
     * @return if there are more bits to read
     */
    public boolean hasMoreToRead()
    {
        return currentByte != -1 || offsetBit <= 7;
    }

    /**
     * @param inStream the stream to rad from
     * @return the next bit in the stream
     * @throws IOException if failed to read
     */
    public int advanceBit(InputStreamHelper inStream) throws IOException
    {
        int bit = ((currentByte >> (7 - offsetBit)) & 1);
        offsetBit++;
        if((7 < offsetBit) && (currentByte != -1))
        {
            offsetBit = 0;
            advanceByte(inStream);
        }
        return bit;
    }

    /**
     * encodes the string to the stream
     * @param stream the stream to write to
     * @param s the string to encode
     * @throws IOException if failed to write
     */
    public void encode(OutputStreamHelper stream, String s) throws IOException
    {
        for(int i = 0; i < s.length(); i++)
        {
            encodeChar(stream, s.charAt(i));
        }
        encodeChar(stream, STOP_CHAR);
        flushEncoding(stream);
    }

    /**
     * encodes the string to the stream
     * @param stream the stream to write to
     * @param s the string to encode
     * @throws IOException if failed to write
     */
    public void encode(FileOutputStream stream, String s) throws IOException
    {
        encode(new OutputStreamHelper(stream), s);
    }

    /**
     * @param s the string to encode
     * @throws IOException if failed to write
     * @return the bytes of the encoded string
     */
    public byte[] encode(String s) throws IOException
    {
        OutputStreamHelper stream = new OutputStreamHelper();
        encode(stream, s);
        return stream.toByteArray();
    }

    /**
     * writes everything to the stream and saves it
     * @param outStream the stream to flush to
     * @throws IOException if failed to write
     */
    public void flushEncoding(OutputStreamHelper outStream) throws IOException {
        while(offsetBit % 8 != 0)
        {
            writeBit(outStream, 1);
        }
        //outStream.flush();
    }

    /**
     * encodes the char to the stream
     * @param stream the stream to write to
     * @param c the string to encode
     * @throws IOException if failed to write
     */
    public abstract void encodeChar(OutputStreamHelper stream, char c) throws IOException;

    /**
     * @param stream the stream to read from
     * @return the decoded char from the stream
     * @throws IOException if failed to read
     */
    public abstract char decodeChar(InputStreamHelper stream) throws IOException;

    /**
     * @param stream the stream to read from
     * @return the decoded string from the stream
     * @throws IOException if failed to read
     */
    public String decodeString(InputStreamHelper stream) throws IOException
    {
        advanceByte(stream);
        StringBuilder s = new StringBuilder();
        char c = decodeChar(stream);
        while(c != STOP_CHAR)
        {
            s.append(c);
            c = decodeChar(stream);
        }
        return s.toString();
    }

    /**
     * @param stream the stream to read from
     * @param readFirstByte should we read the first byte before starting to decode
     * @return the decoded string from the stream
     * @throws IOException if failed to read
     */
    public String decodeString(InputStreamHelper stream, boolean readFirstByte) throws IOException
    {
        if(readFirstByte)
        {
            advanceByte(stream);
        }
        StringBuilder s = new StringBuilder();
        char c = decodeChar(stream);
        while(c != STOP_CHAR)
        {
            s.append(c);
            c = decodeChar(stream);
        }
        return s.toString();
    }

    /**
     * @param stream the stream to read from
     * @param startPointer from where to start decoding
     * @return the decoded string from the stream
     * @throws IOException if failed to read
     */
    public String decodeString(InputStreamHelper stream, int startPointer) throws IOException
    {
        stream.seek(startPointer);
        advanceByte(stream);
        return decodeString(stream, false);
    }


    public String decodeString(InputStreamHelper stream, int startPointer, int endPointer) throws IOException
    {
        if(pointerByte == 0 || offsetBit != 0)
        {
            advanceByte(stream);
        }
        StringBuilder s = new StringBuilder();
        char c = decodeChar(stream);
        while(c != STOP_CHAR)
        {
            s.append(c);
            c = decodeChar(stream);
        }
        return s.toString();
    }


    /**
     * saves the data in dir
     * @param dir the dir to save in
     * @throws IOException if failed to write
     */
    public abstract void save(String dir) throws IOException;

    /**
     * loads the data in dir
     * @param dir the dir to load from
     * @throws IOException if failed to read
     */
    public abstract void load(String dir) throws IOException;


    public String decodeNChars(InputStreamHelper stream, int numChars) throws IOException
    {
        StringBuilder s = new StringBuilder();
        for(int i = 0; i < numChars; i++)
        {
            s.append(decodeChar(stream));
        }
        return s.toString();
    }
}
