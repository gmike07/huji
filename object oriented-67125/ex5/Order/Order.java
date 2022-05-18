package Order;

import filesprocessing.HelperFunctions;

import java.io.File;

public abstract class Order {

    /**
     * @param orderLine the line of the order input
     * @param files the files array to filter
     * @return the files array filtered by the command with the inputs firstValue, secondValue
     */
    public abstract File[] order(String orderLine, File[] files);


    /**
     * @param orderLine the filterLine command in the file
     * @return the command part of the line
     */
    protected static String getCommand(String orderLine){
        return HelperFunctions.getCommand(orderLine);
    }

    /**
     * @param orderLine the line of the order input
     * @return whether the command is of this order or not
     */
    public abstract boolean isThisOrderCommand(String orderLine);
}
