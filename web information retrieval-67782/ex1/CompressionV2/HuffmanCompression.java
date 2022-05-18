package CompressionV2;

import java.io.*;
import java.util.*;

public class HuffmanCompression extends AbstractStringCompression
{
    // the encoding to each char
    private HashMap<Character, String> encodingMapping;
    // the string to save in file
    private String toCompress;
    // the letters in each depth
    private String[] lettersAtDepth;
    // the first code in each depth
    private int[] firstCodeAtDepth;


    /**
     * encodes the char to the stream
     * @param stream the stream to write to
     * @param c the string to encode
     * @throws IOException if failed to write
     */
    @Override
    public void encodeChar(OutputStreamHelper stream, char c) throws IOException
    {
        String code = encodingMapping.get(c);
        for(int j = 0; j < code.length(); j++)
        {
            if(code.charAt(j) == '1')
            {
                writeBit(stream, 1);
            }
            else
            {
                writeBit(stream, 0);
            }
        }
    }

    /**
     * @param stream the stream to read from
     * @return the decoded char from the stream
     * @throws IOException if failed to read
     */
    @Override
    public char decodeChar(InputStreamHelper stream) throws IOException {
        int d = advanceBit(stream);
        for(int i = 1;; i++)
        {
            if(lettersAtDepth[i].length() == 0)
            {
                d = 2 * d + advanceBit(stream);
                continue;
            }
            if(d <= firstCodeAtDepth[i] + lettersAtDepth[i].length() - 1)
            {
                return lettersAtDepth[i].charAt(d - firstCodeAtDepth[i]);
            }
            d = 2 * d + advanceBit(stream);
        }
    }

    /**
     * saves the data in dir
     * @param dir the dir to save in
     * @throws IOException if failed to write
     */
    @Override
    public void save(String dir) throws IOException {
        FileOutputStream f = new FileOutputStream(dir);
        f.write(toCompress.getBytes());
        f.close();
    }

    /**
     * loads the data in dir
     * @param dir the dir to load from
     * @throws IOException if failed to read
     */
    @Override
    public void load(String dir) throws IOException {
        BufferedReader f = new BufferedReader(new InputStreamReader(new FileInputStream(dir)));
        toCompress = f.readLine();
        f.close();
        int splitIndex = toCompress.indexOf('#');
        String letters = toCompress.substring(splitIndex + 1);
        String[] depths = toCompress.substring(0, splitIndex - 1).split(",");
        lettersAtDepth = new String[depths.length];
        firstCodeAtDepth = new int[depths.length];
        for(int i = 0; i < depths.length; i++)
        {
            int numLettersAtDepth = Integer.parseInt(depths[i]);
            lettersAtDepth[i] = letters.substring(0, numLettersAtDepth);
            if(i == 0)
            {
                firstCodeAtDepth[i] = 0;
            }
            else
            {
                firstCodeAtDepth[i] = 2 * (firstCodeAtDepth[i - 1] + lettersAtDepth[i - 1].length());
            }
            letters = letters.substring(numLettersAtDepth);
        }
    }

    class Node
    {
        //the value fo the node
        char key;
        //the left child of the curr node
        Node left = null;
        //the right child of the curr node
        Node right = null;
        //the depth of the curr node
        int depth = 0;
        //the freq of the curr node
        int freq;

        /**
         * @param key the value of the node
         * @param freq the freq of the node
         */
        Node(char key, int freq)
        {
            this.key = key;
            this.freq = freq;
        }

        /**
         * @param freq the freq of the node
         * @param left the left child of the node
         * @param right the right child of the node
         */
        Node(int freq, Node left, Node right)
        {
            this.freq = freq;
            this.left = left;
            this.right = right;
        }
    }

    /**
     * builds the compression and saves it
     * @param freqs a mapping of the chars to freqs
     * @param path the path to save the compression data in
     */
    public HuffmanCompression(HashMap<Character, Integer> freqs, String path)
    {
        this.encodingMapping = createCanonicalHuffmanCode(freqs);
        try {
            save(path);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * loads the compression
     * @param dir the path from which to load the compression
     */
    public HuffmanCompression(String dir){
        try {
            load(dir);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * @param freqs a mapping of the chars to freqs
     * @return a head node of the huffman tree
     */
    private Node createHuffmanTree(HashMap<Character, Integer> freqs)
    {
        Comparator<Node> c = Comparator.comparingInt(o -> o.freq);
        PriorityQueue<Node> minHeap = new PriorityQueue<>(c);
        for(Character character: freqs.keySet())
        {
            minHeap.add(new Node(character, freqs.get(character)));
        }
        while(minHeap.size() > 1)
        {
            Node left = minHeap.remove();
            Node right = minHeap.remove();
            minHeap.add(new Node(left.freq + right.freq, left, right));
        }
        return minHeap.peek();
    }

    /**
     * @param endNodeList the list of the end nodes to add to
     * @param curr the current node in the recursive call
     * @param depth the current depth
     * updates all depths and saves all end nodes in list
     */
    private void updateEndNodes(List<Node> endNodeList, Node curr, int depth)
    {
        if(curr == null)
        {
            return;
        }
        curr.depth =  depth;
        //end node
        if(curr.left == null && curr.right == null)
        {
            endNodeList.add(curr);
        }
        updateEndNodes(endNodeList, curr.left, depth + 1);
        updateEndNodes(endNodeList, curr.right, depth + 1);
    }

    /**
     * @param freqs a mapping of the chars to freqs
     * @return a mapping of the chars to the encoded string of it
     */
    private HashMap<Character, String> createCanonicalHuffmanCode(HashMap<Character, Integer> freqs)
    {
        Node head = createHuffmanTree(freqs);
        ArrayList<Node> endNodes = new ArrayList<>();
        updateEndNodes(endNodes, head, 0);
        Comparator<Node> c = Comparator.comparingInt(o -> o.depth);
        endNodes.sort(c);
        HashMap<Character, String> mapping = new HashMap<>();

        int currentEncoding = -1;
        int lastDepth = -1;
        StringBuilder letters = new StringBuilder();
        int maxDepth = endNodes.get(endNodes.size() - 1).depth;

        int[] depthCount = new int[maxDepth + 1];
        for(int i = 0; i < depthCount.length; i++)
        {
            depthCount[i] = 0;
        }

        for(Node n: endNodes)
        {
            letters.append(n.key);
            currentEncoding = (1 << (n.depth - lastDepth)) * (currentEncoding + 1);
            StringBuilder code = new StringBuilder(Integer.toBinaryString(currentEncoding));
            while(code.length() < n.depth)
            {
                code.insert(0, "0");
            }
            mapping.put(n.key, code.toString());
            depthCount[n.depth]++;
            lastDepth = n.depth;
        }
        StringBuilder depths = new StringBuilder();
        for (int i1 : depthCount) {
            depths.append(i1).append(",");
        }
        toCompress = depths + "#" + letters;
        return mapping;
    }
}
