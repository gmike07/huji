import java.util.HashMap;
import java.util.Map;
import oop.ex3.spaceship.*;
/* this class is a long term storage, everything is static because only one of this can exists */
public class LongTermStorage {

    /* this constant holds the default string error */
    private final String DEFAULT_ERROR = "Error: Your request cannot be completed at this time.";

    /* this constants hold the message to print when the user tries to add items and there is not enough
   place */
    private static final String PLACE_ERROR_1 = "Error: Your request cannot be completed at this time. " +
            "Problem: no room for ";
    private static final String PLACE_ERROR_2 = " Items of type ";


    /* this constant holds the max capacity of the storage */
    private final int STORAGE_MAX_CAPACITY = 1000;

    /* this variable holds the current capacity of the storage */
    private int capacity;

    /* this variable holds the inventory */
    private HashMap<String, Integer> inventory;

    /**
     * This constructor initializes a Long-Term Storage object.
     */
    public LongTermStorage(){
        resetInventory();
    }

    /**
     * this function tries to add item to the storage
     * @param item the item to add to the storage
     * @param n the amount of item to add
     * @return -1 if couldn't add to storage, else 0 and adds items to storage
     */
    public int addItem(Item item, int n){
        if(n < 0){
            System.out.println(DEFAULT_ERROR);
            return -1;
        }
        int addedCapacity = capacity + capacityNItems(item, n);
        if(addedCapacity > STORAGE_MAX_CAPACITY){
            System.out.println(PLACE_ERROR_1 + n + PLACE_ERROR_2 + item.getType());
            return -1;
        }
        addItemsToStorage(item, n);
        return 0;
    }

    /**
     * @param item the item to add to the storage
     * @param n the amount of item to add
     * @return the amount of space the the n items require
     */
    private int capacityNItems(Item item, int n){
        return item.getVolume() * n;
    }

    /**
     * @param item the item to add to the storage
     * @param n the amount of item to add
     * adds the items to the storage and updates the capacity
     */
    private void addItemsToStorage(Item item, int n){
        capacity += capacityNItems(item, n);
        String type = item.getType();
        inventory.put(type, n + getItemCount(type));
    }


    /**
     * This method resets the long-term storage’s inventory (i.e. after
     * it is invoked the inventory does not contain any Item).
     */
    public void resetInventory(){
        capacity = 0;
        inventory = new HashMap<>();
    }

    /**
     * @param type gets a type of item
     * @return the number of Items of type type
     * the long-term storage contains.
     */
    public int getItemCount(String type){
        return inventory.getOrDefault(type, 0);
    }

    /**
     * This method returns a map of all the Items contained in the long-term storage unit, and their
     * respective quantities.
     */
    public Map<String, Integer> getInventory(){
        return inventory;
    }

    /**
     * @return the long-term storage’s total capacity
     */
    public int getCapacity(){
        return STORAGE_MAX_CAPACITY;
    }

    /**
     * @return the long-term storage’s available capacity, i.e. how many storage units are unoccupied by
     * Items.
     */
    public int getAvailableCapacity(){
        return STORAGE_MAX_CAPACITY - capacity;
    }
}
