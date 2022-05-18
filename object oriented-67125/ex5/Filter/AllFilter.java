package Filter;

import ErrorTypes.TypeOneError;

import java.io.File;

public class AllFilter extends Filter {
    /* the commands of the all filtering */
    private static final String ALL = "all";


    /**
     * @param filterLine the filterLine command in the file
     * @param files the files array to filter
     * @return the files array filtered by the command with the inputs firstValue, secondValue
     */
    public File[] filter(String filterLine, File[] files) throws TypeOneError {
        return files;
    }

    /**
     * @param filterLine the line of the filter input
     * @return whether the command is of this filter or not
     */
    public boolean isThisFilterCommand(String filterLine) {
        return getCommand(filterLine).equals(ALL);
    }
}
