package webdata;

import Index.Index;
import Index.IndexFactory;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.Enumeration;
import java.util.Vector;

public class IndexReader
{
    private static final int INT_SIZE = 4;
    private static final int NOT_EXISTS = -1;
    private String dir;
    private Index review_ind, pid_ind, token_ind;

    private int num_of_review, num_of_all_tokens;

    /**
     * Creates an IndexReader which will read from the given directory
     */
    public IndexReader(String dir)
    {
        this.dir = dir;
        IndexFactory.init_factory(dir, null, null, false);
        review_ind = IndexFactory.get_review_ind();
        pid_ind = IndexFactory.get_pid_ind();
        token_ind = IndexFactory.get_token_ind();

        review_ind.load_from_disk();
        pid_ind.load_from_disk();
        token_ind.load_from_disk();

        read_meta_data();
    }

    /**
     * Returns the product identifier for the given review
     * Returns null if there is no review with the given identifier
     */
    public String getProductId(int reviewId)
    {
        if (!is_valid_review_id(reviewId))
            return null;
        return new String(review_ind.get_dict_field("pid", reviewId - 1));
    }

    /**
     * Returns the score for a given review
     * Returns -1 if there is no review with the given identifier
     */
    public int getReviewScore(int reviewId)
    {
        if (!is_valid_review_id(reviewId))
            return NOT_EXISTS;
        return tools.index_tools.byte_to_int(review_ind.get_field("score", reviewId - 1));
    }

    /**
     * Returns the numerator for the helpfulness of a given review
     * Returns -1 if there is no review with the given identifier
     */
    public int getReviewHelpfulnessNumerator(int reviewId)
    {
        if (!is_valid_review_id(reviewId))
            return NOT_EXISTS;
        byte[] helpN = review_ind.get_field("helpN", reviewId - 1);
        if (helpN == null)
            return NOT_EXISTS;
        return tools.index_tools.byte_to_int(helpN);
    }

    /**
     * Returns the denominator for the helpfulness of a given review
     * Returns -1 if there is no review with the given identifier
     */
    public int getReviewHelpfulnessDenominator(int reviewId)
    {
        if (!is_valid_review_id(reviewId))
            return NOT_EXISTS;
        byte[] helpD = review_ind.get_field("helpD", reviewId - 1);
        if (helpD == null)
            return NOT_EXISTS;
        return tools.index_tools.byte_to_int(helpD);
    }

    /**
     * Returns the number of tokens in a given review
     * Returns -1 if there is no review with the given identifier
     */
    public int getReviewLength(int reviewId)
    {
        if (!is_valid_review_id(reviewId))
            return NOT_EXISTS;
        return tools.index_tools.byte_to_int(review_ind.get_field("num_tokens", reviewId - 1));
    }

    /**
     * Return the number of reviews containing a given token (i.e., word)
     * Returns 0 if there are no reviews containing this token
     */
    public int getTokenFrequency(String token)
    {
        byte[] freq = token_ind.get_field_by_dict("token", "num_reviews_contain_token", token.toLowerCase().getBytes(StandardCharsets.UTF_8));
        if (freq == null)
            return 0;
        return tools.index_tools.byte_to_int(freq);
    }

    /**
     * Return the number of times that a given token (i.e., word) appears in
     * the reviews indexed
     * Returns 0 if there are no reviews containing this token
     */
    public int getTokenCollectionFrequency(String token)
    {
        byte[] freq = token_ind.get_field_by_dict("token", "num_appearances", token.toLowerCase().getBytes(StandardCharsets.UTF_8));
        if (freq == null)
            return 0;
        return tools.index_tools.byte_to_int(freq);
    }

    /**
     * Return a series of integers of the form id-1, freq-1, id-2, freq-2, ... such
     * that id-n is the n-th review containing the given token and freq-n is the
     * number of times that the token appears in review id-n
     * Only return ids of reviews that include the token
     * Note that the integers should be sorted by id
     *
     * Returns an empty Enumeration if there are no reviews containing this token
     */
     public Enumeration<Integer> getReviewsWithToken(String token)
     {
         // int i = token_ind.get_index_by_string(word_in_dict);
         byte[] current_list = token_ind.get_synced_dict_field_by_dict("token", "token_id_freq_list", token.toLowerCase().getBytes(StandardCharsets.UTF_8));
         Vector<Integer> ans = new Vector<>();
         if (current_list == null)
             return ans.elements();
         int current_id = 0;
         for(int i = 0; i < (current_list.length / INT_SIZE) / 2; i++)
         {
             current_id += tools.index_tools.byte_to_int(current_list, 2 * i * INT_SIZE);
             ans.add(current_id);
             // add the freq
             ans.add(tools.index_tools.byte_to_int(current_list, (2 * i + 1) * INT_SIZE));
         }
         return ans.elements();
     }

     /**
     * Return the number of product reviews available in the system
     */
    public int getNumberOfReviews()
    {
        return num_of_review;
    }

    /**
     * Return the number of number of tokens in the system
     * (Tokens should be counted as many times as they appear)
     */
    public int getTokenSizeOfReviews()
    {
        return num_of_all_tokens;
    }

    /**
     * Return the ids of the reviews for a given product identifier
     * Note that the integers returned should be sorted by id
     *
     * Returns an empty Enumeration if there are no reviews for this product
     */
    public Enumeration<Integer> getProductReviews(String productId)
    {
        byte[] productIdByte = productId.getBytes(StandardCharsets.UTF_8);
        byte[] first_id_lst = pid_ind.get_field_by_dict("pid", "first_id", productIdByte);
        byte[] num_id_lst = pid_ind.get_field_by_dict("pid", "num_id", productIdByte);
        Vector<Integer> ans = new Vector<>();
        if (first_id_lst == null || num_id_lst == null)
            return ans.elements();

        int first_id = tools.index_tools.byte_to_int(first_id_lst, 0);
        int num_of_rev = tools.index_tools.byte_to_int(num_id_lst, 0);
        for (int i = 0; i < num_of_rev; i++)
            ans.add(first_id + i);
//        for(int i = 0; i < (current_list.length / INT_SIZE); i++)
//        {
//            ans.add(tools.index_tools.byte_to_int(current_list, i * INT_SIZE));
//        }
        return ans.elements();
    }


    private void read_meta_data()
    {
        String path = get_meta_path();
        byte[] current_int = new byte[INT_SIZE];
        FileInputStream reader;
        try {
            reader = new FileInputStream(path);
            reader.read(current_int);
            num_of_review = tools.index_tools.byte_to_int(current_int);
            reader.read(current_int);
            num_of_all_tokens = tools.index_tools.byte_to_int(current_int);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * @return the path to the metadata of the index
     */
    private String get_meta_path()
    {
        return dir + File.separatorChar + "meta_data.index";
    }

    /**
     * @param review_id integer
     * @return true iff the review id is valid
     */
    private boolean is_valid_review_id(int review_id)
    {
        return review_id <= num_of_review && review_id > 0;
    }

}
