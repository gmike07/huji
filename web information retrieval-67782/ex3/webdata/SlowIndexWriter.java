package webdata;

import Index.Index;
import Index.IndexFactory;
import Parser.Review;
import Parser.ReviewsParser;
import Dictionary.ConcatenatedStringDict;

import java.io.*;
import java.util.*;

public class SlowIndexWriter {
    // constants
    private static final int SCORE_INDEX = 0;
    private static final int HELP_N_INDEX = 1;
    private static final int HELP_D_INDEX = 2;
    private static final int NUM_TOKENS_INDEX = 3;
    private static final int INT_SIZE = 4;


    private static final int TOKEN_REV_FREQ_IND = 0;
    private static final int TOKEN_COLLECTION_FREQ_IND = 1;


    private String dir;

    private int current_rev_id;
    private int num_of_all_tokens;

    // review helper structures
    // for each review save [score, helpN, helpD, #tokens]
    private ArrayList<int[]> rev_val;
    // for all rev save the pid;
    private ArrayList<String> rev_pid;
    private HashMap<String, Integer> rev_pid_index;

    // token helper structures
    // for each token save [# reviews containing the token, # appearances]
    private TreeMap<String, int[]> token_val;
    // for each token save list of pairs [id, freq]
    private TreeMap<String, ArrayList<Integer>> token_id_freq;
    private TreeSet<String> sorted_tokens_set;


    // pid helper structures
    private TreeMap<String, ArrayList<Integer>> pid_id_list;
    private TreeSet<String> sorted_pid_set;

    // helper for the compression
    private static HashMap<Character, Integer> tokens_char_freq;
    private static HashMap<Character, Integer> pid_char_freq;

    // dictionaries and indexes
    private ConcatenatedStringDict pid_dict, token_dict, token_id_freq_list_dict, pid_ids_list_dict;
    private Index review_ind, pid_ind, token_ind;

    /**
     * Given product review data, creates an on disk index
     * inputFile is the path to the file containing the review data
     * dir is the directory in which all index files will be created
     * if the directory does not exist, it should be created
     */
    public void slowWrite(String inputFile, String dir)
    {
        this.dir = dir;
        // create the directory;
        File theDir = new File(dir);
        if (!theDir.exists()){
            theDir.mkdirs();
        }

        initialize_structures();
        current_rev_id = 0;
        num_of_all_tokens = 0;

        ReviewsParser parser = new ReviewsParser(inputFile);
        Review rev;
        while((rev = parser.getNextReview()) != null)
        {
            current_rev_id++;
            num_of_all_tokens += rev.getTokens().size();
            update_review_structures(rev);
            update_token_structures(rev);
            update_pid_structures(rev);
        }

        create_index();
        save_meta_data();
    }

    private void initialize_structures()
    {
        rev_val = new ArrayList<>();
        rev_pid = new ArrayList<>();
        rev_pid_index = new HashMap<>();

        token_val = new TreeMap<>();
        token_id_freq = new TreeMap<>();
        sorted_tokens_set = new TreeSet<>();


        pid_id_list = new TreeMap<>();
        sorted_pid_set = new TreeSet<>();

        tokens_char_freq = new HashMap<>();
        pid_char_freq = new HashMap<>();

    }

    private void update_review_structures(Review rev)
    {

        int[] vals = new int[4];
        vals[SCORE_INDEX] = rev.getScore();
        vals[HELP_N_INDEX] = rev.getHelpfulnessNumerator();
        vals[HELP_D_INDEX] = rev.getHelpfulnessDenominator();
        vals[NUM_TOKENS_INDEX] = rev.getTokens().size();
        rev_val.add(vals);

        rev_pid.add(rev.getProductID());
    }


    private void update_token_structures(Review rev)
    {


        int[] vals;
        ArrayList<String> tokens = rev.getTokens();
        HashMap<String, Integer> freq_per_token = get_freq_per_token(tokens);

        for (String token: new HashSet<>(tokens))
        {
            sorted_tokens_set.add(token);

            if (token_val.get(token) == null)
            {
                token_val.put(token, new int[2]);
            }
            vals = token_val.get(token);
            vals[TOKEN_REV_FREQ_IND]++;
            vals[TOKEN_COLLECTION_FREQ_IND] += freq_per_token.get(token);

            int last_id;

            if (token_id_freq.get(token) == null)
            {
                token_id_freq.put(token, new ArrayList<>());
                token_id_freq.get(token).add(current_rev_id);
            }
            // we saving the gaps between the ids, to save space
            else
            {
                last_id = token_id_freq.get(token).get(token_id_freq.get(token).size() - 1);
                token_id_freq.get(token).set(token_id_freq.get(token).size() - 1, current_rev_id - last_id);
            }
            // token_id_freq.get(token).add(new int[]{current_rev_id, freq_per_token.get(token)});

            token_id_freq.get(token).add(freq_per_token.get(token));
            token_id_freq.get(token).add(current_rev_id);
        }
    }


    private static final int NUM_OF_CONSECUTIVE_REV_IND = 1;

    private void update_pid_structures(Review rev)
    {
        String current_pid = rev.getProductID();
        ArrayList<Integer> id_list;
        // NOTE: for each pid, all the rev that on this pid are consecutive, therefore
        // we will save the first rev id and the number of rev on this pid;
        if ((id_list = pid_id_list.get(current_pid)) == null)
        {
            pid_id_list.put(current_pid, new ArrayList<>());
            id_list = pid_id_list.get(current_pid);
            id_list.add(current_rev_id);
            id_list.add(1);
        }
        else
            id_list.set(NUM_OF_CONSECUTIVE_REV_IND, id_list.get(NUM_OF_CONSECUTIVE_REV_IND) + 1);
        // id_list.add(current_rev_id);
    }

    private static HashMap<String, Integer> get_freq_per_token(ArrayList<String> tokens)
    {
        HashMap<String, Integer> ans = new HashMap<>();
        for(String s: tokens)
        {
            if (ans.containsKey(s))
            {
                ans.put(s, ans.get(s) + 1);
            }
            else
            {
                ans.put(s, 1);
            }
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

    private void create_index()
    {
        tokens_char_freq.put(';', num_of_all_tokens);
        pid_char_freq.put(';', pid_id_list.size());
        update_pid_freq();
        IndexFactory.init_factory(dir, tokens_char_freq, pid_char_freq, true);

        pid_dict = IndexFactory.get_pid();
        token_dict = IndexFactory.get_token();
        token_id_freq_list_dict = IndexFactory.get_token_id_freq_list();
        pid_ids_list_dict = IndexFactory.get_pid_ids_list();

        review_ind = IndexFactory.get_review_ind();
        pid_ind = IndexFactory.get_pid_ind();
        token_ind = IndexFactory.get_token_ind();

        update_pid_index();
        update_review_index();
        update_token_index();

        pid_ind.save_to_disk();
        review_ind.save_to_disk();
        token_ind.save_to_disk();
    }

    private void update_pid_freq()
    {
        for (String pid_st: pid_id_list.keySet())
        {
            // update the frequency for compression
            for (int i = 0; i < pid_st.length(); i++)
            {
                if (!pid_char_freq.containsKey(pid_st.charAt(i)))
                    pid_char_freq.put(pid_st.charAt(i), 1);
                else
                    pid_char_freq.put(pid_st.charAt(i), pid_char_freq.get(pid_st.charAt(i)) + 1);
            }
        }
    }

    private void update_pid_index()
    {
        int current_pid_num = 0;
        byte[] current_id = new byte[INT_SIZE];
        for (String pid_st: pid_id_list.keySet())
        {

            // NOTE: relevant for building the review index
            rev_pid_index.put(pid_st, current_pid_num);
            pid_dict.append(pid_st);
            // update the list of id's per pid
            ArrayList<Integer> id_list = pid_id_list.get(pid_st);
            pid_ids_list_dict.append(id_list);
//            pid_ind.new_row();
//            pid_ind.update_field_in_row("pid", tools.index_tools.int_to_byte(current_pid_num));
//            pid_ind.update_field_in_row("pid_ids_list", tools.index_tools.int_to_byte(current_pid_num));
//            pid_ind.finish_row();

            current_pid_num++;
        }
    }

    private void update_review_index()
    {
        int current_pid_index;
        for(int i = 0; i < rev_val.size(); i++)
        {
            review_ind.new_row();
            current_pid_index = rev_pid_index.get(rev_pid.get(i));
            review_ind.update_field_in_row("pid", tools.index_tools.int_to_byte(current_pid_index));
            // NOTE: the function knows how much bytes to read (score is ONE byte while we sent 4 bytes
            review_ind.update_field_in_row("score", tools.index_tools.int_to_byte(rev_val.get(i)[SCORE_INDEX]));
            review_ind.update_field_in_row("helpN", tools.index_tools.int_to_byte(rev_val.get(i)[HELP_N_INDEX]));
            review_ind.update_field_in_row("helpD", tools.index_tools.int_to_byte(rev_val.get(i)[HELP_D_INDEX]));
            review_ind.update_field_in_row("num_tokens", tools.index_tools.int_to_byte(rev_val.get(i)[NUM_TOKENS_INDEX]));
            review_ind.finish_row();
        }
    }

    private void update_token_index()
    {
        int token_num = 0;
        for (String token: token_val.keySet())
        {
            token_dict.append(token);
            ArrayList<Integer> id_freq_list = token_id_freq.get(token);
            // NOTE: the last element is the last rev id (not the gap), we remove it
            id_freq_list.remove(id_freq_list.size() - 1);
            token_id_freq_list_dict.append(id_freq_list);
            token_ind.new_row();
            // token_ind.update_field_in_row("token", tools.index_tools.int_to_byte(token_num));
            // token_ind.update_field_in_row("token_id_freq_list", tools.index_tools.int_to_byte(token_num));
            token_ind.update_field_in_row("num_reviews_contain_token", tools.index_tools.int_to_byte(token_val.get(token)[TOKEN_REV_FREQ_IND]));
            token_ind.update_field_in_row("num_appearances", tools.index_tools.int_to_byte(token_val.get(token)[TOKEN_COLLECTION_FREQ_IND]));
            token_ind.finish_row();

            token_num++;
        }
    }


    private void save_meta_data()
    {
        String path = get_meta_path();
        byte[] current_int = new byte[INT_SIZE];
        FileOutputStream writer;
        try {
            writer = new FileOutputStream(path);
            tools.index_tools.int_to_byte(current_int, current_rev_id);
            writer.write(current_int);
            tools.index_tools.int_to_byte(current_int, num_of_all_tokens);
            writer.write(current_int);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public String get_meta_path()
    {
        return dir + File.separatorChar + "meta_data.index";
    }



    // TODO: complete the removeIndex
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