import java.util.HashSet;
import java.util.LinkedList;
import java.util.TreeSet;

public class SimpleSetPerformanceAnalyzer {

    private static final String[] NAME_CLASS = {"OpenHashSet", "ClosedHashSet", "TreeSet", "LinkedList",
            "HashSet"};
    private static final int[] numberData = {70000, 70000, 70000, 7000, 70000};
    private static final int TO_MILLI_SEC = 1000000;
    private static SimpleSet[] checkClasses;
    private static final String[] DATA_FILES = {"", "_AddData1 = ", "_AddData2 = "};
    private static final String DATA1_HI = "_Contains_hi1 = ";
    private static final String DATA2_HI = "_Contains_hi2 = ";
    private static final String DATA1_NEGATIVE = "_Contains_negative = ";
    private static final String DATA2_23 = "_Contains_23 = ";
    private static final String[] DATA_FILE = {"", "src\\data1.txt","src\\data2.txt"};

    private static final String HI = "hi";
    private static final String CHECK_23 = "23";
    private static final String NEGATIVE = "-13170890158";

    public static void main(String[] args){
        System.out.println();
        testData(1);
        System.out.println();
        testContains(DATA1_HI, HI, 1);
        System.out.println();
        testContains(DATA1_NEGATIVE, NEGATIVE, 1);

        System.out.println();
        System.out.println();
        testData(2);
        System.out.println();
        testContains(DATA2_23, CHECK_23, 2);
        System.out.println();
        testContains(DATA2_HI, HI, 2);
    }

    /**
     * this function handles init of the hashes to check (clears them too)
     */
    private static void initCheckClasses(){
        checkClasses = new SimpleSet[5];
        checkClasses[0] = new OpenHashSet();
        checkClasses[1] = new ClosedHashSet();
        checkClasses[2] = new CollectionFacadeSet(new TreeSet<>());
        checkClasses[3] = new CollectionFacadeSet(new LinkedList<>());
        checkClasses[4] = new CollectionFacadeSet(new HashSet<>());
    }

    /**
     * @param fileNumber gets a file number
     * prints how much time it took to run the file and to add each element to the hash
     */
    private static void testData(int fileNumber){
        initCheckClasses();
        String dataFile = DATA_FILE[fileNumber];

        String[] data = Ex4Utils.file2array(dataFile);
        if (data == null)
            data = new String[0];
        for(int i = 0; i < checkClasses.length; i++){
            long timeBefore = System.nanoTime();
            for(String s: data)
                checkClasses[i].add(s);
            long timeAfter = System.nanoTime();
            System.out.println(NAME_CLASS[i] + DATA_FILES[fileNumber] + (timeAfter - timeBefore)
                    / TO_MILLI_SEC);
        }
    }

    /**
     * this function handles the contains test
     * @param printString the String to print to the user
     * @param value the value to check if contained in sets
     * @param number a file Number to load if the user want to check this without the other tests (remove
     *               commented line)
     */
    private static void testContains(String printString, String value, int number){
        //loadData(DATA_FILE[number]); //if u want to check alone without assuming the data is loaded
        for(int i = 0; i < checkClasses.length; i++){
            int diffTime = checkContains(checkClasses[i], numberData[i], value);
            System.out.println(NAME_CLASS[i] + printString + diffTime);
        }
    }

    /**
     * @param set get a Simple set
     * @param number get a number of how many times to run
     * @param s the string to check if contained
     * @return the time it took to check contains s number times
     */
    private static int checkContains(SimpleSet set, int number, String s){
        for(int i = 0; i < number; i++)
            set.contains(s);
        long timeBefore = System.nanoTime();
        for(int i = 0; i < number; i++)
            set.contains(s);
        long timeAfter = System.nanoTime();
        return (int) ((timeAfter - timeBefore) / number);

    }

    /**
     * @param dataFile gets a file path
     * this function loads the data into the hashes to check contains later
     */
    private static void loadData(String dataFile){
        initCheckClasses();
        String[] data = Ex4Utils.file2array(dataFile);
        if (data == null)
            data = new String[0];
        for(SimpleSet hash: checkClasses)
            for(String s: data)
                hash.add(s);
    }
}
