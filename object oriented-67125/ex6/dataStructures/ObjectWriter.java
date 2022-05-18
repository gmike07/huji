package dataStructures;
import processing.textStructure.Corpus;
import utils.WrongMD5ChecksumException;

import java.io.*;

public class ObjectWriter {

    /**
     * @param indexer the indexer to read from
     * @return the object that was read from the file (dict / trees) if could read it, and updates the corpus
     * @throws FileNotFoundException if there was a problem with the file
     * @throws WrongMD5ChecksumException if it is not the same corpus
     */
    public static Object readIndexedFile(Aindexer<?> indexer) throws FileNotFoundException,
            WrongMD5ChecksumException {
        File inputFile = new File(indexer.getIndexedPath());
        try {
            ObjectInputStream objectInputStream = new ObjectInputStream(new FileInputStream(inputFile));
            String lastMD5 = (String) objectInputStream.readObject();
            String currentMD5;
            try {
                currentMD5 = indexer.origin.getChecksum();
            } catch (IOException e) {
                throw new FileNotFoundException();
            }
            if (!lastMD5.equals(currentMD5))
                throw new WrongMD5ChecksumException();
            indexer.setCorpus((Corpus) objectInputStream.readObject());
            Object object = objectInputStream.readObject();
            objectInputStream.close();
            return object;
        } catch (IOException | ClassNotFoundException e) {
            throw new FileNotFoundException();
        }
    }

    /**
     * @param indexer the indexer to read from
     * @param object the object to write to the file
     */
    public static void writeIndexedFile(Aindexer<?> indexer, Object object){
        try {
            File outputFile = new File(indexer.getIndexedPath());
            if (!outputFile.exists())
                if (!outputFile.createNewFile())
                    throw new IOException();
            ObjectOutputStream outputObject = new ObjectOutputStream(new FileOutputStream(outputFile));
            outputObject.writeObject(indexer.origin.getChecksum());
            outputObject.writeObject(indexer.origin);
            outputObject.writeObject(object);
            outputObject.close();
        } catch (IOException e) {
            //shouldn't come here
            e.printStackTrace();
        }
    }
}
