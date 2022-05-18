package CompressionV2;

import java.io.*;
import java.util.*;

public class NoStringCompression extends AbstractStringCompression
{
    @Override
    public void encodeChar(OutputStreamHelper stream, char c) throws IOException
    {
        writeByte(stream, (byte) c);
    }

    /**
     * @param stream the stream to read from
     * @return the decoded char from the stream
     * @throws IOException if failed to read
     */
    @Override
    public char decodeChar(InputStreamHelper stream) throws IOException {
        int d = advanceByte(stream);
        return (char) (d & 0xFF);
    }

    @Override
    public void save(String dir) throws IOException {

    }

    @Override
    public void load(String dir) throws IOException {

    }
}
