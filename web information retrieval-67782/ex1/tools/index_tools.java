package tools;

public class index_tools
{
    // the size of int
    public static final int INT_SIZE = 4;

    /**
     * converts the data to byte[] and saves it in ans
     * @param ans a byte[] to store the number in
     * @param data the number to convert
     */
    public static void int_to_byte(byte[] ans, int data)
    {
        ans[3] = (byte)((data >> 24) & 0xff);
        ans[2] = (byte)((data >> 16) & 0xff);
        ans[1] = (byte)((data >> 8) & 0xff);
        ans[0] = (byte)((data >> 0) & 0xff);
    }

    /**
     * @param data an int to convert to byte[]
     * @return the byte[] representation of the int
     */
    public static byte[] int_to_byte(int data)
    {
        byte[] ans = new byte[INT_SIZE];
        int_to_byte(ans, data);
        return ans;
    }

    /**
     * @param data the int[] to convert
     * @return converts the int[] to byte[] and returns it
     */
    public static byte[] int_array_to_byte(int[] data)
    {
        byte[] current_int = new byte[INT_SIZE];
        byte[] ans = new byte[data.length * INT_SIZE];
        for (int i = 0; i < data.length; i++)
        {
            int_to_byte(current_int, data[i]);
            for (int j = 0; j < INT_SIZE; j++)
                ans[j + i * INT_SIZE] = current_int[j];
        }
        return ans;
    }

    /**
     * converts the int[] to byte[] and saves it in ans
     * @param ans the byte[] to store the answer in
     * @param data the int[] to convert
     */
    public static void int_array_to_byte(byte[] ans, int[] data)
    {
        byte[] current_int = new byte[INT_SIZE];
        for (int i = 0; i < data.length; i++)
        {
            int_to_byte(current_int, data[i]);
            for (int j = 0; j < INT_SIZE; j++)
                ans[j + i * INT_SIZE] = current_int[j];
        }
    }

    /**
     * @param a an array of bytes to convert to int
     * @param first_index from where to read the array
     * @return the int representation of the bytes from position first_index
     */
    public static int byte_to_int(byte[] a, int first_index)
    {
        int size = Math.min(a.length, INT_SIZE);
        int byte_size = 8;
        int ans = 0;
        for (int i = 0; i < size; i++)
        {
            ans = ans | ((a[first_index + i]  & 0xFF) << (i * byte_size));
        }
        return ans;
    }

    /**
     * @param a an array of bytes to convert to int
     * @return the int representation of the bytes
     */
    public static int byte_to_int(byte[] a)
    {
        return byte_to_int(a, 0);
    }

}
