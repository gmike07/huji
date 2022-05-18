import java.util.LinkedList;

public class WrapperLinkedList {
    private LinkedList<String> linkedList;
    public WrapperLinkedList(LinkedList<String> linkedList){
        this.linkedList = linkedList;
    }

    /**
     * Add a specified element to the list.
     * @param newValue New value to add to the list
     * @return true if succeed adding, else false
     */
    public boolean add(String newValue){
        return linkedList.add(newValue);
    }

    /**
     * Remove the input element from the list.
     * @param toDelete Value to delete
     * @return True iff toDelete is found and deleted
     */
    public boolean delete(String toDelete){
        return linkedList.remove(toDelete);
    }

    /**
     * Look for a specified value in the list.
     * @param searchVal Value to search for
     * @return True iff searchVal is found in the list
     */
    public boolean contains(String searchVal){
        return linkedList.contains(searchVal);
    }

    /**
     * @return the elements currently in the list
     */
    public LinkedList<String> getList(){
        return linkedList;
    }
}
