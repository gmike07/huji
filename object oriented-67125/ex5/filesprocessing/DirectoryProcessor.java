package filesprocessing;

import ErrorTypes.TypeTwoError;

import java.io.File;

public class DirectoryProcessor {
    /* this variable hold the input directory */
    private static File directory;
    /* this variable hold the input command file */
    private static File commandFile;
    public static void main(String[] args){
        Parser interpreter = new Parser();
        try { //try to load the data without errors
            checkValidityInputs(args);
            interpreter.initializeData(commandFile);
            interpreter.compileSections(directory);
        }catch (TypeTwoError error) {
            System.err.println(error.getMessage());
        }
    }

    /**
     * @param args the parameters of the user
     * @throws TypeTwoError if the args length is not correct and if the directory is not a directory
     * this function checks the input of the function without the command file
     */
    private static void checkValidityInputs(String[] args) throws TypeTwoError {
        if(args.length != 2)
            throw new TypeTwoError("Error: wrong number of parameters to main function \n");
        directory = new File(args[0]);
        commandFile = new File(args[1]);
        if(!directory.isDirectory())
            throw new TypeTwoError("Error: the first input is not a directory \n");
    }
}
