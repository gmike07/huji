package webdata;

import java.util.*;

public class ReviewSearch {
    private IndexReader reader;
    private int corpus_size;
    private final static double LAMBDA = 0.5;

    /**
     * Constructor
     */
    public ReviewSearch(IndexReader iReader)
    {
        reader = iReader;
        corpus_size = reader.getTokenSizeOfReviews();
    }

    private <T> void updateQueryTokens(Enumeration<T> query, Collection<T> tokens)
    {
        while(query.hasMoreElements())
        {
            tokens.add(query.nextElement());
        }
    }

    private double vectorScore(int id,
                               HashMap<Integer, HashMap<String, Double>> idMapping,
                               HashMap<String, Double> queryMapping)
    {
        double score = 0;
        for(String token: idMapping.get(id).keySet())
        {
            score += idMapping.get(id).get(token) * queryMapping.get(token);
        }
        return score;
    }


    private void normalizeVectors(HashMap<String, Double> queryMapping)
    {
        double normSquared = 0;
        for(String token: queryMapping.keySet())
        {
            double val = queryMapping.get(token);
            normSquared += val * val;
        }

        double norm = Math.sqrt(normSquared);
        for(String token: queryMapping.keySet())
        {
            queryMapping.put(token, queryMapping.get(token) / norm);
        }
    }

    /**
     * Returns a list of the id-s of the k most highly ranked reviews for the
     * given query, using the vector space ranking function lnn.ltc (using the
     * SMART notation)
     * The list should be sorted by the ranking
     */
    public Enumeration<Integer> vectorSpaceSearch(Enumeration<String> query, int k) {
        //doc: 1 + log10(tf t, d) = 1 + log10(freq of token t in doc)
        //query: Norm((1 + log10(tf t,d)) * log10(N / df t)) =
        // Norm((1 + log10(freq of token t in doc)) * log10(Number of reviews / number of documents
        // containing t))
        ArrayList<String> queryTokensList = new ArrayList<>();
        updateQueryTokens(query, queryTokensList);

        // doc score: id --> token --> freq = 1 + log10(tf t, d)
        HashMap<Integer, HashMap<String, Double>> idMapping = new HashMap<>();

        HashMap<String, Double> queryMapping = new HashMap<>();
        for(String token: queryTokensList)
        {
            queryMapping.put(token, queryMapping.getOrDefault(token, 0.0) + 1.0);
        }
        for(String token : queryMapping.keySet())
        {
            Enumeration<Integer> idFreq = reader.getReviewsWithToken(token);
            int numReviewsWithToken = 0;
            // calculate 1 + Math.log10(tf t, d)
            while(idFreq.hasMoreElements())
            {
                int id = idFreq.nextElement();
                int freq = idFreq.nextElement();
                if(!idMapping.containsKey(id))
                {
                    idMapping.put(id, new HashMap<>());
                }
                idMapping.get(id).put(token, 1 + Math.log10(freq));
                numReviewsWithToken += 1;
            }
            // calculate l + n
            double tokenScore = 0;
            if (numReviewsWithToken != 0)
                tokenScore = Math.log10((double)reader.getNumberOfReviews() / numReviewsWithToken);
            queryMapping.put(token, (1 + Math.log10(queryMapping.get(token))) * tokenScore);
        }
        // calculate c
        normalizeVectors(queryMapping);
        return Collections.enumeration(topK(idMapping.keySet(),
                (id) -> vectorScore(id, idMapping, queryMapping), k));
    }

    /**
     * Returns a list of the id-s of the k most highly ranked reviews for the
     * given query, using the language model ranking function, smoothed using a
     * mixture model with the given value of lambda
     * The list should be sorted by the ranking
     */
    public Enumeration<Integer> languageModelSearch(Enumeration<String> query,
                                                    double lambda, int k)
    {
        //a: id --> token --> review model score
        //b: token --> corpus model score
        //score = 1; for term in query: score *= (lambda) * a(id, token) + (1-lambda) * b(token);
        //notice if a(id,token) doesn't exist return 0
        ArrayList<String> all_tokens = new ArrayList<>();
        HashMap<Integer, HashMap<String, Double>> review_model_score = new HashMap<>();
        HashMap<String, Double> corpus_model_score = new HashMap<>();
        updateQueryTokens(query, all_tokens);
        int id, freq;
        for (String token: all_tokens)
        {
            Enumeration<Integer> id_freq_list = reader.getReviewsWithToken(token);
            while (id_freq_list.hasMoreElements())
            {
                id = id_freq_list.nextElement();
                freq = id_freq_list.nextElement();
                if (!review_model_score.containsKey(id))
                {
                    review_model_score.put(id, new HashMap<>());
                }
                review_model_score.get(id).put(token, (double)freq / reader.getReviewLength(id));
            }
            corpus_model_score.put(token, (double)reader.getTokenCollectionFrequency(token) / corpus_size);
        }
        return Collections.enumeration(topK(review_model_score.keySet(),
                (id1) -> calc_lang_model_score(id1, all_tokens, review_model_score, corpus_model_score, lambda), k));
    }

    private double calc_lang_model_score(int id, ArrayList<String> query, HashMap<Integer, HashMap<String, Double>> a,
                                         HashMap<String, Double> b, double lambda)
    {
        double score = 1;
        for (String token: query)
        {
            score *= lambda * a.get(id).getOrDefault(token, 0.0) + (1 - lambda) * b.get(token);
        }
        return score;
    }


    private double calcScorePid(String pid)
    {
        Collection<Integer> reviewIds = new ArrayList<>();
        updateQueryTokens(reader.getProductReviews(pid), reviewIds);
        double score = 0;
        int N = reviewIds.size();
        // E[help * score] * lambda + E[score] * (1 - lambda)
        for(int id : reviewIds)
        {
            double currentScore = reader.getReviewScore(id);
            double currentHelpfulness = reader.getReviewHelpfulnessNumerator(id);
            double helper = reader.getReviewHelpfulnessDenominator(id);
            currentHelpfulness = helper == 0 ? 0 : currentHelpfulness / helper;
            score += (LAMBDA * currentHelpfulness + (1 - LAMBDA)) * currentScore / 5.0;
        }
        score /= N;
        return score;
    }

    /**
     * Returns a list of the id-s of the k most highly ranked productIds for the
     * given query using a function of your choice
     * The list should be sorted by the ranking
     */
    public Collection<String> productSearch(Enumeration<String> query, int k)
    {
        //mean(helpfulness * score) * sum(tf_idf)
        ArrayList<String> all_tokens = new ArrayList<>();
        HashMap<Integer, HashMap<String, Double>> review_model_score = new HashMap<>();
        HashMap<String, Double> corpus_model_score = new HashMap<>();
        updateQueryTokens(query, all_tokens);
        int id, freq;
        for (String token: all_tokens)
        {
            Enumeration<Integer> id_freq_list = reader.getReviewsWithToken(token);
            while (id_freq_list.hasMoreElements())
            {
                id = id_freq_list.nextElement();
                freq = id_freq_list.nextElement();
                if (!review_model_score.containsKey(id))
                {
                    review_model_score.put(id, new HashMap<>());
                }
                review_model_score.get(id).put(token, (double)freq / reader.getReviewLength(id));
            }
            corpus_model_score.put(token, (double)reader.getTokenCollectionFrequency(token) / corpus_size);
        }

        ArrayList<Pair<Integer, Double>> idScore = new ArrayList<>();
        review_model_score.keySet().forEach((id1) -> idScore.add(new Pair<>(id1,
                calc_lang_model_score(id1, all_tokens, review_model_score, corpus_model_score, 0.5))));
        idScore.sort(ReviewSearch::comparePairs);

        Set<String> pids = new HashSet<>();
        for(int i = 0; i < idScore.size() && pids.size() < k; i++)
        {
            pids.add(reader.getProductId(idScore.get(i).key));
        }

        return topK(pids, this::calcScorePid, k);
    }



    @FunctionalInterface
    public interface ScoringFunction<T> {
        double apply(T t);
    }

    class Pair<K extends Comparable, V extends Comparable>
    {
        K key;
        V value;

        Pair(K _key, V _value)
        {
            key = _key;
            value = _value;
        }
    }



    private static <T extends Comparable> int comparePairs(Pair<T, Double> o1, Pair<T, Double> o2)
    {
        int valueComp = o1.value.compareTo(o2.value);
        if(valueComp != 0) //not equal score
        {
            return -valueComp; //sorted from biggest to smallest
        }
        //break tie by smallest id
        return o1.key.compareTo(o2.key);
    }


    private <T extends Comparable> List<T> topK(Set<T> ids, ScoringFunction<T> scoreFunction, int k)
    {

        ArrayList<Pair<T, Double>> scoreMapping = new ArrayList<>();
        ids.forEach((id) -> scoreMapping.add(new Pair<>(id, scoreFunction.apply(id))));
        scoreMapping.sort(ReviewSearch::comparePairs);

        ArrayList<T> topKIds = new ArrayList<>();
        for(int i = 0; i < scoreMapping.size() && i < k; i++)
        {
            topKIds.add(scoreMapping.get(i).key);
        }
        return topKIds;
    }
}
