package webdata;

import Index.Index;
import Index.IndexFactory;
import Index.IndexMerger;
import Parser.Review;
import Parser.ReviewsParser;
import Dictionary.ConcatenatedStringDict;
import tools.MetaDataHandler;

import java.io.*;
import java.time.Duration;
import java.time.Instant;
import java.util.*;

import static tools.index_tools.int_to_byte;

public class SlowIndexWriter {
    // constants
    private static final int SCORE_INDEX = 0;
    private static final int HELP_N_INDEX = 1;
    private static final int HELP_D_INDEX = 2;
    private static final int NUM_TOKENS_INDEX = 3;
    private static final int PID_COUNTER_INDEX = 4;
    private static final int INT_SIZE = 4;


    private static final int TOKEN_REV_FREQ_IND = 0;
    private static final int TOKEN_COLLECTION_FREQ_IND = 1;
    private static final int NUM_OF_CONSECUTIVE_REV_IND = 1;


    private String dir;

    private int current_rev_id;
    private int num_of_all_tokens;
    private int num_of_pids;

    private int current_pid_counter;
    private int current_token_counter;

    // === Helper Structures
    // the review's index' values
    private ArrayList<int[]> rev_val;
    // the token's index' values
    private ArrayList<int[]> token_val;
    // for each index of token match list of (id, freq)
    private ArrayList<ArrayList<Integer>> token_id_freq;
    // all the tokens, holding integer represent the order the tokens read;
    private HashMap<String, Integer> tokens_map;
    // all the tokens, sorted by reading them
    private ArrayList<String> tokens_list;
    // holds mapping from the initial indexing of the tokens to the sorted indexing
    private ArrayList<Integer> tokens_indexes;
    // the pids' index' values
    private ArrayList<int[]> pid_val;
    // all the pids, sorted by reading them
    private ArrayList<String> pids;
    // holds mapping from the initial indexing of the pids to the sorted indexing
    private ArrayList<Integer> pids_indexes;
    // the inverse of the sorted indexing og pids, relevant for the review structure
    private int[] pids_indexes_inverse;



    // helper for the compression
    private static HashMap<Character, Integer> tokens_char_freq;
    private static HashMap<Character, Integer> pid_char_freq;

    // dictionaries and indexes
    private ConcatenatedStringDict pid_dict, token_dict, token_id_freq_list_dict;
    private Index review_ind, pid_ind, token_ind;


    private int numberIndex = 0;
    private static final int MAX_REVS_INDEX = 500000;
    /**
     * Given product review data, creates an on disk index
     * inputFile is the path to the file containing the review data
     * dir is the directory in which all index files will be created
     * if the directory does not exist, it should be created
     */
    public void slowWrite(String inputFile, String dir, int max_rev, boolean read_all)
    {
        this.dir = dir;
        // create the directory;
        IndexMerger.createFolder(dir);
        IndexMerger.createFolder(IndexMerger.getPrevDir(dir));

        current_rev_id = 0;
        num_of_all_tokens = 0;

        tokens_char_freq = new HashMap<>();
        pid_char_freq = new HashMap<>();

        ReviewsParser parser = new ReviewsParser(inputFile);
        Review rev = parser.getNextReview();
        int rev_per_index = read_all ? MAX_REVS_INDEX : Math.min(MAX_REVS_INDEX, max_rev);
        for(numberIndex = 0; rev != null && (read_all || MAX_REVS_INDEX * numberIndex < max_rev); numberIndex++)
        {
//            System.out.println(numberIndex);
//            Instant start = Instant.now();
            initialize_structures();
            rev = slowWriteIndex(parser, rev, rev_per_index);
            num_of_pids += current_pid_counter;
//            Instant end = Instant.now();
//            System.out.println("time took " + Duration.between(start, end));
        }
        initialize_structures();
        parser.closeSources();
        System.gc();
        tokens_char_freq.put(';', num_of_all_tokens);
        pid_char_freq.put(';', num_of_pids);
        IndexMerger.mergeIndexesAndSave(dir, tokens_char_freq, pid_char_freq, numberIndex);
        save_meta_data();
    }

    /**
     * create the indexes of the current portion of reviews in the disk
     * @param parser ReviewParser object
     * @param rev Review object
     * @return the last review didn't get into the current index
     */
    private Review slowWriteIndex(ReviewsParser parser, Review rev, int max_rev)
    {
        current_pid_counter = 0;
        current_token_counter = 0;
        String last_pid = "";
        boolean is_new_pid;
        for(int i = 0; i < max_rev && rev != null; i++)
        {
            current_rev_id++;
            num_of_all_tokens += rev.getTokens().size();
            is_new_pid = !last_pid.equals(rev.getProductID());
            last_pid = rev.getProductID();
            if(is_new_pid)
            {
                pids_indexes.add(current_pid_counter);
                current_pid_counter++;
                pids.add(last_pid);
                pid_val.add(new int[]{current_rev_id, 1});
                // update compression structures
                for (int j = 0; j < last_pid.length(); j++)
                    if (!pid_char_freq.containsKey(last_pid.charAt(j)))
                        pid_char_freq.put(last_pid.charAt(j), 1);
                    else
                        pid_char_freq.put(last_pid.charAt(j), pid_char_freq.get(last_pid.charAt(j)) + 1);
            }
            else
                pid_val.get(current_pid_counter - 1)[NUM_OF_CONSECUTIVE_REV_IND] += 1;
            update_review_structures(rev);
            update_token_structures(rev);
            // update_pid_structures(rev);
            rev = parser.getNextReview();
        }
        create_index();
        return rev;
    }

    /**
     * initialize all the helper structures (that relevant for initial index)
     */
    private void initialize_structures()
    {
        rev_val = new ArrayList<>();
        token_val = new ArrayList<>();
        token_id_freq = new ArrayList<>();
        tokens_map = new HashMap<>();
        tokens_list = new ArrayList<>();
        tokens_indexes = new ArrayList<>();
        pid_val = new ArrayList<>();
        pids = new ArrayList<>();
        pids_indexes = new ArrayList<>();
    }

    /**
     * given a review update the review's preprocess structures
     * @param rev review ovject
     */
    private void update_review_structures(Review rev)
    {
        int[] vals = new int[5];
        vals[SCORE_INDEX] = rev.getScore();
        vals[HELP_N_INDEX] = rev.getHelpfulnessNumerator();
        vals[HELP_D_INDEX] = rev.getHelpfulnessDenominator();
        vals[NUM_TOKENS_INDEX] = rev.getTokens().size();
        vals[PID_COUNTER_INDEX] = current_pid_counter - 1;
        rev_val.add(vals);
    }

    /**
     * given a review update the tokens' preprocess structures
     * @param rev review ovject
     */
    private void update_token_structures(Review rev)
    {
        int[] vals;
        ArrayList<String> tokens = rev.getTokens();
        HashMap<String, Integer> freq_per_token = get_freq_per_token(tokens);
        // System.out.println(freq_per_token);
        int current_token_ind, last_id;
        ArrayList<Integer> temp;
        for (String token: freq_per_token.keySet())
        {
            if (!tokens_map.containsKey(token))
            {
                tokens_map.put(token, current_token_counter);
                tokens_indexes.add(current_token_counter);
                current_token_counter++;
                tokens_list.add(token);
                token_val.add(new int[]{1, freq_per_token.get(token)});
                token_id_freq.add(new ArrayList<>());
                token_id_freq.get(token_id_freq.size() - 1).add(current_rev_id);
            }
            else
            {
                current_token_ind = tokens_map.get(token);
                temp = token_id_freq.get(current_token_ind);
                vals = token_val.get(current_token_ind);
                vals[TOKEN_REV_FREQ_IND]++;
                vals[TOKEN_COLLECTION_FREQ_IND] += freq_per_token.get(token);
                last_id = temp.get(temp.size() - 1);
                temp.set(temp.size() - 1, current_rev_id - last_id);
            }
            current_token_ind = tokens_map.get(token);
            temp = token_id_freq.get(current_token_ind);
            temp.add(freq_per_token.get(token));
            temp.add(current_rev_id);
        }
    }

    /**
     * @param tokens array of strings of tokens
     * @return a mapping between string and its frequency in the given array
     */
    private static HashMap<String, Integer> get_freq_per_token(ArrayList<String> tokens)
    {
        HashMap<String, Integer> ans = new HashMap<>();
        for(String s: tokens)
        {
            if (ans.containsKey(s))
                ans.put(s, ans.get(s) + 1);
            else
                ans.put(s, 1);
            // update the freq of each character, relevant for compression
            for (int i = 0; i < s.length(); i++)
            {
                if (!tokens_char_freq.containsKey(s.charAt(i)))
                    tokens_char_freq.put(s.charAt(i), 1);
                else
                    tokens_char_freq.put(s.charAt(i), tokens_char_freq.get(s.charAt(i)) + 1);
            }

        }
        return ans;
    }

    /**
     * create all the indexes assuming finishing updating the helper structuers
     */
    private void create_index()
    {
        IndexFactory.init_factory(IndexMerger.getPrevDir(dir), true, numberIndex);
        pid_dict = IndexFactory.get_pid();
        token_dict = IndexFactory.get_token();
        token_id_freq_list_dict = IndexFactory.get_token_id_freq_list();

        review_ind = IndexFactory.get_review_ind();
        pid_ind = IndexFactory.get_pid_ind();
        token_ind = IndexFactory.get_token_ind();

        sort_tokens_and_pids();

        update_pid_index();
        update_review_index();
        update_token_index();

        pid_ind.save_to_disk();
        review_ind.save_to_disk();
        token_ind.save_to_disk();

        try
        {
            pid_ind.close();
            review_ind.close();
            token_ind.close();
        }catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    /**
     * sort the indexes of pid, token by the match strings
     */
    private void sort_tokens_and_pids()
    {
        pids_indexes.sort((o1, o2) -> pids.get(o1).compareTo(pids.get(o2)));
        pids_indexes_inverse = new int[pids_indexes.size()];
        for (int i = 0; i < pids_indexes.size(); i++)
            pids_indexes_inverse[pids_indexes.get(i)] = i;
        // no need more for quick searching
        tokens_map = null;
        tokens_indexes.sort((o1, o2) -> tokens_list.get(o1).compareTo(tokens_list.get(o2)));
    }

    /**
     * update all the rows in the pid index
     */
    private void update_pid_index()
    {
        int[] id_list;
        int ind;
        for (int i = 0; i < pids.size(); i++)
        {
            ind = pids_indexes.get(i);
            pid_dict.append(pids.get(ind));
            id_list = pid_val.get(ind);
            pid_ind.new_row();
            pid_ind.update_field_in_row("first_id", int_to_byte(id_list[0]));
            pid_ind.update_field_in_row("num_id", int_to_byte(id_list[1]));
            pid_ind.finish_row();
        }
    }

    /**
     * update all the rows in the review index
     */
    private void update_review_index()
    {
        for (int i = 0; i < rev_val.size(); i++)
        {
            review_ind.new_row();
            review_ind.update_field_in_row("score", int_to_byte(rev_val.get(i)[SCORE_INDEX]));
            review_ind.update_field_in_row("helpN", int_to_byte(rev_val.get(i)[HELP_N_INDEX]));
            review_ind.update_field_in_row("helpD", int_to_byte(rev_val.get(i)[HELP_D_INDEX]));
            review_ind.update_field_in_row("num_tokens", int_to_byte(rev_val.get(i)[NUM_TOKENS_INDEX]));
            // the index in rev_val of pid is point to the pid before sorting, therefore using permutation
            review_ind.update_field_in_row("pid", int_to_byte(pids_indexes_inverse[rev_val.get(i)[PID_COUNTER_INDEX]]));
            review_ind.finish_row();
        }
    }

    /**
     * update all the rows in the token index
     */
    private void update_token_index()
    {
        ArrayList<Integer> id_freq_list;
        String current_token;
        int ind;
        for (int i = 0; i < tokens_indexes.size(); i++)
        {
            ind = tokens_indexes.get(i);
            current_token = tokens_list.get(ind);
            token_dict.append(current_token);
            id_freq_list = token_id_freq.get(ind);
            id_freq_list.remove(id_freq_list.size() - 1);
            token_id_freq_list_dict.append(id_freq_list);

            token_ind.new_row();
            token_ind.update_field_in_row("num_reviews_contain_token", int_to_byte(token_val.get(ind)[TOKEN_REV_FREQ_IND]));
            token_ind.update_field_in_row("num_appearances", int_to_byte(token_val.get(ind)[TOKEN_COLLECTION_FREQ_IND]));
            token_ind.finish_row();
        }
    }

    /**
     * save the global variables for the index reader
     */
    private void save_meta_data()
    {
        MetaDataHandler meta = new MetaDataHandler(get_meta_path(), true);
        meta.add_field(current_rev_id);
        meta.add_field(num_of_all_tokens);
        meta.release();
    }

    /**
     * return the path to the meta data
     */
    public String get_meta_path()
    {
        return dir + File.separatorChar + "meta_data.index";
    }

    /**
     * Delete all index files by removing the given directory
     */
    public void removeIndex(String dir) {
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
                currentFile.delete();
            }
        }
        index.delete();
    }
}