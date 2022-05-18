package CompressionV2;
import java.io.IOException;

public class bitLengthCompression extends AbstractBitIntegerCompression {

    /**
     * encodes the number to the stream
     * @param outStream the stream to write the encoded to
     * @param n the number to encode
     * @throws IOException if failed to write
     */
    @Override
    public void encode(OutputStreamHelper outStream, int n) throws IOException {
        for(int i = 0; i < n - 1; i++)
        {
            writeBit(outStream, 1);
        }
        writeBit(outStream, 0);
    }

    /**
     * @param inputStream an encoded stream to decode
     * @return the next number encoded in the stream
     * @throws IOException if failed to read
     */
    @Override
    public int decodeNumber(InputStreamHelper inputStream) throws IOException {
        int counter = 0;
        while(advanceBit(inputStream) == 1)
        {
            counter++;
            //to handle the last 11111 bits
            if(!hasMoreToRead())
            {
                throw new IOException("reached end of file");
            }
        }
        return counter + 1;
    }
}
