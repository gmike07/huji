package Filter;

import ErrorTypes.TypeOneError;

import java.io.File;

public class NameFilter extends Filter{
    /* the commands of the name filtering */
    private static final String FILE_COMMAND = "file";
    private static final String CONTAINS_COMMAND = "contains";
    private static final String PREFIX_COMMAND = "prefix";
    private static final String SUFFIX_COMMAND = "suffix";



    /**
     * @param filterLine the filterLine command in the file
     * @param files the files array to filter
     * @return the files array filtered by the command with the inputs firstValue, secondValue
     */
    public File[] filter(String filterLine, File[] files) throws TypeOneError {
        return filter(files, getCommand(filterLine), getFirstValue(filterLine));
    }

    /**
     * @param files the files array to filter
     * @param command the command of the filter
     * @param value the first value of the filter
     * @return a filtered file array from files with the command
     * @throws TypeOneError if the size has errors
     */
    private File[] filter(File[] files, String command, String value) throws TypeOneError {
        if(command.equals(PREFIX_COMMAND))
            return filterArrayByFunction(files,
                    (File file) -> (file.getName().startsWith(value)));
        if(command.equals(SUFFIX_COMMAND))
            return filterArrayByFunction(files,
                    (File file) -> (file.getName().endsWith(value)));
        if(command.equals(CONTAINS_COMMAND))
            return filterArrayByFunction(files,
                    (File file) -> (file.getName().contains(value)));
        if(command.equals(FILE_COMMAND))
            return filterArrayByFunction(files,
                    (File file) -> (file.getName().equals(value)));
        return files;
    }


    /**
     * @param filterLine the line of the filter input
     * @return whether the command is of this filter or not
     */
    public boolean isThisFilterCommand(String filterLine){
        String command = getCommand(filterLine);
        return command.equals(FILE_COMMAND) || command.equals(CONTAINS_COMMAND)
                || command.equals(PREFIX_COMMAND) || command.equals(SUFFIX_COMMAND);
    }
}


