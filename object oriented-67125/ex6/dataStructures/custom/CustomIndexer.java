package dataStructures.custom;

import dataStructures.Aindexer;
import processing.parsingRules.IparsingRule;
import processing.searchStrategies.CustomSearch;
import processing.textStructure.Corpus;
import utils.WrongMD5ChecksumException;

import java.io.FileNotFoundException;

public class CustomIndexer extends Aindexer<CustomSearch> {
    private CustomSearch search;
    /**
     * Basic constructor accepting origin Corpus
     *
     * @param origin The corpus indexed in this DS.
     */
    public CustomIndexer(Corpus origin) {
        super(origin);
        search = new CustomSearch(origin);
    }

    @Override
    /*
     * get the backing search interface.
     * @return  The search interface implementation used by this indexer.
     */
    public CustomSearch asSearchInterface() {
        return search;
    }

    @Override
    protected void indexCorpus() {
        // does nothing
    }

    @Override
    /*
     * Try to read a cached index file if one already exists.
     */
    protected void readIndexedFile() throws FileNotFoundException, WrongMD5ChecksumException {
        throw new WrongMD5ChecksumException();
    }

    @Override
    /*
     * Write the internal index into file.
     */
    protected void writeIndexFile() {
        // does nothing
    }

    @Override
    /*
     * Extract the parsing rule used for indexing this data structure.
     * @return  an instance of a parser implementing IparsingRule
     */
    public IparsingRule getParseRule() {
        return origin.getParsingRule();
    }
}
