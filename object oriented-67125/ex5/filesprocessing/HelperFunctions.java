package filesprocessing;

import ErrorTypes.TypeOneError;
import Filter.NotFilter;

import java.io.File;
import java.util.ArrayList;
import java.util.function.Function;

public class HelperFunctions {
    /* the constants for getting the command of the filter \ command line */
    private static final String SPLIT_REGEX = "#";
    private static final int COMMAND_INDEX = 0;
    private static final int FIRST_VALUE = 1;
    private static final int SECOND_VALUE = 2;

    /**
     * @param files the files as array list
     * @return the files converted into an array of files
     */
    public static File[] convertToArray(ArrayList<File> files){
        File[] arrayFiles = new File[files.size()];
        return files.toArray(arrayFiles);
    }


    /**
     * @param line the filterLine \ OrderLine command in the file
     * @return the command part of the line
     */
    public static String getCommand(String line){
        return getPart(line, COMMAND_INDEX);
    }

    /**
     * @param line the filterLine \ OrderLine command in the file
     * @return the first value part of the line
     */
    public static String getFirstValue(String line){
        return getPart(line, FIRST_VALUE);
    }

    /**
     * @param line the filterLine \ OrderLine command in the file
     * @return the second value part of the line
     */
    public static String getSecondValue(String line){
        return getPart(line, SECOND_VALUE);
    }


    /**
     * @param line the filterLine \ OrderLine command in the file
     * @param index the index to know which part to return
     * @return the index part of the line
     */
    private static String getPart(String line, int index) {
        String[] splitted = line.split(SPLIT_REGEX);
        return splitted.length > index ? splitted[index] : "";
    }

    /**
     * @param lineNumber the line in which there is a warning
     *  this function prints warning in the needed line
     */
    public static void printWarning(int lineNumber){
        System.err.println("Warning in line " + lineNumber);
    }

    /**
     * @param files the files array to filter
     * @param func the function to filter by
     * @return the files array filtered as an array list
     */
    public static File[] filterArrayByFunction(File[] files,
                                                  Function<File, Boolean> func){
        ArrayList<File> listFiles = new ArrayList<>();
        for(File file: files) {
            if (func.apply(file))
                listFiles.add(file);
        }
        return convertToArray(listFiles);
    }

}
