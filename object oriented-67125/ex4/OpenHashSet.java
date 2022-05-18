import java.util.LinkedList;

public class OpenHashSet extends SimpleHashSet {

    /* this holds the table hash of the set */
    private WrapperLinkedList[] hashTable;

    /**
     * A default constructor. Constructs a new, empty table with default initial capacity (16), upper load
     * factor (0.75) and lower load factor (0.25).
     */
    public OpenHashSet(){
        super();
        reset();
    }

    /**
     * Constructs a new, empty table with the specified load factors, and the default initial capacity (16).
     * @param upperLoadFactor The upper load factor of the hash table.
     * @param lowerLoadFactor The lower load factor of the hash table.
     */
    public OpenHashSet(float upperLoadFactor, float lowerLoadFactor){
        super(upperLoadFactor, lowerLoadFactor);
        reset();
    }

    /**
     * Data constructor - builds the hash set by adding the elements one by one. Duplicate values should be
     * ignored. The new table has the default values of initial capacity (16), upper load factor (0.75),
     * and lower load factor (0.25).
     * @param data Values to add to the set.
     */
    public OpenHashSet(String[] data){
        super();
        reset();
        for(String s: data)
            add(s);
    }

    /**
     * Add a specified element to the set if it's not already in it.
     * @param newValue New value to add to the set
     * @return False iff newValue already exists in the set
     */
    @Override
    public boolean add(String newValue) {
        if(contains(newValue))
            return false;
        if((size() + 1) > getUpperLoadFactor() * capacity())
            resizeTable(resizeFactor * capacity());
        addToTable(newValue);
        return true;
    }

    /**
     * this function handles resizing the table, by adding everything from 0
     * @param newCapacity the new capacity to resize the table to
     */
    private void resizeTable(int newCapacity){
        capacity = Math.max(newCapacity, 1);
        WrapperLinkedList[] newHashTable = hashTable;
        reset();
        for(WrapperLinkedList list: newHashTable)
            updateCollectionResize(list);
    }

    /**
     * @param list a list of elements from the hash
     * this function adds all the values from the list to the new table
     */
    private void updateCollectionResize(WrapperLinkedList list) {
        LinkedList<String> strings = list.getList();
        for(String s: strings)
            addToTable(s);
    }

    /**
     * Add a specified element to the set.
     * @param newValue New value to add to the set
     */
    private void addToTable(String newValue) {
        size++;
        hashTable[clamp(newValue.hashCode())].add(newValue);
    }

    /**
     * Look for a specified value in the set.
     * @param searchVal Value to search for
     * @return True iff searchVal is found in the set
     */
    @Override
    public boolean contains(String searchVal) {
        return hashTable[clamp(searchVal.hashCode())].contains(searchVal);
    }

    /**
     * Remove the input element from the set.
     * @param toDelete Value to delete
     * @return True iff toDelete is found and deleted
     */
    @Override
    public boolean delete(String toDelete) {
        if(!contains(toDelete))
            return false;
        boolean deleted = hashTable[clamp(toDelete.hashCode())].delete(toDelete);
        size--;
        if((size() - 1) <  getLowerLoadFactor() * capacity())
            resizeTable(capacity() / resizeFactor);
        return deleted;
    }


    /**
     * this function reset the set and the table
     */
    private void reset(){
        hashTable = resetFacadeArray(capacity());
        size = 0;
    }

    /**
     * @param capacity get a new capacity
     * @return returns an empty table of length capacity
     */
    private WrapperLinkedList[] resetFacadeArray(int capacity){
        WrapperLinkedList[]  table = new WrapperLinkedList[capacity];
        for(int i = 0; i < table.length; i++)
            table[i] = new WrapperLinkedList(new LinkedList<>());
        return table;
    }
}
