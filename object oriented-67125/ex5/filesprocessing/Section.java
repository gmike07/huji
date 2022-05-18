package filesprocessing;

public class Section {
    /* this variable holds the filter command */
    private String filterCommand = "";
    /* this variable holds the filter command line number */
    private int filterCommandLineNumber;
    /* this variable holds the order command */
    private String orderCommand = "";
    /* this variable holds the order command line number */
    private int orderCommandLineNumber;

    /**
     * @param filterCommandLineNumber gets the filter command line number
     * @param orderCommandLineNumber gets the order command line number
     */
    public Section(int filterCommandLineNumber, int orderCommandLineNumber){
        this.filterCommandLineNumber = filterCommandLineNumber;
        this.orderCommandLineNumber = orderCommandLineNumber;
    }

    /**
     * @return the order command line number
     */
    public int getOrderNumber(){
        return this.orderCommandLineNumber;
    }

    /**
     * @return the filter command line number
     */
    public int getFilterNumber(){
        return this.filterCommandLineNumber;
    }

    /**
     * @return the filter command
     */
    public String getFilterCommand(){
        return this.filterCommand;
    }

    /**
     * @return the order command
     */
    public String getOrderCommand(){
        return this.orderCommand;
    }

    /**
     * @param command gets a command
     * this function sets the command to the filter command
     */
    public void setFilterCommand(String command){
        this.filterCommand = command;
    }

    /**
     * @param command gets a command
     * this function sets the command to the order command
     */
    public void setOrderCommand(String command){
        this.orderCommand = command;
    }



}
