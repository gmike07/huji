package Index;

import Dictionary.ConcatenatedStringDict;
import tools.index_tools;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.function.Consumer;

public class IndexMerger
{
    @FunctionalInterface
    public interface FiveParameterFunction<T, U, V, W, R> {
        public void apply(T t, U u, V v, W w, R r);
    }

    public static class Tuple
    {
        public int currRevId; public int pointerIndex;
        Tuple(int b1, int b2)
        {
            currRevId = b1; pointerIndex = b2;
        }
    }

    private static final int MAX_INDEXES_RAM = 20;
    private static final String prevDirName = "prevDir";
    private static final String currDirName = "currDir";

    private static ArrayList<Integer> findMinimalIndex(ArrayList<Index> indexes, String dictName)
    {
        ArrayList<Integer> minimalIndexes = new ArrayList<>();
        String minimalString = null;
        for(int i = 0; i < indexes.size(); i++)
        {
            Index index = indexes.get(i);
            if(index.reachedEnd(dictName))
            {
                continue;
            }
            if(minimalString == null)
            {
                minimalIndexes.add(i);
                minimalString = index.getCurrentString();
                continue;
            }
            int comp = index.getCurrentString().compareTo(minimalString);
            if(comp < 0)
            {
                minimalIndexes = new ArrayList<>();
                minimalString = index.getCurrentString();
            }
            if(comp <= 0)
            {
                minimalIndexes.add(i);
            }
        }
        return minimalIndexes;
    }

    private static void mergeDictIndexes(ArrayList<Index> indexes, Index newIndex, String mainDictName,
                                      String otherDictName,
                                         FiveParameterFunction<ArrayList<Index>, ArrayList<Integer>, Index,
                                                 ConcatenatedStringDict, ConcatenatedStringDict> func)
    {
        indexes.forEach((index) -> index.initPointer(mainDictName, true));
        ConcatenatedStringDict mainDict = newIndex.getDictionary(mainDictName);
        ConcatenatedStringDict otherDict = newIndex.getDictionary(otherDictName);

        ArrayList<Integer> minimalIndexes = findMinimalIndex(indexes, mainDictName);

        while(minimalIndexes.size() > 0)
        {
            func.apply(indexes, minimalIndexes, newIndex, mainDict, otherDict);
            minimalIndexes.forEach((minIndex) -> indexes.get(minIndex).advancePointer(mainDictName, true));
            minimalIndexes = findMinimalIndex(indexes, mainDictName);
        }
    }

    private static void mergeMinimalProductIdIndexes(ArrayList<Index> indexes, ArrayList<Integer> minIndexes,
                                                     Index newIndex,
                                              ConcatenatedStringDict pidDict,
                                              ConcatenatedStringDict pidIdsListDict,
                                                     ArrayList<int[]> pointers)
    {
        Index minZeroIndex = indexes.get(minIndexes.get(0));
        String productId = minZeroIndex.getCurrentString();
        pidDict.append(productId);
        byte[] currentList = minZeroIndex.get_field("first_id", minZeroIndex.getCurrentPointer());
        int minRevId = index_tools.byte_to_int(currentList, 0);
        currentList = minZeroIndex.get_field("num_id", minZeroIndex.getCurrentPointer());
        int maxRevId = minRevId + index_tools.byte_to_int(currentList, 0);

        for(int i : minIndexes)
        {
            Index index = indexes.get(i);
            pointers.get(i)[index.getCurrentPointer()] = pidDict.getNumRows() - 1;
            currentList = index.get_field("first_id", index.getCurrentPointer());
            int curentMinRevId = index_tools.byte_to_int(currentList, 0);
            currentList = index.get_field("num_id", index.getCurrentPointer());
            int curentMaxRevId = curentMinRevId + index_tools.byte_to_int(currentList, 0);

            minRevId = Math.min(curentMinRevId, minRevId);
            maxRevId = Math.max(curentMaxRevId, maxRevId);
        }

        newIndex.new_row();
        newIndex.update_field_in_row("first_id", tools.index_tools.int_to_byte(minRevId));
        newIndex.update_field_in_row("num_id", tools.index_tools.int_to_byte(maxRevId - minRevId));
        newIndex.finish_row();
    }


    private static void mergeMinimalTokenIndexes(ArrayList<Index> indexes, ArrayList<Integer> minIndexes,
                                                 Index newTokenIndex,
                                              ConcatenatedStringDict tokenDict,
                                              ConcatenatedStringDict tokenIdFreqListDict, boolean gapId)
    {
        String token = indexes.get(minIndexes.get(0)).getCurrentString();
        tokenDict.append(token);
        mergeIdFreqLists(indexes, minIndexes, tokenIdFreqListDict, gapId);
        byte[] current_list;
        int numAppearances = 0, numReviewsContainToken = 0;

        for(int i: minIndexes)
        {
            Index index = indexes.get(i);
            current_list = index.get_field("num_appearances", index.getCurrentPointer());
            numAppearances += index_tools.byte_to_int(current_list);

            current_list = index.get_field("num_reviews_contain_token", index.getCurrentPointer());
            numReviewsContainToken += index_tools.byte_to_int(current_list);
        }

        newTokenIndex.new_row();
        newTokenIndex.update_field_in_row("num_reviews_contain_token", index_tools.int_to_byte(numReviewsContainToken));
        newTokenIndex.update_field_in_row("num_appearances", index_tools.int_to_byte(numAppearances));
        newTokenIndex.finish_row();
    }

    private static void mergeReviewsIndexes(ArrayList<Index> indexes, Index newReviewId,
                                            ArrayList<int[]> pointers)
    {
        for(int i = 0; i < indexes.size(); i++)
        {
            Index currentIndex = indexes.get(i);
            for(int row = 0; row < currentIndex.getNumRows(); row++)
            {
                newReviewId.new_row();
                //TODO: maybe not cheat and do O(n) and not O(n * log(n))
                int oldPointer = index_tools.byte_to_int(currentIndex.get_field("pid", row));
                newReviewId.update_field_in_row("pid", index_tools.int_to_byte(pointers.get(i)[oldPointer]));
                // NOTE: the function knows how much bytes to read (score is ONE byte while we sent 4 bytes
                newReviewId.update_field_in_row("score", currentIndex.get_field("score", row));
                newReviewId.update_field_in_row("helpN", currentIndex.get_field("helpN", row));
                newReviewId.update_field_in_row("helpD", currentIndex.get_field("helpD", row));
                newReviewId.update_field_in_row("num_tokens", currentIndex.get_field("num_tokens", row));
                newReviewId.finish_row();
            }
        }
    }

    public static void mergeIndexes(String dir, int index, ArrayList<Index> productIndexes,
                             ArrayList<Index> tokenIndexes,
                             ArrayList<Index> reviewIndexes)
    {
        if(index != -1)
        {
            IndexFactory.init_factory(dir, true, index);
        }
        Index reviewIndex = IndexFactory.get_review_ind();
        Index pidIndex = IndexFactory.get_pid_ind();
        Index tokenIndex = IndexFactory.get_token_ind();

        IndexFactory.clear();

        FiveParameterFunction<ArrayList<Index>, ArrayList<Integer>, Index, ConcatenatedStringDict,
                ConcatenatedStringDict> f;
        ArrayList<int[]> pointers = new ArrayList<>();
        for(int i = 0; i < productIndexes.size(); i++)
        {
            pointers.add(new int[productIndexes.get(i).getDictionary("pid").getNumRows()]);
        }
        f = (indexes, minIndexes, newIndex, mainDict, otherDict) -> mergeMinimalProductIdIndexes(indexes,
                minIndexes, newIndex, mainDict, otherDict, pointers);
        mergeDictIndexes(productIndexes, pidIndex, "pid", "pid", f);
        pidIndex.save_to_disk();

        try
        {
            pidIndex.close();
            pidIndex = null;
        }catch (IOException e){
            e.printStackTrace();
        }
        System.gc();

        f = (indexes, minIndexes, newIndex, mainDict, otherDict) -> mergeMinimalTokenIndexes(indexes,
                minIndexes, newIndex, mainDict,  otherDict, true);
        mergeDictIndexes(tokenIndexes, tokenIndex, "token", "token_id_freq_list", f);
        tokenIndex.save_to_disk();

        try
        {
            tokenIndex.close();
            tokenIndex = null;
        }catch (IOException e){
            e.printStackTrace();
        }
        System.gc();

        mergeReviewsIndexes(reviewIndexes, reviewIndex, pointers);

        reviewIndex.save_to_disk();

        try
        {
            reviewIndex.close();
            reviewIndex = null;
        }catch (IOException e){
            e.printStackTrace();
        }
    }


    private static String getCurrentDir(String dir)
    {
        return dir + File.separatorChar + currDirName;
    }

    public static String getPrevDir(String dir)
    {
        return dir + File.separatorChar + prevDirName;
    }

    private static void renameDir(String parentDir, String oldName, String newName)
    {
        File dir = new File(parentDir + File.separatorChar + oldName);
        File newDir = new File(parentDir + File.separatorChar + newName);
        dir.renameTo(newDir);
    }

    public static void createFolder(String dir)
    {
        File fdir = new File(dir);
        if (!fdir.exists())
        {
            fdir.mkdirs();
        }
    }

    private static  void deleteFolder(String dir) {
        File index = new File(dir);
        if(!index.exists())
        {
            return;
        }
        String[] entries = index.list();
        if(entries != null)
        {
            for(String s: entries){
                File currentFile = new File(index.getPath(), s);
                try{
                    Files.delete(Path.of(currentFile.getPath()));
                }catch(IOException e)
                {
                    e.printStackTrace();
                }
            }
        }
        index.delete();
    }


    private static int mergeIndexesOnce(String dir, int maxIndexNumber)
    {
        ArrayList<Index> productIndexes, tokenIndexes, reviewIndexes;
        int counter = 0;
        productIndexes = new ArrayList<Index>();
        tokenIndexes = new ArrayList<Index>();
        reviewIndexes = new ArrayList<Index>();

        Consumer<Index> closer = (index) -> {
            try {
                index.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        };

        for(int i = 0; i < maxIndexNumber; i+= MAX_INDEXES_RAM)
        {
            for(int j = i; j < i + MAX_INDEXES_RAM && j < maxIndexNumber; j++)
            {
                IndexFactory.init_factory(getPrevDir(dir), false, j);
                IndexFactory.get_pid_ind().load_from_disk();
                IndexFactory.get_token_ind().load_from_disk();
                IndexFactory.get_review_ind().load_from_disk();

                productIndexes.add(IndexFactory.get_pid_ind());
                tokenIndexes.add(IndexFactory.get_token_ind());
                reviewIndexes.add(IndexFactory.get_review_ind());
            }
            mergeIndexes(getCurrentDir(dir), i / MAX_INDEXES_RAM, productIndexes,
                    tokenIndexes, reviewIndexes);

            productIndexes.forEach(closer);
            tokenIndexes.forEach(closer);
            reviewIndexes.forEach(closer);


            counter += 1;
            productIndexes = new ArrayList<Index>();
            tokenIndexes = new ArrayList<Index>();
            reviewIndexes = new ArrayList<Index>();
        }
        return counter;
    }


    public static void mergeIndexesAndSave(String dir, HashMap<Character, Integer> tokens_char_freq,
                                           HashMap<Character, Integer> pid_char_freq, int numberOfIndexes)
    {
        createFolder(getCurrentDir(dir));
        createFolder(getPrevDir(dir));
        while(numberOfIndexes > MAX_INDEXES_RAM)
        {
            numberOfIndexes = mergeIndexesOnce(dir, numberOfIndexes);
            deleteFolder(getPrevDir(dir));
            renameDir(dir, currDirName, prevDirName);
            createFolder(getCurrentDir(dir));
        }
        //final merge into dir and with special dictionaries
        ArrayList<Index> productIndexes = new ArrayList<Index>();
        ArrayList<Index> tokenIndexes = new ArrayList<Index>();
        ArrayList<Index> reviewIndexes = new ArrayList<Index>();
        for(int i = 0; i < numberOfIndexes; i++)
        {
            IndexFactory.init_factory(getPrevDir(dir), false, i);
            IndexFactory.get_pid_ind().load_from_disk();
            IndexFactory.get_token_ind().load_from_disk();
            IndexFactory.get_review_ind().load_from_disk();

            productIndexes.add(IndexFactory.get_pid_ind());
            tokenIndexes.add(IndexFactory.get_token_ind());
            reviewIndexes.add(IndexFactory.get_review_ind());
        }

        // do it in the slowIndexWriter
        // pid_char_freq.put(';', IndexFactory.get_pid_ind().getDictionary("pid").getNumRows());

        IndexFactory.init_factory(dir, tokens_char_freq, pid_char_freq, true);
        mergeIndexes(dir, -1, productIndexes, tokenIndexes, reviewIndexes);

        Consumer<Index> closer = (index) -> {
            try {
                index.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        };

        productIndexes.forEach(closer);
        tokenIndexes.forEach(closer);
        reviewIndexes.forEach(closer);

        deleteFolder(getPrevDir(dir));
        deleteFolder(getCurrentDir(dir));
    }


    private static void mergeIdFreqLists(ArrayList<Index> indexes, ArrayList<Integer> pointerIndexes,
                                  ConcatenatedStringDict tokenIdFreqListDict, boolean gap)
    {
        pointerIndexes.forEach((i) -> indexes.get(i).getDictionary("token_id_freq_list").startReading(indexes.get(i).getCurrentPointer()));
        PriorityQueue<Tuple> queue = new PriorityQueue<>(pointerIndexes.size(), Comparator.comparingInt(x -> x.currRevId));
        pointerIndexes.forEach((i) -> queue.add(new Tuple(indexes.get(i).getDictionary("token_id_freq_list").readNext(), i)));
        int prevRevId = 0;
        tokenIdFreqListDict.startAppending();
        while(queue.size() > 0)
        {
            Tuple top = queue.peek();
            int currRevId = top.currRevId;
            int pointerIndex = top.pointerIndex;
            queue.remove(top);
            if(gap)
            {
                tokenIdFreqListDict.append(currRevId - prevRevId);
            }
            else
            {
                tokenIdFreqListDict.append(currRevId);
            }
            ConcatenatedStringDict dct = indexes.get(pointerIndex).getDictionary("token_id_freq_list");
            int freq = dct.readNext();
            tokenIdFreqListDict.append(freq);
            prevRevId = currRevId;
            int nextRevId = dct.readNext();
            if(nextRevId != -1)
            {
                queue.add(new Tuple(nextRevId + currRevId ,pointerIndex));
            }
        }
        tokenIdFreqListDict.finishAppending();
    }
}
