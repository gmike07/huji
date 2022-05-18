import dataStructures.Aindexer;
import dataStructures.IndexerFactory;
import processing.textStructure.*;
import utils.BadInputException;
import utils.Parser;
import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * The main program - A text searching module that indexes and queries large corpuses for strings or word groups
 */
public class TextSearcher {
    private static final int NUMBER_OF_RESULTS = 10;
    private static Parser parser;
    private static Corpus corpus;
    private static Aindexer indexer;
    /**
     * Main method. Reads and parses a command file and if a query exists, prints the results.
     * @param args the argument file
     */
    public static void main(String[] args){
        if (!initParser(args)) return;
        corpus = new Corpus(parser.getCorpus().getPath(), parser.getParsingRule().toString());
        if (!initIndexer()) return;
        if (!parser.hasQuery()) return;
        List<? extends WordResult> words = indexer.asSearchInterface().search(parser.getQuery());
        //sort and print results
        try {
            sortAndPrint(words);
        } catch (IOException e) {
            //shouldn't reach here
            printError(e);
        }
    }

    /**
     * @param args the inputs of the program
     * @return false if there was a bad format in the input, else true, init the parser variable
     */
    private static boolean initParser(String[] args) {
        try {
            parser = new Parser(args);
        } catch (BadInputException e){
            //may reach here, print error
            printError(e);
            return false;
        }
        return true;
    }

    /**
     * @return false if there was a problem in the indexer, else true, init the indexer variable and call
     * index of indexer
     */
    private static boolean initIndexer() {
        indexer = IndexerFactory.getIndexer(parser.getIndexer(), corpus);
        if (indexer == null)
            return false;
        try {
            indexer.index();
            return true;
        } catch (IOException e) {
            //may reach here
            printError(e);
            return false;
        }
    }

    /**
     * @param words a list of results
     * @throws IOException if there was a problem printing the results
     * the function sorts if needed then prints the NUMBER_OF_RESULTS first results
     */
    private static void sortAndPrint(List<? extends WordResult> words) throws IOException {
        if (words.size() == 0)
            return;
        List<? extends WordResult> results;
        if (words.get(0) instanceof MultiWordResult){ //everything is multi then sort by multi
            results = sortMultiResults(words);
        }else{ //already sorted
            results = words;
        }
        System.out.println("The top " + Math.min(NUMBER_OF_RESULTS,results.size())
                + " results for query " + parser.getQuery() +
                " are:");
        for (int i = 0; i < results.size() && i < NUMBER_OF_RESULTS; i++) {
            corpus.getParsingRule().printResult(results.get(i));
        }
    }

    /**
     * @param words a list of results
     * the function sorts the multiWordResult and returns it as a list
     */
    private static List<MultiWordResult> sortMultiResults(List<? extends WordResult> words){
        List<MultiWordResult> results = new ArrayList<>();
        for (WordResult word : words)
            results.add((MultiWordResult)word);
        Collections.sort(results);
        return results;
    }


    /**
     * @param e exception to print
     * prints the error that occurred
     */
    private static void printError(Exception e){
        System.out.println(e.getMessage());
    }
}