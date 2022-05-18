package Order;

import java.io.File;
import java.util.function.BiFunction;

public class SizeOrder extends Order {
    /* the commands of the size ordering */
    private static final String SIZE = "size";

    /* the size sorting function */
    private static BiFunction<File, File, Integer> sizeFunction =
            (File f1, File f2) -> (f1.length() - f2.length() != 0 ?
                    (int)Math.signum(f1.length() - f2.length()) :
                    AbsOrder.absFunction.apply(f1, f2));

    /**
     * @param orderLine the line of the order input
     * @param files the files array to filter
     * @return the files array filtered by the command with the inputs firstValue, secondValue
     */
    public File[] order(String orderLine, File[] files){
        return OrderManager.sort(files, sizeFunction);
    }


    /**
     * @param orderLine the line of the order input
     * @return whether the command is of this order or not
     */
    public boolean isThisOrderCommand(String orderLine){
        return getCommand(orderLine).equals(SIZE);
    }
}
