package filesprocessing;

import ErrorTypes.TypeTwoError;
import Filter.FilterManager;
import Order.OrderManager;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Parser {

    /* this constant holds the amount of lines per section */
    private static final int NUMBER_LINES_PER_SECTION = 4;
    /* this constant holds the name of the filter sub-section */
    private static final String FILTER = "FILTER";
    /* this constant holds the name of the order sub-section */
    private static final String ORDER = "ORDER";
    /* this variable holds all the sections */
    private ArrayList<Section> sections;
    /* this variable hold all the files in the directory */
    private File[] filesDirectory;

    /**
     * this function initializes the sections array list
     */
    public Parser() {
        sections = new ArrayList<>();
    }

    /**
     * this function initializes the sections if everything is alright else throws an error
     * @param commandFile gets the command file
     * @throws TypeTwoError handle all errors that might occur if the command file has type 2 errors
     */
    public void initializeData(File commandFile) throws TypeTwoError {
        Scanner reader;
        try {
            reader = new Scanner(commandFile);
        }catch (FileNotFoundException error){
            throw new TypeTwoError("ERROR: the command file doesn't exists \n");
        }
        readData(reader);
    }

    /**
     * this function initializes the sections if everything is alright else throws an error
     * @param reader gets the command file as a scanner to read the data with
     * @throws TypeTwoError handle all errors that might occur if the command file has type 2 and the file
     * exists
     */
    private void readData(Scanner reader) throws TypeTwoError {
        ArrayList<String> data = new ArrayList<>();
        while(reader.hasNextLine())
            data.add(reader.nextLine());
        int lineNumber = 0;
        while(lineNumber < data.size()){
            int newLineNumber = readSection(data, lineNumber);
            lineNumber += newLineNumber;
        }
        if(sections.size() != 0 && sections.get(sections.size() - 1).getOrderCommand().equals(""))
            // the last line is empty
            sections.get(sections.size() - 1).setOrderCommand(OrderManager.getDefaultOrder());
    }

    /**
     * this function reads a single section and adds it to the sections array list
     * @param data the data of the file
     * @param lineNumber the current line number before entering there section
     * @throws TypeTwoError handle all errors that might occur if the command file has type 2 error
     * @return the number of lines in this section
     */
    private int readSection(ArrayList<String> data, int lineNumber) throws TypeTwoError {
        int filterNumber = lineNumber + 1 + 1;
        int orderNumber = lineNumber + 3 + 1;
        Section section = new Section(filterNumber, orderNumber);
        int counter;
        for(counter = 0; counter < NUMBER_LINES_PER_SECTION && counter + lineNumber < data.size(); counter++)
            handleCommand(section, data.get(counter + lineNumber), counter);
        if(counter - 1 < NUMBER_LINES_PER_SECTION / 2) // no order sub section at all
            throw new TypeTwoError("ERROR: ORDER sub-section missing \n");
        if(section.getOrderCommand().equals(FILTER)){ //the last line is not part of this section
            counter--;
            section.setOrderCommand(OrderManager.getDefaultOrder());
        }
        this.sections.add(section);
        return counter;
    }

    /**
     * this function updates the command of the section if the index is correct and checks whether the
     * other are correct
     * @param section section to check and update
     * @param line the current command line
     * @param i the index in the section itself
     * @throws TypeTwoError handle all errors that might occur if the command file has type 2 error
     */
    private void handleCommand(Section section, String line, int i) throws TypeTwoError {
        if(i == 0)
            if(!line.equals(FILTER))
                throw new TypeTwoError("ERROR: FILTER sub-section missing \n");
        if(i == 1)
            section.setFilterCommand(line);
        if(i == 2)
            if(!line.equals(ORDER))
                throw new TypeTwoError("ERROR: ORDER sub-section missing \n");
        if(i == 3)
            section.setOrderCommand(line);
    }


    /**
     * this function does all the requests from the sections in order after the sections were filled
     */
    public void compileSections(File directory){
        filesDirectory = directory.listFiles();
        //make sure the files exists
        if(filesDirectory == null)
            filesDirectory = new File[0];
        //make sure all the files are files and not directories
        filesDirectory = HelperFunctions.filterArrayByFunction(filesDirectory,
                (File f) -> (f.isFile()));
        for (Section section : sections)
            compileSection(section);
    }

    /**
     * this function does all the requests from a single section
     */
    private void compileSection(Section section){
        File[] filteredFiles = FilterManager.filter(section, filesDirectory);
        File[] orderedFiles = OrderManager.order(section, filteredFiles);
        for(File file: orderedFiles)
            System.out.println(file.getName());
    }

}
