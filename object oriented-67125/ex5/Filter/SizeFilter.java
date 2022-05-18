package Filter;

import ErrorTypes.TypeOneError;

import java.io.File;
public class SizeFilter extends Filter{
    /* the commands of the size filtering */
    private static final String GREATER_COMMAND = "greater_than";
    private static final String LESSER_COMMAND = "smaller_than";
    private static final String BETWEEN_COMMAND = "between";
    /* the ration between bytes and k bytes */
    private static final int convertToBytes = 1024;

    /**
     * @param filterLine the line of the filter input
     * @return whether the command is of this filter or not
     */
    public boolean isThisFilterCommand(String filterLine){
        String command = getCommand(filterLine);
        return command.equals(GREATER_COMMAND) || command.equals(LESSER_COMMAND)
                || command.equals(BETWEEN_COMMAND);
    }

    /**
     * @param filterLine the filterLine command in the file
     * @param files the files array to filter
     * @return the files array filtered by the command with the inputs firstValue, secondValue
     */
    public File[] filter(String filterLine, File[] files) throws TypeOneError {
        return filter(files, getCommand(filterLine), getFirstValue(filterLine), getSecondValue(filterLine));
    }

    /**
     * @param files the files array to filter
     * @param command the command of the filter
     * @param firstValue the first value of the filter
     * @param secondValue the second value of the filter
     * @return a filtered file array from files with the command
     * @throws TypeOneError if the size has errors
     */
    private File[] filter(File[] files, String command, String firstValue, String secondValue) throws
            TypeOneError {
        double firstNumber = convertToDouble(firstValue) * convertToBytes;
        if(command.equals(GREATER_COMMAND)) {
            invalidInput(secondValue);
            return filterArrayByFunction(files,
                    (File file) -> (file.length() > firstNumber));
        }
        if(command.equals(LESSER_COMMAND)) {
            invalidInput(secondValue);
            return filterArrayByFunction(files,
                    (File file) -> (file.length() < firstNumber));
        }
        if(command.equals(BETWEEN_COMMAND)){
            double secondNumber = convertToDouble(secondValue) * convertToBytes;
            if(firstNumber > secondNumber)
                throw new TypeOneError("the second number is less than the first one");
            return filterArrayByFunction(files,
                    (File file) -> (firstNumber <= file.length() && file.length() <= secondNumber));
        }
        return files;
    }

    /**
     * @param value the sting to convert into a double
     * @return the string as a double
     * @throws TypeOneError if the number is negative or couldn't convert the number
     */
    private static double convertToDouble(String value) throws TypeOneError {
        try{
            double number = Double.parseDouble(value);
            if(number < 0)
                throw new TypeOneError("the number you entered is negative");
            return number;
        }catch(NumberFormatException error){
            throw new TypeOneError("the number you entered is illegal");
        }
    }

    /**
     * @param value the value to check
     * throws an error if the input is invalid (not NOT command or empty string
     */
    private static void invalidInput(String value) throws TypeOneError {
        if(value.equals(""))
            return;
        if(value.equals(NotFilter.NOT))
            return;
        throw new TypeOneError("invalid subsection input");
    }
}
