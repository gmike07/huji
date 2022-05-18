package utils;

import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * Helper class for calculating an MD5 checksum for a string
 */
public class MD5 {
    /**
     * Get an MD5 checksum from an input string.
     * @param input - the string to calculate a checksum for.
     * @return - String object representing the checksum.
     */
    public static String getMd5(String input)
    {
        try {

            // Static getInstance method is called with hashing utils.MD5
            MessageDigest md = MessageDigest.getInstance("MD5");

            // digest() method is called to calculate message digest 
            //  of an input digest() return array of byte 
            byte[] messageDigest = md.digest(input.getBytes());

            // Convert byte array into signum representation 
            BigInteger no = new BigInteger(1, messageDigest);

            // Convert message digest into hex value 
            String hashtext = no.toString(16);
            while (hashtext.length() < 32) {
                hashtext = "0" + hashtext;
            }
            return hashtext;
        }

        // For specifying wrong message digest dataStructures
        catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Get an MD5 checksum from an input byte array.
     * @param inputBytes - the array of bytes to calculate a checksum from.
     * @return - an output String object representing the checksum.
     */
    public static String getMd5(byte[] inputBytes)
    {
        try {

            // Static getInstance method is called with hashing utils.MD5
            MessageDigest md = MessageDigest.getInstance("MD5");

            // digest() method is called to calculate message digest
            //  of an input digest() return array of byte
            byte[] messageDigest = md.digest(inputBytes);

            // Convert byte array into signum representation
            BigInteger no = new BigInteger(1, messageDigest);

            // Convert message digest into hex value
            String hashtext = no.toString(16);
            while (hashtext.length() < 32) {
                hashtext = "0" + hashtext;
            }
            return hashtext;
        }

        // For specifying wrong message digest dataStructures
        catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

}