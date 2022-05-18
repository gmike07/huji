public class ClosedHashSet extends SimpleHashSet {

    /* the current table of the hash set */
    private Object[] hashTable;

    /* an object to show that the cell os empty */
    private Object emptyCell = new Object();



    /**
     * A default constructor. Constructs a new, empty table with default initial capacity (16), upper load
     * factor (0.75) and lower load factor (0.25).
     */
    public ClosedHashSet(){
        super();
        reset();
    }

    /**
     * Constructs a new, empty table with the specified load factors, and the default initial capacity (16).
     * @param upperLoadFactor The upper load factor of the hash table.
     * @param lowerLoadFactor The lower load factor of the hash table.
     */
    public ClosedHashSet(float upperLoadFactor, float lowerLoadFactor){
        super(upperLoadFactor, lowerLoadFactor);
        reset();
    }

    /**
     * Data constructor - builds the hash set by adding the elements one by one. Duplicate values should be
     * ignored. The new table has the default values of initial capacity (16), upper load factor (0.75),
     * and lower load factor (0.25).
     * @param data Values to add to the set.
     */
    public ClosedHashSet(String[] data){
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
        int index = findEmptyIndex(newValue);
        if(index == -1)
            return false;
        if((size() + 1) > getUpperLoadFactor() * capacity()) {
            resizeTable(resizeFactor * capacity());
            return addValueAtIndex(newValue,  findEmptyIndex(newValue));
        }
        return addValueAtIndex(newValue, index);
    }

    /**
     * @param value the  value to search an empty cell for
     * @return the first empty index if such exists, else -1
     */
    private int findEmptyIndex(String value){
        int hash = value.hashCode();
        for(int i = 0; i < hashTable.length; i++){
            int index = getIndex(hash, i);
            if(hashTable[index] == null || hashTable[index] == emptyCell)
                return index;
            if(hashTable[index].equals(value))
                return -1;
        }
        return -1;
    }

    /**
     * Add a specified element to the set if it's not already in it.
     * @param newValue New value to add to the set
     */
    private void addToTable(String newValue) {
        int hash = newValue.hashCode();
        for(int i = 0; i < hashTable.length; i++){
            int index = getIndex(hash, i);
            if(hashTable[index] == null || hashTable[index] == emptyCell){
                addValueAtIndex(newValue, index);
                return;
            }
            if(hashTable[index].equals(newValue))
                return;
        }
    }

    /**
     * this function adds a value to the table at place index and returns true
     * @param newValue the value to add to the table
     * @param index the index where to add the value
     * @return true
     */
    private boolean addValueAtIndex(String newValue, int index) {
        hashTable[index] = newValue;
        size++;
        return true;
    }


    /**
     * this function handles resizing the table, by adding everything from 0
     * @param newCapacity the new capacity to resize the table to
     */
    private void resizeTable(int newCapacity){
        capacity = Math.max(newCapacity, 1);
        Object[] newHashTable = hashTable;
        reset();
        for(Object o: newHashTable)
            if (o != null && o != emptyCell)
                addToTable((String)o);
    }

    /**
     * this function resets the table and size of the hash table
     */
    private void reset() {
        hashTable = new Object[capacity];
        size = 0;
    }

    /**
     * @param hash the hash code
     * @param i int index
     * @return the index in the table of value for the i try
     */
    private int getIndex(int hash, int i) {
        return clamp(hash + (i + i * i) / 2);
    }

    /**
     * Look for a specified value in the set.
     * @param searchVal Value to search for
     * @return True iff searchVal is found in the set
     */
    @Override
    public boolean contains(String searchVal) {
        int hash = searchVal.hashCode();
        for(int i = 0; i < hashTable.length; i++){
            int index = getIndex(hash, i);
            if(hashTable[index] == null)
                return false;
            else if(hashTable[index] == emptyCell){
                continue;
            }
            else if(hashTable[index].equals(searchVal))
                return true;
        }
        return false;
    }

    /**
     * Remove the input element from the set.
     * @param toDelete Value to delete
     * @return True iff toDelete is found and deleted
     */
    @Override
    public boolean delete(String toDelete) {
        int hash = toDelete.hashCode();
        for(int i = 0; i < hashTable.length; i++){
            int index = getIndex(hash, i);
            if(hashTable[index] == null)
                return false;
            else if(hashTable[index] == emptyCell){
                continue;
            }
            else if(hashTable[index].equals(toDelete)){
                hashTable[index] = emptyCell;
                size--;
                if(size() < getLowerLoadFactor() * capacity())
                    resizeTable(capacity() / resizeFactor);
                return true;
            }
        }
        return false;
    }
}
