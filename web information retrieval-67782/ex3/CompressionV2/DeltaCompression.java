package CompressionV2;

import java.io.IOException;

public class DeltaCompression extends AbstractBitIntegerCompression {
    //an helper compression to encode with
    private static final GammaCompression b = new GammaCompression();

    /**
     * encodes the number to the stream
     * @param outStream the stream to write the encoded to
     * @param n the number to encode
     * @throws IOException if failed to write
     */
    @Override
    public void encode(OutputStreamHelper outStream, int n) throws IOException {
        int len = findLargestBit(n) + 1;
        b.moveToPosition(this);
        b.encode(outStream, len);
        moveToPosition(b);
        for(int i = len - 2; i >= 0; i--)
        {
            writeBit(outStream, (n >> i) & 1);
        }
        b.moveToPosition(this);
    }

    /**
     * @param inputStream an encoded stream to decode
     * @return the next number encoded in the stream
     * @throws IOException if failed to read
     */
    @Override
    public int decodeNumber(InputStreamHelper inputStream) throws IOException {
        b.moveToPosition(this);
        int len = b.decodeNumber(inputStream);
        int n = 1;
        moveToPosition(b);
        for(int i = 0; i < len - 1; i++)
        {
            n = 2 * n + advanceBit(inputStream);
        }
        return n;
    }
}
