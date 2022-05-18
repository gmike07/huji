package processing.parsingRules;

import processing.textStructure.Block;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class ParsingHelper {
    private static final String ACTOR_STRING = "with the characters: ";
    /* holds the current scene number */
    private static int sceneNumber;
    /* holds the current scene title */
    private static String title;
    /* the number group of the scene number */
    private static final int SCENE_NUMBER = 1;
    /* the number group of the scene title */
    private static final int SCENE_TITLE = 2;
    /* the number group of the actors */
    private static final int GET_ACTOR = 1;

    /**
     * @param block the current block
     * @param metadata the metadata of the block
     * @param actorsPattern the actor pattern
     * adds actors to the metadata
     */
    private static void addActors(Block block, List<String> metadata, Pattern actorsPattern){
        StringBuilder actorString = new StringBuilder(ACTOR_STRING);
        Set<String> actorsSet = new HashSet<>();
        Matcher actors = actorsPattern.matcher(block.toString());
        while(actors.find()) {
            String actor = actors.group(GET_ACTOR);
            if(!actor.equals("THE END") && !actorsSet.contains(actor))
                actorsSet.add(actor);
        }
        for(String actor : actorsSet){
            actorString.append("\"").append(actor).append("\", ");
        }
        if(actorString.toString().equals(ACTOR_STRING)) //no actors were found
            return;
        metadata.add(actorString.substring(0, actorString.length() - ", ".length()));
    }


    /**
     * @param block the current block
     * @param metadataEntry the metadata of the entry
     * @param actorsPattern the actor pattern
     * adds the metadata to the block
     */
    static void addMetadataToBlock(Block block,List<String> metadataEntry, Pattern actorsPattern){
        List<String> metadata = new LinkedList<>();
        metadata.add("Appearing in scene " + sceneNumber + ", titled \"" + title + "\"");
        metadata.addAll(metadataEntry);
        addActors(block, metadata, actorsPattern);
        block.setMetadata(metadata);
    }

    /**
     * @param raf the file to read from
     * @param sceneMatcher the scene matcher
     * @param iparsingRule the current parsing rule
     * @param blocks a list of all current blocks
     * this function fills the block list with all the blocks
     * @throws IOException if there was a problem with the raf
     */
    private static void parseScenesHelper(RandomAccessFile raf, Matcher sceneMatcher,
                                         IparsingRule iparsingRule, List<Block> blocks) throws IOException {
        int startScene = sceneMatcher.start();
        sceneNumber = Integer.valueOf(sceneMatcher.group(SCENE_NUMBER));
        title = sceneMatcher.group(SCENE_TITLE);
        while(sceneMatcher.find()){
            int scene = Integer.valueOf(sceneMatcher.group(SCENE_NUMBER));
            if(scene > sceneNumber) {
                blocks.add(iparsingRule.parseRawBlock(raf, startScene, sceneMatcher.start()));
                startScene = sceneMatcher.start();
                sceneNumber = scene;
                title = sceneMatcher.group(SCENE_TITLE);
            }
        }
        blocks.add(iparsingRule.parseRawBlock(raf, startScene, raf.length()));
    }

    /**
     * @param raf the file to read from
     * @param sceneMatcher the scene matcher
     * @param iparsingRule the current parsing rule
     * @return a list of all blocks in the file
     * @throws IOException if there was a problem with the raf
     */
    static List<Block> parseScenes(RandomAccessFile raf, Matcher sceneMatcher, IparsingRule iparsingRule)
            throws IOException {
        List<Block> blocks = new LinkedList<>();
        parseScenesHelper(raf, sceneMatcher, iparsingRule, blocks);
        return blocks;
    }
}
