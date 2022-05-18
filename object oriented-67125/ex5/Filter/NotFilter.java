package Filter;

import ErrorTypes.TypeOneError;

import java.io.File;
import java.util.ArrayList;

public class NotFilter extends Filter {

    /* the filter object to apply not to */
    private Filter filter;
    /* the string value to check if to swap the filter or not */
    protected static final String NOT = "NOT";

    /**
     * @param filter a filter to apply not to
     */
    public NotFilter(Filter filter){
        this.filter = filter;
    }


    /**
     * @param filterLine the filterLine command in the file
     * @param files the files array to filter
     * @return the files array filtered by the filterLine with the not command if needed
     */
    public File[] filter(String filterLine, File[] files) throws TypeOneError {
        File[] filtered = this.filter.filter(filterLine, files);
        if(!shouldNot(filterLine))
            return filtered;
        return ApplyNot(files, filtered);
    }

    /**
     * @param files the files array
     * @param filtered the files array filtered
     * @return all the files in files that are not in filtered
     */
    private static File[] ApplyNot(File[] files, File[] filtered){
        ArrayList<File> newFiles = new ArrayList<>();
        for(File file : files){
            if(!Contains(filtered, file))
                newFiles.add(file);
        }
        return convertToArray(newFiles);
    }

    /**
     * @param files the files array to check
     * @param f the file to check
     * @return whether f is in the array files
     */
    private static boolean Contains(File[] files, File f){
        for(File file: files) {
            if (file == f)
                return true;
        }
        return false;
    }

    /**
     * @param filterLine the line of the filter input
     * @return whether the command is of this filter or not
     */
    public boolean isThisFilterCommand(String filterLine){
        return filter.isThisFilterCommand(filterLine);
    }

    /**
     * @param s gets a string
     * @return should not the string
     */
    private boolean shouldNot(String s){
        String[] spillted = s.split("#");
        if(spillted.length == 0)
            return false;
        return spillted[spillted.length - 1].equals(NOT);
    }
}
