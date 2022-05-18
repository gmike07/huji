package utils;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.List;

public class ToolBox {
    /**
     * @param file the raf to read from
     * @param start from where to start reading
     * @param length how much to read
     * @return the string from start to start + length
     * @throws IOException if there was a problem with the raf
     */
    public static String readFromFile(RandomAccessFile file, long start, int length) throws IOException {
        file.seek(start);
        byte[] rawBytes = new byte[length];
        file.read(rawBytes);
        return new String(rawBytes);
    }

    /**
     * @param file the raf to read from
     * @param start from where to start reading
     * @param length how much to read
     * @return the string from start to start + length, if there was a problem with the raf return ""
     */
    public static String readFromFileNoIO(RandomAccessFile file, long start, int length){
        try {
            return readFromFile(file, start, length);
        } catch (IOException e) {
            return "";
        }
    }

    /**
     * @param strings a list of strings
     * @return a string that is a combination of all strings in the list
     */
    public static String convertToString(List<String> strings){
        StringBuilder result = new StringBuilder();
        for (String s : strings)
            result.append(s).append("\n");
        return result.toString();
    }

    /**
     * @param file the raf to read from
     * @return a string of all the data in the file
     */
    public static String readFile(RandomAccessFile file) throws IOException {
        return readFromFile(file, 0, (int)file.length());
    }
}
