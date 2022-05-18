import static org.junit.Assert.*;
import org.junit.*;

import java.util.HashMap;
import oop.ex3.spaceship.*;

/**
 * this class test the LongTermStorage class
 */
public class LongTermTest {

    private static Item[] items;
    private static LongTermStorage storage;

    private static final String WRONG_UPDATE_ADD = "you didn't update correctly after adding";
    private static final String WRONG_MAX_CAPACITY = "wrong max storage capacity";
    private static final String WRONG_RESET_UPDATE = "wrong current storage input after resetting inventory";
    private static final String ADD_NEGATIVE = "added to storage a negative amount of item";
    private static final String ERROR_ADDING = "added to storage when the storage didn't have the place for" +
            " it";
    private static final int ZERO_APPEARANCE = 0;
    private static final int MAX_CAPACITY = 1000;
    private static final int BASEBALL = 0;
    private static final int MAX_BASKETBALL = 500;
    private static final int FAIL = -1;
    private static final int SUCCESS = 0;
    private static final int TIMES_ADD_ITEM = 1;
    private static final int NUMBER_OF_CHECKS = 10;

    /**
     * this function resets the storage before every test
     */
    @Before
    public void resetStorage(){
        storage.resetInventory();
    }

    /**
     * this function resets the the items
     */
    @BeforeClass
    public static void resetItems(){
        items = ItemFactory.createAllLegalItems();
        storage = new LongTermStorage();
    }

    /**
     * this function checks the getCapacity function
     */
    @Test
    public void TestMaxCapacity(){
        assertEquals(WRONG_MAX_CAPACITY, MAX_CAPACITY, storage.getCapacity());
    }

    /**
     * this function checks the resetInventory function
     */
    @Test
    public void TestResetInventory(){
        storage.resetInventory();
        assertEquals(WRONG_RESET_UPDATE, MAX_CAPACITY, storage.getAvailableCapacity());
        assertTrue(WRONG_RESET_UPDATE, storage.getInventory().isEmpty());
    }

    /**
     * this function checks correctness for adding items
     */
    @Test
    public void TestAddItem(){
        Item item = items[BASEBALL];

        //check negative inputs
        for(int i = -NUMBER_OF_CHECKS; i < 0; i++) {
            assertEquals(ADD_NEGATIVE, FAIL, storage.addItem(item, i));
        }

        //check simple adding above the thresh hold
        for(int i = MAX_BASKETBALL + NUMBER_OF_CHECKS; i > MAX_BASKETBALL; i--) {
            assertEquals(ERROR_ADDING, FAIL, storage.addItem(item, i));
        }

        //check simple adding to storage
        for(Item item1 : items) {
            assertEquals(WRONG_UPDATE_ADD, 0, storage.addItem(item1, TIMES_ADD_ITEM));
        }

        //check that storage doesn't overflow
        storage.resetInventory();
        assertEquals(WRONG_UPDATE_ADD, SUCCESS, storage.addItem(item, MAX_BASKETBALL));
        assertEquals(WRONG_UPDATE_ADD, FAIL, storage.addItem(item, TIMES_ADD_ITEM));

    }

    /**
     * this function checks correctness for saving the correct getAvailableCapacity
     */
    @Test
    public void TestGetAvailableCapacity(){
        Item item = items[BASEBALL];

        //check negative inputs
        for(int i = -NUMBER_OF_CHECKS; i < 0; i++) {
            storage.addItem(item, i);
            assertEquals(ADD_NEGATIVE, MAX_CAPACITY, storage.getAvailableCapacity());
        }

        //check simple adding above the thresh hold
        for(int i = MAX_BASKETBALL + NUMBER_OF_CHECKS; i > MAX_BASKETBALL; i--) {
            storage.addItem(item, i);
            assertEquals(ERROR_ADDING, MAX_CAPACITY, storage.getAvailableCapacity());
        }

        //check simple adding to storage
        int capacity = 0;
        for(Item item1 : items) {
            storage.addItem(item1, TIMES_ADD_ITEM);
            capacity += item1.getVolume();
            assertEquals(WRONG_UPDATE_ADD, MAX_CAPACITY-capacity,
                    storage.getAvailableCapacity());
        }

        //check that storage doesn't overflow
        storage.resetInventory();
        assertEquals(WRONG_RESET_UPDATE, MAX_CAPACITY, storage.getAvailableCapacity());
        storage.addItem(item, MAX_BASKETBALL);
        assertEquals(WRONG_UPDATE_ADD, SUCCESS, storage.getAvailableCapacity());
        storage.addItem(item, TIMES_ADD_ITEM);
        assertEquals(WRONG_UPDATE_ADD, SUCCESS, storage.getAvailableCapacity());

    }

    /**
     * this function checks correctness for saving the correct getItemCount
     */
    @Test
    public void TestGetItemCount(){
        Item item = items[BASEBALL];
        //check negative inputs
        for(int i = -NUMBER_OF_CHECKS; i < 0; i++) {
            storage.addItem(item, i);
            assertEquals(ADD_NEGATIVE, ZERO_APPEARANCE, storage.getItemCount(item.getType()));
        }
        //check simple adding above the thresh hold
        for(int i = MAX_BASKETBALL + NUMBER_OF_CHECKS; i > MAX_BASKETBALL; i--) {
            storage.addItem(item, i);
            assertEquals(ERROR_ADDING, ZERO_APPEARANCE,storage.getItemCount(item.getType()));
        }
        //check simple adding to storage
        for(Item item1 : items) {
            storage.addItem(item1, TIMES_ADD_ITEM);
            assertEquals(WRONG_UPDATE_ADD, TIMES_ADD_ITEM, storage.getItemCount(item.getType()));
        }
        //check that storage doesn't overflow
        storage.resetInventory();
        assertEquals(WRONG_RESET_UPDATE, SUCCESS, storage.getItemCount(item.getType()));
        storage.addItem(item, MAX_BASKETBALL);
        assertEquals(WRONG_UPDATE_ADD, MAX_BASKETBALL, storage.getItemCount(item.getType()));
        storage.addItem(item, TIMES_ADD_ITEM);
        assertEquals(WRONG_UPDATE_ADD, MAX_BASKETBALL, storage.getItemCount(item.getType()));
    }

    /**
     * this function checks correctness for saving the correct getInventory
     */
    @Test
    public void TestGetInventory(){
        Item item = items[BASEBALL];
        HashMap<String, Integer> testMap = new HashMap<>();
        //check negative inputs
        for(int i = -NUMBER_OF_CHECKS; i < 0; i++) {
            storage.addItem(item, i);
            assertEquals(ADD_NEGATIVE, testMap,storage.getInventory());
        }
        //check simple adding above the thresh hold
        for(int i = MAX_BASKETBALL + NUMBER_OF_CHECKS; i > MAX_BASKETBALL; i--) {
            storage.addItem(item, i);
            assertEquals(ERROR_ADDING, testMap, storage.getInventory());
        }
        //check simple adding to storage
        for(Item item1 : items) {
            storage.addItem(item1, TIMES_ADD_ITEM);
            testMap.put(item1.getType(), TIMES_ADD_ITEM);
            assertEquals(WRONG_UPDATE_ADD, testMap, storage.getInventory());
        }
        //check that storage doesn't overflow
        storage.resetInventory();
        testMap = new HashMap<>();
        assertEquals(WRONG_RESET_UPDATE, testMap, storage.getInventory());
        testMap.put(item.getType(), MAX_BASKETBALL);
        storage.addItem(item, MAX_BASKETBALL);
        assertEquals(WRONG_UPDATE_ADD, testMap, storage.getInventory());
        storage.addItem(item, TIMES_ADD_ITEM);
        assertEquals(WRONG_UPDATE_ADD, testMap, storage.getInventory());
    }

}
