
public interface SimpleSet {
	/**
	 * Add a specified element to the set if it's not already in it.
	 * @param newValue New value to add to the set
	 * @return False iff newValue already exists in the set
	 */
	boolean add(String newValue);
	/**
	 * Look for a specified value in the set.
	 * @param searchVal Value to search for
	 * @return True iff searchVal is found in the set
	 */
	boolean contains(String searchVal);
	/**
	 * Remove the input element from the set.
	 * @param toDelete Value to delete
	 * @return True iff toDelete is found and deleted
	 */
	boolean delete(String toDelete);
	/**
	 * @return The number of elements currently in the set
	 */
	public int size();
}
