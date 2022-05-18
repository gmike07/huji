import java.util.HashMap;
import java.util.Map;
import oop.ex3.spaceship.*;

public class Locker {

    /* this constants hold the message to print when the user tries to add baseball and football */
    private static final String FOOTBALL_ERROR_1 = "Error: Your request cannot be completed at this time. " +
            "Problem: the locker cannot contain items of type ";
    private static final String FOOTBALL_ERROR_2 = ", as it contains a contradicting item";

    /* this constant holds the message to print when the items were added to the storage */
    private static final String ADDED_TO_STORAGE = "Warning: Action successful, but has caused items to be " +
            "moved to storage";

    /* this constants hold the message to print when the user tries to add items and there is not enough
    place */
    private static final String PLACE_ERROR_1 = "Error: Your request cannot be completed at this time. " +
            "Problem: no room for ";
    private static final String PLACE_ERROR_2 = " Items of type ";

    /* this constant holds the message to print when the user tries to remove a negative number */
    private static final String REMOVE_NEGATIVE_ERRROR = "Error: Your request cannot be completed at this " +
            "time. Problem: cannot remove a negative number of items of type ";

    /* this constants hold the message to print when the user tries to remove too many. */
    private static final String REMOVE_MANY_ERROR_1 = "Error: Your request cannot be completed at " +
            "this time. Problem: the locker does not contain ";
    private static final String REMOVE_MANY_ERROR_2 = " items of type ";

    /* this constant holds the default string error */
    private static final String DEFAULT_ERROR = "Error: Your request cannot be completed at this time.";

    /* this constant holds the football type */
    private static final String FOOTBALL = "football";

    /* this constant holds the baseball bat type */
    private static final String BASEBALL = "baseball bat";

    /* this constant holds the max capacity of the locker */
    private final int maxCapacity;

    /* this variable holds the current capacity of the locker */
    private int capacity;

    /* this variable holds the inventory */
    private HashMap<String, Integer> inventory;

    /* this variable holds the storage */
    private static final LongTermStorage storage = new LongTermStorage();

    /* this constant holds the factor of things that stay in the locker if part of them go the storage */
    private static final double FACTOR_LOCKER = 0.2;
    /**
     * This constructor initializes a Locker object with the given capacity
     * @param capacity gets the maximum amount of storage for this locker
     */
    public Locker(int capacity){
        maxCapacity = capacity;
        this.capacity = 0;
        inventory = new HashMap<>();

    }

    /**
     * this function tries to add item to the locker
     * @param item the item to add to the locker
     * @param n the amount of item to add
     * @return -1 if couldn't add to storage, else 0 and adds items to locker, 1 if part of the added items
     * moved to the storage
     */
    public int addItem(Item item, int n){
        if(item.getType().equals(FOOTBALL) || item.getType().equals(BASEBALL)) {
            if ((inventory.containsKey(FOOTBALL) || inventory.containsKey(BASEBALL)) &&
                    !inventory.containsKey(item.getType())){ //contains the other type
                System.out.println(FOOTBALL_ERROR_1 + item.getType() + FOOTBALL_ERROR_2);
                return -2;
            }
        }
        if(n < 0){
            System.out.println(DEFAULT_ERROR);
            return -1;
        }
        int addedCapacity = capacity + capacityNItems(item, n);
        if(addedCapacity > maxCapacity){
            System.out.println(PLACE_ERROR_1 + n + PLACE_ERROR_2 + item.getType());
            return -1;
        }
        addItemsToLocker(item, n);
        if(capacityNItems(item, getItemCount(item.getType())) <= maxCapacity / 2) { // not more than 50%
            return 0;
        }
        int returnValue = handleAllocationStorage(item, n);
        //delete item if it is 0 times in locker
        if(getItemCount(item.getType()) == 0)
            inventory.remove(item.getType());
        return returnValue;
    }

    /**
     * this function assumes that n items alreasy were added to the locker and should be removed somehow
     * @param item the item to add to the locker
     * @param n the amount of item to add
     * @return -1 if couldn't add to storage (removing n items from locker), else 1 if successed and leaves
     * 20% in the locker (removing everything but 20%)
     */
    private int handleAllocationStorage(Item item, int n) {
        int maxCountItemLocker = (int) (FACTOR_LOCKER * maxCapacity / item.getVolume());
        int amountToMoveToStorage = getItemCount(item.getType()) - maxCountItemLocker;
        if(capacityNItems(item, amountToMoveToStorage) > storage.getAvailableCapacity()) {
            removeItemsFromLocker(item, n);
            System.out.println(PLACE_ERROR_1 + amountToMoveToStorage + PLACE_ERROR_2 + item.getType());
            return -1;
        }
        //can add to storage
        storage.addItem(item, amountToMoveToStorage);
        System.out.println(ADDED_TO_STORAGE);
        removeItemsFromLocker(item, amountToMoveToStorage);
        return 1;
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
     * adds the items to the locker and updates the capacity
     */
    private void addItemsToLocker(Item item, int n){
        capacity += capacityNItems(item, n);
        String type = item.getType();
        inventory.put(type, n + getItemCount(type));
    }

    /**
     * @param item the item to remove from the locker
     * @param n the amount of item to remove
     * @return -1 if couldn't remove from locker else 0
     */
    public int removeItem(Item item, int n){
        if(n < 0){
            System.out.println(REMOVE_NEGATIVE_ERRROR + item.getType());
            return -1;
        }
        if(getItemCount(item.getType()) < n){
            System.out.println(REMOVE_MANY_ERROR_1 + n + REMOVE_MANY_ERROR_2 + item.getType());
            return -1;
        }
        removeItemsFromLocker(item, n);
        return 0;
    }

    /**
     * @param item the item to remove from the locker
     * @param n the amount of item to remove
     * removes the items from the locker and updates the capacity
     */
    private void removeItemsFromLocker(Item item, int n){
        capacity -= capacityNItems(item, n);
        String type = item.getType();
        inventory.put(type, getItemCount(type) - n);
        if(inventory.get(type) == 0)
            inventory.remove(type);
    }

    /**
     * @param type gets a type of item
     * @return the number of Items of type type the locker contains.
     */
    public int getItemCount(String type){
        return inventory.getOrDefault(type, 0);
    }

    /**
     * This method returns a map of all the item types contained in the locker, and their respective
     * quantities.
     */
    public Map<String, Integer> getInventory(){
        return inventory;
    }

    /**
     * @return the locker’s total capacity
     */
    public int getCapacity(){
        return maxCapacity;
    }

    /**
     * @return the locker’s available capacity, i.e.how many storage units are unoccupied by Items
     */
    public int getAvailableCapacity(){
        return maxCapacity - capacity;
    }

    /**
     * @return the storage of the lockers
     */
    protected LongTermStorage getStorage(){
        return storage;
    }
}
