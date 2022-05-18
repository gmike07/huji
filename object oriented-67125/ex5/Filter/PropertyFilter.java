package Filter;

import ErrorTypes.TypeOneError;

import java.io.File;
public class PropertyFilter extends Filter{
    /* the commands of the property filtering */
    private static final String WRITABLE_COMMAND = "writable";
    private static final String EXECUTABLE_COMMAND = "executable";
    private static final String HIDDEN_COMMAND = "hidden";

    /* the options on the value of the property */
    private static final String YES = "YES";
    private static final String NO = "NO";


    /**
     * @param filterLine the line of the filter input
     * @return whether the command is of this filter or not
     */
    public boolean isThisFilterCommand(String filterLine){
        String command = getCommand(filterLine);
        return command.equals(WRITABLE_COMMAND) || command.equals(EXECUTABLE_COMMAND)
                || command.equals(HIDDEN_COMMAND);
    }

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
    private File[] filter(File[] files, String command, String value) throws
            TypeOneError {
        if(!value.equals(YES) && !value.equals(NO))
            throw new TypeOneError("the value is not yes or no");
        if (command.equals(WRITABLE_COMMAND))
            return filterArrayByFunction(files,
                    (File file) -> (file.canWrite() == value.equals(YES)));
        if (command.equals(EXECUTABLE_COMMAND))
            return filterArrayByFunction(files,
                    (File file) -> (file.canExecute() == value.equals(YES)));
        if (command.equals(HIDDEN_COMMAND))
            return filterArrayByFunction(files,
                    (File file) -> (file.isHidden() == value.equals(YES)));
        return files;
    }


}
