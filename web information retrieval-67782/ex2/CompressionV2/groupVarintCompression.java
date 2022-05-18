package CompressionV2;

import java.io.IOException;
import java.util.ArrayList;


public class groupVarintCompression extends AbstractIntegerCompression {

    //stores the current length to decode with
    private int currentLenDecode;
    //the byte that stores the lengths to decode with
    private byte lengthsDecode;
    //bytes encoded
    private ArrayList<Byte> bytes;
    //byte containing lengths
    private byte lengthByteEncoded;
    //the number of byte encoded currently
    private int numLenEncoded;


    public groupVarintCompression()
    {
        currentLenDecode = 4;
        lengthsDecode = 0;
        bytes = new ArrayList<>();
        numLenEncoded = 0;
        lengthByteEncoded = 0;

    }

    /**
     * writes everything to the stream and saves it
     * @param outStream the stream to flush to
     * @throws IOException if failed to write
     */
    @Override
    public void flushEncoding(OutputStreamHelper outStream) throws IOException {
        if(numLenEncoded == 0)
        {
            return;
        }
        writeByte(outStream, lengthByteEncoded);
        for(byte b: bytes)
        {
            writeByte(outStream, b);
        }
        super.flushEncoding(outStream);
    }

    /**
     * encodes the number to the stream
     * @param outStream the stream to write the encoded to
     * @param n the number to encode
     * @throws IOException if failed to write
     */
    @Override
    public void encode(OutputStreamHelper outStream, int n) throws IOException {
        int largestBit = findLargestBit(n);
        largestBit += 1;
        largestBit = largestBit % 8 == 0 ? largestBit : largestBit + (8 - (largestBit % 8));
        for(int i = largestBit; i > 0; i -= 8)
        {
            if(i > 8)
            {
                bytes.add((byte) ((n >> (i - 8)) & 255));
            }
            else
            {
                bytes.add((byte) (n & 255));
            }
        }
        lengthByteEncoded |= (largestBit / 8 - 1) << (6 - 2 * numLenEncoded);
        numLenEncoded++;
        if(numLenEncoded == 4)
        {
            writeByte(outStream, lengthByteEncoded);
            lengthByteEncoded = 0;
            for(byte b: bytes)
            {
                writeByte(outStream, b);
            }
            bytes = new ArrayList<>();
            numLenEncoded = 0;
        }
    }

    /**
     * @param inputStream an encoded stream to decode
     * @return the next number encoded in the stream
     * @throws IOException if failed to read
     */
    @Override
    public int decodeNumber(InputStreamHelper inputStream) throws IOException {
        if(currentLenDecode == 4)
        {
            lengthsDecode = advanceByte(inputStream);
            currentLenDecode = 0;
        }
        int n = 0;
        int length = (lengthsDecode >> (2 * (3 - currentLenDecode))) & 3;
        for(int i = 0; i <= length; i++)
        {
            n = 256 * n + Byte.toUnsignedInt(advanceByte(inputStream));
        }
        currentLenDecode++;
        return n;
    }
}
