package CompressionV2;

import java.io.BufferedInputStream;
import java.util.Enumeration;

public class EnumerationDictionaryField implements Enumeration<Integer>
{

    public EnumerationDictionaryField(BufferedInputStream in_stream)
    {

    }

    @Override
    public boolean hasMoreElements() {
        return false;
    }

    @Override
    public Integer nextElement() {
        return null;
    }
}
