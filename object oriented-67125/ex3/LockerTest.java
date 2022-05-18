import static org.junit.Assert.*;
import org.junit.*;

import java.util.HashMap;
import oop.ex3.spaceship.*;
public class LockerTest {
    private static Item[] items;
    private static final String WRONG_UPDATE_ADD = "you didn't update correctly after adding";
    private static final String WRONG_UPDATE_REMOVE = "you didn't update correctly after removing";
    private static final String WRONG_MAX_CAPACITY = "wrong max storage capacity";
    private static final String WRONG_RESET_UPDATE = "wrong current locker input after resetting inventory";
    private static final String ERROR_ADDING = "added to locker when the locker didn't have the place for it";
    private static final String ERROR_REMOVING = "removed from locker when the locker shouldn't have been " +
            "changed.";
    private static final int ZERO_APPEARANCE = 0;
    private static final int MAX_TEST_MAX_CAPACITY = 100;
    private static final int FIRST_LOCKER_CAPACITY = 10;
    private static final int SECOND_LOCKER_CAPACITY = 1250;
    private static final int SECOND_LOCKER_CURRENT_CAPACITY = (int)(1250 / 2 * 0.2);
    private static final int BASEBALL = 0;
    private static final int HELMET1 = 1;
    private static final int HELMET3 = 2;
    private static final int ENGINE = 3;
    private static final int FIRST_ADD_NUM = 1;
    private static final int BASEBALL_VALUE = 2;
    private static final int HELMET1_VALUE = 3;
    private static final int HELMET3_VALUE = 5;
    private static final int SECOND_ADD_NUM = 1250 / 2;
    private static final int SUCCESS = 0;
    private static final int FAIL = -1;
    private static final int MOVED_TO_STORAGE = 1;
    private static final int FOOTBALL_ERROR = -2;
    private static final int FOOTBALL = 4;
    /**
     * this function resets the storage before every test
     */
    @BeforeClass
    public static void resetItems(){
        items = ItemFactory.createAllLegalItems();
    }

    /**
     * this function resets the storage before every test
     */
    @Before
    public void resetStorage(){
        new Locker(1).getStorage().resetInventory();
    }

    /**
     * this function checks the function addItem
     */
    @Test
    public void TestAddItem(){
        Locker locker1 = new Locker(FIRST_LOCKER_CAPACITY);
        //try to add a negative number
        assertEquals(WRONG_UPDATE_ADD, FAIL, locker1.addItem(items[BASEBALL], -FIRST_ADD_NUM));

        //add successfully without storage
        assertEquals(WRONG_UPDATE_ADD, SUCCESS, locker1.addItem(items[BASEBALL], FIRST_ADD_NUM));
        assertEquals(WRONG_UPDATE_ADD, SUCCESS, locker1.addItem(items[HELMET1], FIRST_ADD_NUM));
        assertEquals(WRONG_UPDATE_ADD, SUCCESS, locker1.addItem(items[HELMET3], FIRST_ADD_NUM));
        //check error when adding more than the locker can posses
        assertEquals(ERROR_ADDING, FAIL, locker1.addItem(items[ENGINE], FIRST_ADD_NUM));

        //try to remove a negative number
        locker1.removeItem(items[BASEBALL], -FIRST_ADD_NUM);
        //try to remove more than possible
        locker1.removeItem(items[BASEBALL], FIRST_ADD_NUM + 3);

        //clear
        locker1.removeItem(items[BASEBALL], FIRST_ADD_NUM);
        locker1.removeItem(items[HELMET1], FIRST_ADD_NUM);
        locker1.removeItem(items[HELMET3], FIRST_ADD_NUM);

        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        //move to storage and fill it up completely
        assertEquals(ERROR_ADDING, MOVED_TO_STORAGE, locker1.addItem(items[BASEBALL], SECOND_ADD_NUM));
        //try to move to storage again, this time fail due to no place in storage
        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        assertEquals(ERROR_ADDING, FAIL, locker1.addItem(items[BASEBALL], SECOND_ADD_NUM));

        //check football baseball
        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        assertEquals(WRONG_UPDATE_ADD, SUCCESS, locker1.addItem(items[BASEBALL], FIRST_ADD_NUM));
        assertEquals(ERROR_ADDING, FOOTBALL_ERROR, locker1.addItem(items[FOOTBALL], FIRST_ADD_NUM));
    }

    /**
     * this function checks the function removeItem
     */
    @Test
    public void TestRemoveItem(){
        Locker locker1 = new Locker(FIRST_LOCKER_CAPACITY);
        //try to add a negative number
        locker1.addItem(items[BASEBALL], -FIRST_ADD_NUM);

        //add successfully without storage
        locker1.addItem(items[BASEBALL], FIRST_ADD_NUM);
        locker1.addItem(items[HELMET1], FIRST_ADD_NUM);
        locker1.addItem(items[HELMET3], FIRST_ADD_NUM);
        //check error when adding more than the locker can posses
        locker1.addItem(items[ENGINE], FIRST_ADD_NUM);

        //try to remove a negative number
        assertEquals(ERROR_REMOVING, FAIL, locker1.removeItem(items[BASEBALL], -FIRST_ADD_NUM));
        //try to remove more than possible
        assertEquals(ERROR_REMOVING, FAIL, locker1.removeItem(items[BASEBALL], FIRST_ADD_NUM + 1));

        //clear
        assertEquals(WRONG_UPDATE_REMOVE, SUCCESS, locker1.removeItem(items[BASEBALL], FIRST_ADD_NUM));
        assertEquals(WRONG_UPDATE_REMOVE, SUCCESS, locker1.removeItem(items[HELMET1], FIRST_ADD_NUM));
        assertEquals(WRONG_UPDATE_REMOVE, SUCCESS, locker1.removeItem(items[HELMET3], FIRST_ADD_NUM));

        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        //move to storage and fill it up completely
        locker1.addItem(items[BASEBALL], SECOND_ADD_NUM);
        //try to move to storage again, this time fail due to no place in storage
        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        locker1.addItem(items[BASEBALL], SECOND_ADD_NUM);

        //check football baseball
        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        locker1.addItem(items[BASEBALL], FIRST_ADD_NUM);
        locker1.addItem(items[FOOTBALL], FIRST_ADD_NUM);
    }

    /**
     * this function checks the function getItemCount
     */
    @Test
    public void TestGetItemCount(){
        Locker locker1 = new Locker(FIRST_LOCKER_CAPACITY);
        assertEquals(WRONG_RESET_UPDATE, ZERO_APPEARANCE, locker1.getItemCount(items[BASEBALL].getType()));

        //try to add a negative number
        locker1.addItem(items[BASEBALL], -FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, ZERO_APPEARANCE, locker1.getItemCount(items[BASEBALL].getType()));

        //add successfully without storage
        locker1.addItem(items[BASEBALL], FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, FIRST_ADD_NUM, locker1.getItemCount(items[BASEBALL].getType()));
        locker1.addItem(items[HELMET1], FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, FIRST_ADD_NUM, locker1.getItemCount(items[HELMET1].getType()));
        locker1.addItem(items[HELMET3], FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, FIRST_ADD_NUM, locker1.getItemCount(items[HELMET3].getType()));
        //check error when adding more than the locker can posses
        locker1.addItem(items[ENGINE], FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, ZERO_APPEARANCE, locker1.getItemCount(items[ENGINE].getType()));

        //try to remove a negative number
        locker1.removeItem(items[BASEBALL], -FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_REMOVE, FIRST_ADD_NUM, locker1.getItemCount(items[BASEBALL].getType()));

        //try to remove more than possible
        locker1.removeItem(items[BASEBALL], FIRST_ADD_NUM + 1);
        assertEquals(WRONG_UPDATE_REMOVE, FIRST_ADD_NUM, locker1.getItemCount(items[BASEBALL].getType()));

        //clear
        locker1.removeItem(items[BASEBALL], FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_REMOVE, ZERO_APPEARANCE, locker1.getItemCount(items[BASEBALL].getType()));
        locker1.removeItem(items[HELMET1], FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_REMOVE, ZERO_APPEARANCE, locker1.getItemCount(items[HELMET1].getType()));
        locker1.removeItem(items[HELMET3], FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_REMOVE, ZERO_APPEARANCE, locker1.getItemCount(items[HELMET3].getType()));

        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        assertEquals(WRONG_RESET_UPDATE, ZERO_APPEARANCE, locker1.getItemCount(items[BASEBALL].getType()));
        //move to storage and fill it up completely
        locker1.addItem(items[BASEBALL], SECOND_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, SECOND_LOCKER_CURRENT_CAPACITY,
                locker1.getItemCount(items[BASEBALL].getType()));
        //try to move to storage again, this time fail due to no place in storage
        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        assertEquals(WRONG_RESET_UPDATE, ZERO_APPEARANCE, locker1.getItemCount(items[BASEBALL].getType()));
        locker1.addItem(items[BASEBALL], SECOND_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, ZERO_APPEARANCE, locker1.getItemCount(items[BASEBALL].getType()));


        //check football baseball
        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        assertEquals(WRONG_RESET_UPDATE, ZERO_APPEARANCE, locker1.getItemCount(items[BASEBALL].getType()));
        locker1.addItem(items[BASEBALL], FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, FIRST_ADD_NUM, locker1.getItemCount(items[BASEBALL].getType()));
        locker1.addItem(items[FOOTBALL], FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, ZERO_APPEARANCE, locker1.getItemCount(items[FOOTBALL].getType()));
    }

    /**
     * this function checks the function getInventory
     */
    @Test
    public void TestGetInventory(){
        Locker locker1 = new Locker(FIRST_LOCKER_CAPACITY);
        HashMap<String, Integer> testMap = new HashMap<>();
        assertEquals(WRONG_RESET_UPDATE, testMap, locker1.getInventory());

        //try to add a negative number
        locker1.addItem(items[BASEBALL], -FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, testMap, locker1.getInventory());

        //add successfully without storage
        locker1.addItem(items[BASEBALL], FIRST_ADD_NUM);
        testMap.put(items[BASEBALL].getType(), FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, testMap, locker1.getInventory());
        locker1.addItem(items[HELMET1], FIRST_ADD_NUM);
        testMap.put(items[HELMET1].getType(), FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, testMap, locker1.getInventory());
        locker1.addItem(items[HELMET3], FIRST_ADD_NUM);
        testMap.put(items[HELMET3].getType(), FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, testMap, locker1.getInventory());
        //check error when adding more than the locker can posses
        locker1.addItem(items[ENGINE], FIRST_ADD_NUM);
        assertEquals(ERROR_ADDING, testMap, locker1.getInventory());

        //try to remove a negative number
        locker1.removeItem(items[BASEBALL], -FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_REMOVE, testMap, locker1.getInventory());

        //try to remove more than possible
        locker1.removeItem(items[BASEBALL], FIRST_ADD_NUM + 1);
        assertEquals(WRONG_UPDATE_REMOVE, testMap, locker1.getInventory());

        //clear
        locker1.removeItem(items[BASEBALL], FIRST_ADD_NUM);
        testMap.remove(items[BASEBALL].getType());
        assertEquals(WRONG_UPDATE_REMOVE, testMap, locker1.getInventory());
        locker1.removeItem(items[HELMET1], FIRST_ADD_NUM);
        testMap.remove(items[HELMET1].getType());
        assertEquals(WRONG_UPDATE_REMOVE, testMap, locker1.getInventory());
        locker1.removeItem(items[HELMET3], FIRST_ADD_NUM);
        testMap.remove(items[HELMET3].getType());
        assertEquals(WRONG_UPDATE_REMOVE, testMap, locker1.getInventory());

        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        testMap = new HashMap<>();
        assertEquals(WRONG_RESET_UPDATE, testMap, locker1.getInventory());
        //move to storage and fill it up completely
        locker1.addItem(items[BASEBALL], SECOND_ADD_NUM);
        testMap.put(items[BASEBALL].getType(), SECOND_LOCKER_CURRENT_CAPACITY);
        assertEquals(WRONG_UPDATE_ADD, testMap, locker1.getInventory());
        //try to move to storage again, this time fail due to no place in storage
        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        testMap = new HashMap<>();
        assertEquals(WRONG_RESET_UPDATE, testMap, locker1.getInventory());
        locker1.addItem(items[BASEBALL], SECOND_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, testMap, locker1.getInventory());

        //check football baseball
        testMap = new HashMap<>();
        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        assertEquals(WRONG_RESET_UPDATE, testMap, locker1.getInventory());
        locker1.addItem(items[BASEBALL], FIRST_ADD_NUM);
        testMap.put(items[BASEBALL].getType(), FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, testMap, locker1.getInventory());
        locker1.addItem(items[FOOTBALL], FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, testMap, locker1.getInventory());
    }

    /**
     * this function checks the function getAvailableCapacity
     */
    @Test
    public void TestGetAvailableCapacity(){
        Locker locker1 = new Locker(FIRST_LOCKER_CAPACITY);
        assertEquals(WRONG_RESET_UPDATE, FIRST_LOCKER_CAPACITY, locker1.getAvailableCapacity());

        //try to add a negative number
        locker1.addItem(items[BASEBALL], -FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, FIRST_LOCKER_CAPACITY, locker1.getAvailableCapacity());

        //add successfully without storage
        int capacity = FIRST_LOCKER_CAPACITY;
        locker1.addItem(items[BASEBALL], FIRST_ADD_NUM);
        capacity -= FIRST_ADD_NUM * BASEBALL_VALUE;
        assertEquals(WRONG_UPDATE_ADD, capacity, locker1.getAvailableCapacity());
        locker1.addItem(items[HELMET1], FIRST_ADD_NUM);
        capacity -= FIRST_ADD_NUM * HELMET1_VALUE;
        assertEquals(WRONG_UPDATE_ADD, capacity, locker1.getAvailableCapacity());
        locker1.addItem(items[HELMET3], FIRST_ADD_NUM);
        capacity -= FIRST_ADD_NUM * HELMET3_VALUE;
        assertEquals(WRONG_UPDATE_ADD, capacity, locker1.getAvailableCapacity());
        //check error when adding more than the locker can posses
        locker1.addItem(items[ENGINE], FIRST_ADD_NUM);
        assertEquals(ERROR_ADDING, capacity, locker1.getAvailableCapacity());

        //try to remove a negative number
        locker1.removeItem(items[BASEBALL], -FIRST_ADD_NUM);
        assertEquals(WRONG_UPDATE_ADD, capacity, locker1.getAvailableCapacity());

        //try to remove more than possible
        locker1.removeItem(items[BASEBALL], FIRST_ADD_NUM + 1);
        assertEquals(WRONG_UPDATE_ADD, capacity, locker1.getAvailableCapacity());

        //clear
        locker1.removeItem(items[BASEBALL], FIRST_ADD_NUM);
        capacity += FIRST_ADD_NUM * BASEBALL_VALUE;
        assertEquals(WRONG_UPDATE_ADD, capacity, locker1.getAvailableCapacity());
        locker1.removeItem(items[HELMET1], FIRST_ADD_NUM);
        capacity += FIRST_ADD_NUM * HELMET1_VALUE;
        assertEquals(WRONG_UPDATE_ADD, capacity, locker1.getAvailableCapacity());
        locker1.removeItem(items[HELMET3], FIRST_ADD_NUM);
        capacity += FIRST_ADD_NUM * HELMET3_VALUE;
        assertEquals(WRONG_UPDATE_ADD, capacity, locker1.getAvailableCapacity());


        assertEquals(WRONG_RESET_UPDATE, locker1.getStorage().getCapacity(),
                locker1.getStorage().getAvailableCapacity());
        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        assertEquals(WRONG_RESET_UPDATE, SECOND_LOCKER_CAPACITY, locker1.getAvailableCapacity());
        //move to storage and fill it up completely
        locker1.addItem(items[BASEBALL], SECOND_ADD_NUM);
        capacity = SECOND_LOCKER_CAPACITY - SECOND_LOCKER_CURRENT_CAPACITY * BASEBALL_VALUE;
        assertEquals(WRONG_UPDATE_ADD, capacity, locker1.getAvailableCapacity());
        assertEquals(WRONG_UPDATE_ADD, ZERO_APPEARANCE, locker1.getStorage().getAvailableCapacity());
        //try to move to storage again, this time fail due to no place in storage
        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        assertEquals(WRONG_RESET_UPDATE, SECOND_LOCKER_CAPACITY, locker1.getAvailableCapacity());
        locker1.addItem(items[BASEBALL], SECOND_ADD_NUM);
        assertEquals(WRONG_RESET_UPDATE, SECOND_LOCKER_CAPACITY, locker1.getAvailableCapacity());
        assertEquals(WRONG_UPDATE_ADD, ZERO_APPEARANCE, locker1.getStorage().getAvailableCapacity());

        //check football baseball
        locker1 = new Locker(SECOND_LOCKER_CAPACITY);
        assertEquals(WRONG_RESET_UPDATE, SECOND_LOCKER_CAPACITY, locker1.getAvailableCapacity());
        locker1.addItem(items[BASEBALL], FIRST_ADD_NUM);
        capacity = SECOND_LOCKER_CAPACITY - FIRST_ADD_NUM * BASEBALL_VALUE;
        assertEquals(WRONG_RESET_UPDATE, capacity, locker1.getAvailableCapacity());
        locker1.addItem(items[FOOTBALL], FIRST_ADD_NUM);
        assertEquals(WRONG_RESET_UPDATE, capacity, locker1.getAvailableCapacity());
    }

    /**
     * this function checks the getCapacity function
     */
    @Test
    public void TestGetCapacity(){
        for(int i = 1; i < MAX_TEST_MAX_CAPACITY; i++) {
            Locker locker = new Locker(i);
            assertEquals(WRONG_MAX_CAPACITY, i, locker.getCapacity());
        }
    }


}
