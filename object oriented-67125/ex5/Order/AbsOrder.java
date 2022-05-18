package Order;

import java.io.File;
import java.util.function.BiFunction;

public class AbsOrder extends Order {

    /* the commands of the abs ordering */
    private static final String ABS = "abs";

    /* the abs sorting function */
    protected static BiFunction<File, File, Integer> absFunction =
            (File f1, File f2) -> (f1.getAbsolutePath().compareTo(f2.getAbsolutePath()));

    /**
     * @param orderLine the line of the order input
     * @param files the files array to filter
     * @return the files array filtered by the command with the inputs firstValue, secondValue
     */
    public File[] order(String orderLine, File[] files){
        return OrderManager.sort(files, absFunction);
    }


    /**
     * @param orderLine the line of the order input
     * @return whether the command is of this order or not
     */
    public boolean isThisOrderCommand(String orderLine){
        return getCommand(orderLine).equals(ABS);
    }
}
