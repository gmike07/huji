package processing.searchStrategies;

import processing.textStructure.Block;

class WordContainer {
    /* the block it contains */
    private Block block;
    /* the word it has in the block */
    private String word;
    /* the start index of the word in the block */
    private long startIndex;
    WordContainer(Block block, String word, long startIndex){
        this.block = block;
        this.word = word;
        this.startIndex = startIndex;
    }

    /**
     * @return the block
     */
    Block getBlock() {
        return block;
    }

    /**
     * @return the word
     */
    String getWord(){
        return word;
    }

    /**
     * @return the statIndex
     */
    long getStartIndex(){
        return startIndex;
    }
}
