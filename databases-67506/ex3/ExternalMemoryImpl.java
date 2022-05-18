package Join;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;

public class ExternalMemoryImpl extends IExternalMemory {
    private static final int CHAR_LENGTH = 2;
    private static final int BLOCK_SIZE = 4096;
    private static final int JOINED_TUPLE_LENGTH = 83;
    private static final int TUPLE_LENGTH = 53; //the amount of char's per line
    private static final int TUPLE_SIZE = CHAR_LENGTH * TUPLE_LENGTH; //java char = 2 bytes not 1 like in amazing c
    private static final int TUPLES_PER_BLOCK = BLOCK_SIZE / TUPLE_SIZE;
    private static final int BLOCKS_IN_BUFFER = 10000; //the buffer size, 40 mb


    /**
     * recieve an input file and sort to small files with the size of the buffer
     * @param in input file
     * @param out temporary output files
     * @return the amount of files created ;
     * @throws IOException shit
     */
    private static int firstPartSort(BufferedReader in, String out, boolean isSelect, String pattern)
            throws IOException {
        String s = in.readLine();
        ArrayList<String> buffer = new ArrayList<>();
        int fileCounter = 0;
        while(s != null){
            while(s != null && buffer.size() + 1 <= BLOCKS_IN_BUFFER * TUPLES_PER_BLOCK){
                if(!isSelect || isFittingSelect(s, pattern))
                    buffer.add(s);
                s = in.readLine();
            }
            Collections.sort(buffer);
            BufferedWriter writer =
                    new BufferedWriter(new FileWriter(Paths.get(out, fileCounter + ".txt").toString()));
            writeToFile(buffer, writer);
            writer.close();
            buffer.clear();
            fileCounter++;
        }
        return fileCounter;
    }

    /**
     * returns the smallest (lexicographic) line from the given array
     * @param strings array of strings
     * @return the smallest (lexicographic) line from the given array
     */
    private static int minimumIndex(String[] strings){
        int bestIndex = -1;
        for(int i = 0; i < strings.length; i++) {
            if(strings[i] == null)
                continue;
            if (bestIndex == -1 || strings[i].compareTo(strings[bestIndex]) < 0)
                bestIndex = i;
        }
        return bestIndex;
    }

    /**
     * get the sorted temp files (determined by base name + index) and write to out
     * sorted union of all the files;
     * @param in base name for input files;
     * @param out output file;
     * @param length amount of temp files;
     * @throws IOException shit
     */
    private static void secondPartSort(String in, String out, int length) throws IOException {
        String[] strings = new String[length];
        BufferedWriter writer = new BufferedWriter(new FileWriter(out));
        ArrayList<String> outputBlock = new ArrayList<>();
        BufferedReader[] files = new BufferedReader[length];
        int number = length;
        for(int i = 0; i < length; i++) {
            files[i] = new BufferedReader(new FileReader(Paths.get(in, i + ".txt").toString()));
            strings[i] = files[i].readLine();
            number -= (strings[i] == null) ? 1 : 0;
        }
        while(number != 0){
            int minimum = minimumIndex(strings);
            addToOutput(outputBlock, strings[minimum], TUPLE_LENGTH, writer);
            strings[minimum] = files[minimum].readLine();
            number -= (strings[minimum] == null) ? 1 : 0;
        }
        writeToFile(outputBlock, writer);
        for(BufferedReader r : files)
            r.close();
        writer.close();
    }

    /**
     * @param in the input file
     * @param out the output file
     * @param tmpPath the place to create helper files
     * @param isSelect if true then add only those who fit selection
     * @param s the string to check the selection with
     * @throws IOException shit
     */
    private static void sortHelper (String in, String out, String tmpPath, boolean isSelect, String s)
            throws IOException {
        BufferedReader file = new BufferedReader(new FileReader(in));
        int counter = firstPartSort(file, tmpPath, isSelect, s);
        secondPartSort(tmpPath, out, counter);
        for (int i = 0; i < counter; i++)
            Files.deleteIfExists(Paths.get(tmpPath, i + ".txt"));
    }

    @Override
    public void sort(String in, String out, String tmpPath) {
        try{
            sortHelper(in, out, tmpPath, false, "");
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    /**
     * @param s1 the first string
     * @param s2 the second string
     * @return the difference between their id's
     */
    private int compare(String s1, String s2)
    {
        return s1.split(" ")[0].compareTo(s2.split(" ")[0]);
    }

    /**
     * @param f1 the first string
     * @param f2 the second string
     * @return the combined data to write to the join
     */
    private String combineResults(String f1, String f2){
        StringBuilder result = new StringBuilder();
        String[] s1 = f1.split(" "), s2 = f2.split(" ");
        result.append(s1[0]).append(" ").append(s1[1]).append(" ").append(s1[2]).append(" ").append(s2[1])
                .append(" ").append(s2[2]);
        return result.toString();
    }

    @Override
    protected void join(String in1, String in2, String out, String tmpPath) {
        try{
            BufferedReader file1 = new BufferedReader(new FileReader(in1));
            BufferedReader file2 = new BufferedReader(new FileReader(in2));
            BufferedWriter writer = new BufferedWriter(new FileWriter(out));
            ArrayList<String> outputBlock = new ArrayList<>();
            String s1 = file1.readLine(), s2 = file2.readLine();
            while(s1 != null){
                while(s2 != null && compare(s1, s2) > 0)
                    s2 = file2.readLine();
                while(s2 != null && compare(s1, s2) == 0){
                    addToOutput(outputBlock, combineResults(s1, s2), JOINED_TUPLE_LENGTH, writer);
                    s2 = file2.readLine();
                }
                s1 = file1.readLine();
            }
            writeToFile(outputBlock, writer);
            file1.close();
            file2.close();
            writer.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    /**
     * @param currentSelected the current string
     * @param substrSelect the selection string
     * @return true if the string fits the selection, else false
     */
    private static boolean isFittingSelect(String currentSelected, String substrSelect) {
        return currentSelected.split(" ")[0].contains(substrSelect);
    }

    @Override
    protected void select(String in, String out, String substrSelect, String tmpPath) {
        try{
            BufferedReader file = new BufferedReader(new FileReader(in));
            BufferedWriter writer = new BufferedWriter(new FileWriter(out));
            ArrayList<String> outputBlock = new ArrayList<>();
            String s = file.readLine();
            while(s != null){
                if(isFittingSelect(s, substrSelect))
                    addToOutput(outputBlock, s, TUPLE_LENGTH, writer);
                s = file.readLine();
            }
            writeToFile(outputBlock, writer);
            file.close();
            writer.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }


    /**
     * @param block the block to write to memory
     * @param s the string to add to the block
     * @param tupleLength the length of each string in the block
     * @param writer the object with which to write to file
     * this function stores the string and if the block is full, saves it and clears the block
     * @throws IOException shit
     */
    private static void addToOutput(ArrayList<String> block, String s, int tupleLength, BufferedWriter writer)
            throws IOException {
        block.add(s);
        if((block.size() + 1) * tupleLength <= BLOCK_SIZE)
            return;
        writeToFile(block, writer);
        block.clear();
    }

    /**
     * @param block the block to write to file
     * @param writer the object with whom to write
     * @throws IOException shit
     * writes the block to the writer object
     */
    private static void writeToFile(ArrayList<String> block, BufferedWriter writer) throws IOException {
        if(block.size() == 0)
            return;
        for(String s : block)
            writer.write(s + "\n");
        writer.flush();
    }


    @Override
    public void joinAndSelectEfficiently(String in1, String in2, String out,
                                         String substrSelect, String tmpPath) {
        String sout1 = Paths.get(tmpPath, "tempOut1.txt").toString();
        String sout2 = Paths.get(tmpPath, "tempOut2.txt").toString();
        try{
            sortHelper(in1, sout1, tmpPath, true, substrSelect);
            sortHelper(in2, sout2, tmpPath, true, substrSelect);
            join(sout1, sout2, out, tmpPath);
            Files.deleteIfExists(Paths.get(sout1));
            Files.deleteIfExists(Paths.get(sout2));
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}