package Order;
import java.io.File;
import java.util.function.BiFunction;

public class TypeOrder extends Order {

    /* the commands of the type ordering */
    private static final String TYPE = "type";

    /* a dot */
    private static final String DOT = ".";

    /* the type sorting function */
    private static BiFunction<File, File, Integer> typeFunction =
            (File f1, File f2) -> (compareExtensions(f1, f2) != 0 ?
                    compareExtensions(f1, f2): AbsOrder.absFunction.apply(f1, f2));

    /**
     * @param orderLine the line of the order input
     * @param files the files array to filter
     * @return the files array filtered by the command with the inputs firstValue, secondValue
     */
    public File[] order(String orderLine, File[] files) {
        return OrderManager.sort(files, typeFunction);
    }

    /**
     * @param orderLine the line of the order input
     * @return whether the command is of this order or not
     */
    public boolean isThisOrderCommand(String orderLine){
        return getCommand(orderLine).equals(TYPE);
    }

    /**
     * @param s get a file name with an extension
     * @return return everything from the extension
     */
    private static String getExtension(String s){
        int lastIndexOfDot = s.lastIndexOf(DOT);
        if(lastIndexOfDot == 0 || lastIndexOfDot == -1)
            return "";
        return s.substring(lastIndexOfDot + 1);
    }

    /**
     * @param f1 gets first file
     * @param f2 gets second file
     * @return an int comparing their extensions
     */
    private static int compareExtensions(File f1, File f2){
        return getExtension(f1.getName()).compareTo(getExtension(f2.getName()));
    }
}
