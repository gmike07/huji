package CompressionV2;



import java.io.IOException;
import java.io.InputStream;
import java.io.RandomAccessFile;
import java.util.ArrayList;

public abstract class AbstractBitIntegerCompression extends AbstractIntegerCompression {
    //remember bit offset in current byte
    private int offsetBit = 0;

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
     * @return if there are more bits to read
     */
    protected boolean hasMoreToRead()
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
     * writes everything to the stream and saves it
     * @param outStream the stream to flush to
     * @throws IOException if failed to write
     */
    public void flushEncoding(OutputStreamHelper outStream) throws IOException {
        while(offsetBit % 8 != 0)
        {
            writeBit(outStream, 1);
        }
        super.flushEncoding(outStream);
    }

    /**
     * @param c another bit compression
     * change the compression to point to the other compression location
     */
    protected void moveToPosition(AbstractBitIntegerCompression c)
    {
        offsetBit = c.offsetBit;
        pointerByte = c.pointerByte;
        currentByte = c.currentByte;
    }

    /**
     * @param inStream the stream to read from
     * @param startPointer the point to start reading from
     * @param endPointer the point to end reading
     * @return the list of integers written from start to end in inStream
     * @throws IOException if failed to read
     */
    @Override
    public ArrayList<Integer> decodeList(RandomAccessFile inStream, int startPointer, int endPointer) throws IOException {
        ArrayList<Integer> lst = new ArrayList<>();
        InputStreamHelper inputStreamHelper = new InputStreamHelper(inStream);
        inputStreamHelper.seek(startPointer);
        offsetBit = 0;
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
        if(inStream.getFilePointer() == endPointer + 1 && offsetBit == 0)
        {
            lst.add(value);
        }
        return lst;
    }


    @Override
    public ArrayList<Integer> decode(InputStreamHelper inputStream) throws IOException
    {
        offsetBit = 0;
        return super.decode(inputStream);
    }

    @Override
    public byte advanceByte(InputStreamHelper inStream) throws IOException
    {
        offsetBit = 0;
        return super.advanceByte(inStream);
    }
}
