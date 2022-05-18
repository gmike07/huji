package utils;
import dataStructures.Aindexer;
import processing.parsingRules.IparsingRule;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Parser {
    /* regex to check the file validity */
    private static final String regexInputs = "CORPUS\\n(.*?)\\nINDEXER\\n(.*?)\\nPARSE_RULE\\n(.*?)\\n" +
            "(QUERY\\n(.*?)\\n)?";
    /* the pattern to check the file validity */
    private Pattern patternInputs = Pattern.compile(regexInputs);
    /* the path of the corpus in the file */
    private File corpusPath;
    /* the query in the file */
    private String query = "";
    /* the parsingRule in the file */
    private IparsingRule.ParserTypes parsingRule;
    /* the indexer in the file */
    private Aindexer.IndexTypes indexer;
    /* contains whether the query exists */
    private boolean isQuery = false;
    /* the lines of the file */
    private List<String> lines;
    /* the number group of the corpus */
    private static final int CORPUS = 1;
    /* the number group of the indexer */
    private static final int INDEXER = 2;
    /* the number group of the parser */
    private static final int PARSER = 3;
    /* the number group of the is query field */
    private static final int IS_QUERY = 4;
    /* the number group of the query */
    private static final int QUERY = 5;


    /**
     * @param args the path to the command file
     * @throws BadInputException if there is a bad format to the command file
     */
    public Parser(String[] args) throws BadInputException {
        checkInputs(args);
        try {
            checkFileValidity();
        } catch (NoSuchElementException e){
            throw new BadInputException("the file didn't contain all the needed info");
        }
    }

    /**
     * @param args the path to the command file
     * @throws BadInputException if the path isn't a file or not correct number of args were given
     */
    private void checkInputs(String[] args) throws BadInputException {
        if (args.length != 1)
            throw new BadInputException("wrong number of parameters");
        String filePath = args[0];
        try {
            lines = Files.readAllLines(Paths.get(filePath));
        } catch (IOException exception){
            throw new BadInputException("file doesn't exists");
        }
    }

    /**
     * reads and stores the info from the args file
     * @throws BadInputException if the args file is not in the correct format
     */
    private void checkFileValidity() throws BadInputException {
        StringBuilder text = new StringBuilder();
        for (String line : lines)
            text.append(line).append("\n");
        if (lines.get(lines.size() - 1).equals("QUERY")){
            text.append(" \n");
        }
        String data  = text.toString();
        Matcher m = patternInputs.matcher(data);
        if (!m.matches())
            throw new BadInputException("the file is in wrong format");
        checkCorpus(m.group(CORPUS));
        checkIndexer(m.group(INDEXER));
        checkParser(m.group(PARSER));
        if (m.group(IS_QUERY) != null){
            isQuery = true;
            checkQuery(m.group(QUERY));
        }
    }

    /**
     * @param path the path of the corpus in the file, store the path in corpusPath
     * @throws BadInputException if there is a problem with the path
     */
    private void checkCorpus(String path) throws BadInputException {
        corpusPath = new File(path);
        if (corpusPath.isDirectory())
            return;
        if (corpusPath.isFile())
            return;
        throw new BadInputException("unknown type of corpus");
    }

    /**
     * @param indexer the indexer rule in the file, store the indexer in indexer
     * @throws BadInputException if there is a problem with the indexer rule
     */
    private void checkIndexer(String indexer) throws BadInputException {
        try {
            this.indexer = Aindexer.IndexTypes.valueOf(indexer);
        } catch (NoSuchElementException e) {
            throw new BadInputException("unknown type of indexer");
        }
    }

    /**
     * @param parsingRule the parsing rule in the file, store the parser in parsingRule
     * @throws BadInputException if there is a problem with the parsing rule
     */
    private void checkParser(String parsingRule) throws BadInputException {
        try {
            this.parsingRule = IparsingRule.ParserTypes.valueOf(parsingRule);
        } catch (NoSuchElementException e) {
            throw new BadInputException("unknown type of parsing rule");
        }
    }

    /**
     *
     * @param query the query line if such exists
     * @throws BadInputException if the modifiers are not quick or case
     */
    private void checkQuery(String query) throws BadInputException {
        String[] queries = query.split("#");
        if (queries.length > 1)
            throw new BadInputException("too many #");
        this.query = queries[0];
    }


    /**
     * @return the corpus path specified in the file
     */
    public File getCorpus(){
        return this.corpusPath;
    }

    /**
     * @return the ParserTypes specified in the file
     */
    public IparsingRule.ParserTypes getParsingRule(){
        return this.parsingRule;
    }

    /**
     * @return the IndexTypes specified in the file
     */
    public Aindexer.IndexTypes getIndexer(){
        return this.indexer;
    }

    /**
     * @return true if there is a query, else false
     */
    public boolean hasQuery(){
        return isQuery;
    }
    /**
     * @return the query in the file if exists, else ""
     */
    public String getQuery(){
        return query;
    }
}
