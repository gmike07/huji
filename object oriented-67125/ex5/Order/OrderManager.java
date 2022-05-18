package Order;

import filesprocessing.HelperFunctions;
import filesprocessing.Section;

import java.io.File;
import java.util.function.BiFunction;

public class OrderManager {
    /* the default case if none is selected */
    private static final String DEFAULT_CASE = "abs";


    /* the abs order with reverse decorator */
    private static Order absOrder = new ReverseOrder(new AbsOrder());
    /* the size order with reverse decorator */
    private static Order sizeOrder = new ReverseOrder(new SizeOrder());
    /* the type order with reverse decorator */
    private static Order typeOrder = new ReverseOrder(new TypeOrder());

    /* all the orders in an array */
    private static Order[] orders = {absOrder, sizeOrder, typeOrder};

    /**
     * @param section the current section of this filter
     * @param files the files to order
     * @return the files sorted
     */
    public static File[] order(Section section, File[] files){
        return order(section.getOrderCommand(), section.getOrderNumber(), files);
    }

    /**
     * @param orderLine the line of the order input
     * @param lineNumber the line in which the order is happening in
     * @param files the files to order
     * @return the files sorted
     */
    public static File[] order(String orderLine, int lineNumber, File[] files){
        if(orderLine.equals(DEFAULT_CASE))
            return absOrder.order(orderLine, files);
        for(Order order : orders)
            if(order.isThisOrderCommand(orderLine))
                return order.order(orderLine, files);
        //else unknown command
        HelperFunctions.printWarning(lineNumber);
        return order(DEFAULT_CASE, lineNumber, files);
    }

    /**
     * @param files the files to sort
     * @param func the function to sort by
     * @return the files sorted
     */
    protected static File[] sort(File[] files, BiFunction<File, File, Integer> func){
        return mergeSort(files, func);
    }

    /**
     * @param array the array to sort
     * @param func the function to sort by
     * @return the array sorted by the function
     */
    private static File[] mergeSort(File[] array, BiFunction<File, File, Integer> func){
        if(array.length <= 1)
            return array;
        File[] part1 = mergeSort(newArray(0, array.length / 2, array), func);
        File[] part2 = mergeSort(newArray(array.length / 2, array.length, array), func);
        return merge(part1, part2, func);
    }

    /**
     * @param start the start of the new array
     * @param end the end of the new array
     * @param arr the array to copy from
     * @return a new array from start to end-1 (in python array[start:end])
     */
    private static File[] newArray(int start, int end, File[] arr){
        File[] newArr = new File[end - start];
        for(int i = start; i < end; i++)
            newArr[i - start] = arr[i];
        return newArr;
    }

    /**
     * @param arr1 the first sorted array
     * @param arr2 the second sorted array
     * @param func the function to sort by
     * @return the arrays merged into one
     */
    private static File[] merge(File[] arr1, File[] arr2, BiFunction<File, File, Integer> func){
        File[] newArr = new File[arr1.length + arr2.length];
        int i = 0;
        int j = 0;
        while(i < arr1.length || j < arr2.length){
            if(i == arr1.length){
                newArr[i + j] = arr2[j];
                j++;
            }else if(j == arr2.length || func.apply(arr1[i], arr2[j]) < 0){
                newArr[i + j] = arr1[i];
                i++;
            }else{
                newArr[i + j] = arr2[j];
                j++;
            }
        }
        return newArr;
    }

    /**
     * @return the default case for orders
     */
    public static String getDefaultOrder(){
        return DEFAULT_CASE;
    }
}
