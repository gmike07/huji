package utils;

public class WrongMD5ChecksumException extends Throwable {
    public WrongMD5ChecksumException(){
        super("Corpus MD5 doesn't match indexed MD5");
    }
}
