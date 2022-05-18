package Order;

import java.io.File;

public class ReverseOrder extends Order {

    /* the order object to apply reverse to */
    private Order order;

    /* the reverse string to check */
    private static final String REVERSE = "REVERSE";

    /**
     * @param order the order object to apply reverse to
     */
    public ReverseOrder(Order order){
        this.order = order;
    }

    /**
     * @param orderLine the line of the order input
     * @param files the files array to filter
     * @return the files array filtered by the command with the inputs firstValue, secondValue
     */
    public File[] order(String orderLine, File[] files) {
        File[] sorted = this.order.order(orderLine, files);
        if(!shouldReverse(orderLine))
            return sorted;
        return reversedArray(sorted);
    }


    /**
     * @param orderLine the line of the order input
     * @return whether the command is of this order or not
     */
    public boolean isThisOrderCommand(String orderLine) {
        return order.isThisOrderCommand(orderLine);
    }

    /**
     * @param sorted the sorted array to reverse
     * @return the reversed array
     */
    private File[] reversedArray(File[] sorted){
        File[] reversedFile = new File[sorted.length];
        for(int i = 0; i < sorted.length; i++)
            reversedFile[sorted.length - i - 1] = sorted[i];
        return reversedFile;
    }

    /**
     * @param s gets a string
     * @return should reverse the string
     */
    private boolean shouldReverse(String s){
        String[] spillted = s.split("#");
        if(spillted.length == 0)
            return false;
        return spillted[spillted.length - 1].equals(REVERSE);
    }
}
