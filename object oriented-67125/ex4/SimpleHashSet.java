public abstract class SimpleHashSet implements  SimpleSet {
    /* Describes the higher load factor of a newly created hash set */
    protected static float DEFAULT_HIGHER_CAPACITY = 0.75f;

    /* Describes the lower load factor of a newly created hash set */
    protected static final float DEFAULT_LOWER_CAPACITY = 0.25f;

    /* Describes the capacity of a newly created hash set */
    protected static final int INITIAL_CAPACITY = 16;

    /* a constant representing how much the hash should grow each time */
    protected static final int resizeFactor = 2;

    /* the current capacity */
    protected int capacity;

    /* the lower load factor of the set */
    private float lowerLoadFactor;

    /* the higher load factor of the set */
    private float higherLoadFactor;

    /* the current size of the table */
    protected int size = 0;

    /**
     * Constructs a new hash set with the default capacities given in DEFAULT_LOWER_CAPACITY and
     * DEFAULT_HIGHER_CAPACITY
     */
    SimpleHashSet(){
       this.capacity = INITIAL_CAPACITY;
       this.lowerLoadFactor = DEFAULT_LOWER_CAPACITY;
       this.higherLoadFactor = DEFAULT_HIGHER_CAPACITY;
    }

    /**
     *  Constructs a new hash set with capacity INITIAL_CAPACITY
     * @param upperLoadFactor the higher load factor of the set
     * @param lowerLoadFactor the lower load factor of the set
     */
    SimpleHashSet(float upperLoadFactor, float lowerLoadFactor){
        this.capacity = INITIAL_CAPACITY;
        this.lowerLoadFactor = lowerLoadFactor;
        this.higherLoadFactor = upperLoadFactor;
    }

    /**
     * @return The current capacity (number of cells) of the table.
     */
    public int capacity(){
        return capacity;
    }

    /**
     * Clamps hashing indices to fit within the current table capacity (see the exercise description for
     * details)
     * @param index the index before clamping
     * @return an index properly clamped
     */
    protected int clamp(int index){
        return index & (capacity - 1);
    }

    /**
     * @return The lower load factor of the table.
     */
    protected float getLowerLoadFactor(){
        return this.lowerLoadFactor;
    }

    /**
     * @return The higher load factor of the table.
     */
    protected float getUpperLoadFactor(){
        return this.higherLoadFactor;
    }


    /**
     * @return The number of elements currently in the set
     */
    public int size() {
        return size;
    }
}
