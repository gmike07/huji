package CompressionV2;

import java.io.IOException;

public class lengthVarintCompression extends AbstractIntegerCompression {

    /**
     * encodes the number to the stream
     * @param outStream the stream to write the encoded to
     * @param n the number to encode
     * @throws IOException if failed to write
     */
    @Override
    public void encode(OutputStreamHelper outStream, int n) throws IOException {
        if(n <= 63)
        {
            writeByte(outStream, (byte) n);
            return;
        }

        int largestBit = findLargestBit(n) + 1;
        int length = (largestBit + 1) / 8;
        largestBit = largestBit % 8 == 6 ? largestBit : largestBit + (8 - (largestBit+2) % 8);

        byte b = 0;
        b |= length << 6;
        b |= (n >> (largestBit - 6)) & 63;
        writeByte(outStream, b);

        for(int i = largestBit - 8; i >= 0; i-= 8)
        {
            writeByte(outStream, (byte) ((n >> (i - 6)) & 255));
        }
    }

    /**
     * @param inputStream an encoded stream to decode
     * @return the next number encoded in the stream
     * @throws IOException if failed to read
     */
    @Override
    public int decodeNumber(InputStreamHelper inputStream) throws IOException {
        byte b = advanceByte(inputStream);
        //get length
        int length = (b & (127 + 128)) >> 6;
        int n = b & 63;
        for(int i = 0; i < length; i++)
        {
            n = 256 * n + Byte.toUnsignedInt(advanceByte(inputStream));
        }
        return n;
    }
}
