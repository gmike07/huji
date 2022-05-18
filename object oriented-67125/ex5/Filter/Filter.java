package Filter;

import ErrorTypes.TypeOneError;
import filesprocessing.HelperFunctions;

import java.io.File;
import java.util.ArrayList;
import java.util.function.Function;

public abstract class Filter {
    /**
     * @param filterLine the filterLine command in the file
     * @param files the files array to filter
     * @return the files array filtered by the command with the inputs firstValue, secondValue
     */
    public abstract File[] filter(String filterLine, File[] files) throws TypeOneError;


    /**
     * @param files the files array to filter
     * @param func the function to filter by
     * @return the files array filtered as an array list
     */
    protected static File[] filterArrayByFunction(File[] files,
                                                  Function<File, Boolean> func){
        return HelperFunctions.filterArrayByFunction(files, func);
    }


    /**
     * @param files the files as array list
     * @return the files converted into an array of files
     */
    protected static File[] convertToArray(ArrayList<File> files){
        return HelperFunctions.convertToArray(files);
    }


    /**
     * @param filterLine the filterLine command in the file
     * @return the command part of the line
     */
    protected static String getCommand(String filterLine){
        return HelperFunctions.getCommand(filterLine);
    }

    /**
     * @param filterLine the filterLine command in the file
     * @return the first value part of the line
     */
    protected static String getFirstValue(String filterLine){
        return HelperFunctions.getFirstValue(filterLine);
    }

    /**
     * @param filterLine the filterLine command in the file
     * @return the second value part of the line
     */
    protected static String getSecondValue(String filterLine){
        return HelperFunctions.getSecondValue(filterLine);
    }

    /**
     * @param filterLine the line of the filter input
     * @return whether the command is of this filter or not
     */
    public abstract boolean isThisFilterCommand(String filterLine);

}
