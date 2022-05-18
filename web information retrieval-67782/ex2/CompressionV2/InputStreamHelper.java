package CompressionV2;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.RandomAccessFile;

public class InputStreamHelper {
    // an input stream
    public InputStream inputStream = null;
    // a random access file
    public RandomAccessFile randomAccessFile = null;

    private int length = 0;
    private int currLength = 0;
    /**
     * @param i an input stream
     */
    public InputStreamHelper(InputStream i)
    {
        inputStream = i;
    }

    public InputStreamHelper(InputStream i, int endLength)
    {
        inputStream = i;
        length = endLength;
        currLength = 0;
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
        if(length != 0)
        {
            if(currLength >= length)
            {
                return -1;
            }
            currLength++;
        }
        if(randomAccessFile == null)
        {
            return inputStream.read();
        }
        return randomAccessFile.read();
    }


    public void close() throws IOException
    {
        if(randomAccessFile == null)
        {
            inputStream.close();
            return;
        }
        randomAccessFile.close();
    }
}
