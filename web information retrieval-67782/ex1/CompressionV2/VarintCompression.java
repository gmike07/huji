package CompressionV2;

import java.io.IOException;

public class VarintCompression extends AbstractIntegerCompression {
    /**
     * encodes the number to the stream
     * @param outStream the stream to write the encoded to
     * @param n the number to encode
     * @throws IOException if failed to write
     */
    @Override
    public void encode(OutputStreamHelper outStream, int n) throws IOException {
        int largestBit = findLargestBit(n) + 1;
        largestBit = largestBit % 7 == 0 ? largestBit : largestBit + (7 - largestBit % 7);
        for(int i = largestBit; i > 0; i -= 7)
        {
            byte b = 0;
            if(i > 7)
            {
                b |= ((n >> (i - 7)) & 127);
            }
            else
            {
                b |= 128 | (n & 127);
            }
            writeByte(outStream, b);
        }
    }

    /**
     * @param inputStream an encoded stream to decode
     * @return the next number encoded in the stream
     * @throws IOException if failed to read
     */
    @Override
    public int decodeNumber(InputStreamHelper inputStream) throws IOException {
        int n = 0;
        byte b = advanceByte(inputStream);
        while(b >= 0)
        {
            n = 128 * n + b;
            b = advanceByte(inputStream);
        }
        n = 128 * n + (b & 127);
        return n;
    }
}
