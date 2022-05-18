package Index;

import CompressionV2.*;
import Dictionary.ConcatDict;
import Dictionary.ConcatenatedStringDict;
import Dictionary.DictOutputType;
import Dictionary.FrontCoding;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashMap;

public class IndexFactory
{
    //the string directory path
    public static String dir;
    //the dictionaries we create
    private static ConcatenatedStringDict pid, token, token_id_freq_list;
    //the indexes we create
    private static Index review_ind, pid_ind, token_ind;
    //int compressions
    private static AbstractIntegerCompression token_id_freq_int_comp;
    //string compressions
    private static AbstractStringCompression token_string_comp, pid_string_comp;

    /**
     * @param p_dir the dir folder
     * @param tokens_char_freq the freqs of chars in tokens
     * @param pid_char_freq the freqs of chars in pid
     * @param for_writing should we write or read
     */
    public static void init_factory(String p_dir, HashMap<Character, Integer> tokens_char_freq,
                                    HashMap<Character, Integer> pid_char_freq, boolean for_writing)
    {
        dir = p_dir;

        token_id_freq_int_comp = new DeltaCompression();
        String path = dir + File.separatorChar;
        if (for_writing)
        {
            token_string_comp = new HuffmanCompression(tokens_char_freq,  path + "token_compress_meta.compress");
            pid_string_comp = new HuffmanCompression(pid_char_freq, path + "pid_compress_meta.compress");
        }
        else
        {
            token_string_comp = new HuffmanCompression(path + "token_compress_meta.compress");
            pid_string_comp = new HuffmanCompression(path + "pid_compress_meta.compress");
        }

        try {
            pid = new ConcatDict(dir,"pid", for_writing, DictOutputType.String_out, null, pid_string_comp);
            // tokens sorted by alphabet
            token = new ConcatDict(dir, "token", for_writing, DictOutputType.String_out, null,
                    token_string_comp);
            // list of (id, freq) per token sorted by id
            token_id_freq_list = new ConcatDict(dir, "token_id_freq_list", for_writing,
                    DictOutputType.ArrayList_out, token_id_freq_int_comp, null);
        } catch (IOException e) {
            e.printStackTrace();
        }

        review_ind = new Index("review", dir, false, null, true);
        pid_ind = new Index("pid", dir, false, null, true);
        token_ind = new Index("token", dir, false, null, true);
        addFieldsIndexes();
    }


    public static void init_factory(String p_dir, boolean for_writing, int index)
    {
        dir = p_dir;

        token_id_freq_int_comp = new DeltaCompression();

        token_string_comp = new NoStringCompression();
        pid_string_comp = new NoStringCompression();

        try {
            pid = new ConcatDict(dir, index + "_pid", for_writing, DictOutputType.String_out, null,
                    pid_string_comp, 0);
            // tokens sorted by alphabet
            token = new ConcatDict(dir, index + "_token", for_writing, DictOutputType.String_out, null,
                    token_string_comp, 0);
            // list of (id, freq) per token sorted by id
            token_id_freq_list = new ConcatDict(dir, index + "_token_id_freq_list", for_writing,
                    DictOutputType.ArrayList_out, token_id_freq_int_comp, null, 0);
            // list of id's per pid sorted by id
        } catch (IOException e) {
            e.printStackTrace();
        }

        review_ind = new Index(index + "_review", dir, false, null, true);
        pid_ind = new Index(index + "_pid", dir, false, null, true);
        token_ind = new Index(index + "_token", dir, false, null, true);
        addFieldsIndexes();
    }

    private static void addFieldsIndexes()
    {
        // === review ===
        review_ind.add_field("pid", 4);
        review_ind.add_dictionary("pid", pid);

        review_ind.add_field("score", 1);
        review_ind.add_field("helpN", 2);
        review_ind.add_field("helpD", 2);
        review_ind.add_field("num_tokens", 2);

        // === pid ===
        pid_ind.add_dictionary("pid", pid);

        pid_ind.add_field("first_id", 4);
        pid_ind.add_field("num_id", 4);

        // === token ===
        token_ind.add_dictionary("token", token);

        token_ind.add_dictionary("token_id_freq_list", token_id_freq_list);

        token_ind.add_field("num_reviews_contain_token", 4);
        token_ind.add_field("num_appearances", 4);
    }

    /**
     * @return the review index
     */
    public static Index get_review_ind() {
        return review_ind;
    }


    /**
     * @return the pid index
     */
    public static Index get_pid_ind() {
        return pid_ind;
    }


    /**
     * @return the token index
     */
    public static Index get_token_ind() {
        return token_ind;
    }


    /**
     * @return the pid dict
     */
    public static ConcatenatedStringDict get_pid() {
        return pid;
    }

    /**
     * @return the token dict
     */
    public static ConcatenatedStringDict get_token() {
        return token;
    }

    /**
     * @return the id freq list dict
     */
    public static ConcatenatedStringDict get_token_id_freq_list() {
        return token_id_freq_list;
    }


    public static void clear()
    {
        review_ind = null;
        pid_ind = null;
        token_ind = null;
        pid = null;
        token = null;
        token_id_freq_list = null;
    }

}
