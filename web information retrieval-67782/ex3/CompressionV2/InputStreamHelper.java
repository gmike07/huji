package CompressionV2;

import java.io.IOException;
import java.io.InputStream;
import java.io.RandomAccessFile;

public class InputStreamHelper {
    // an input stream
    private InputStream inputStream = null;
    // a random access file
    private RandomAccessFile randomAccessFile = null;

    /**
     * @param i an input stream
     */
    public InputStreamHelper(InputStream i)
    {
        inputStream = i;
    }

    /**
     * @param randomAccessFile a random access file
     */
    public InputStreamHelper(RandomAccessFile randomAccessFile)
    {
        this.randomAccessFile = randomAccessFile;
    }

    /**
     * if random access file, move it to pos
     * @param pos the position to move to
     * @throws IOException if failed to move
     */
    public void seek(long pos) throws IOException {
        if(randomAccessFile != null)
        {
            randomAccessFile.seek(pos);
        }
    }

    /**
     * @throws IOException if failed to read
     * @return if random access file, get current pointer, else 0
     */
    public long getFilePointer() throws IOException {
        if(randomAccessFile != null)
        {
            return randomAccessFile.getFilePointer();
        }
        return 0;
    }

    /**
     * @return reads byte from the stream
     * @throws IOException if failed to read
     */
    public int read() throws IOException {
        if(randomAccessFile == null)
        {
            return inputStream.read();
        }
        return randomAccessFile.read();
    }
}
