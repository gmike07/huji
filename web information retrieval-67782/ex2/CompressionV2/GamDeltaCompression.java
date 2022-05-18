package CompressionV2;

import java.io.IOException;

public class GamDeltaCompression extends AbstractBitIntegerCompression {
    //helper compressions to encode with
    private static final GammaCompression b1 = new GammaCompression();
    private static final DeltaCompression b2 = new DeltaCompression();
    //which compression to use
    private int counter;

    /**
     * @param startGamma boolean with which compression to start
     */
    public GamDeltaCompression(boolean startGamma)
    {
        if(startGamma)
        {
            counter = 0;
        }
        else
        {
            counter = 1;
        }
    }

    /**
     * encodes the number to the stream
     * @param outStream the stream to write the encoded to
     * @param n the number to encode
     * @throws IOException if failed to write
     */
    @Override
    public void encode(OutputStreamHelper outStream, int n) throws IOException {
        AbstractBitIntegerCompression b = counter == 0 ? b1 : b2;
        b.moveToPosition(this);
        b.encode(outStream, n);
        moveToPosition(b);
        b.moveToPosition(this);
        counter = (counter + 1) % 2;
    }

    /**
     * @param inputStream an encoded stream to decode
     * @return the next number encoded in the stream
     * @throws IOException if failed to read
     */
    @Override
    public int decodeNumber(InputStreamHelper inputStream) throws IOException {
        AbstractBitIntegerCompression b = counter == 0 ? b1 : b2;
        b.moveToPosition(this);
        int n = b.decodeNumber(inputStream);
        moveToPosition(b);
        counter = (counter + 1) % 2;
        return n;
    }

}
