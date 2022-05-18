#include <stdio.h>
#include <string.h>
/**
 * @def STUDENT_INFO_STRING
 * @brief A macro that sets the student info string to be the request
 */
#define STUDENT_INFO_STRING "Enter student info. To exit press q, then enter\n"
/**
 * @def MAX_LENGTH_LINE 150
 * @brief A macro that sets the maximal length of a user's line input
 */
#define MAX_LENGTH_LINE 150
/**
 * @def MAX_NUMBER_STUDENTS 5000
 * @brief A macro that sets the maximal number of students to hold to be 5000
 */
#define MAX_NUMBER_STUDENTS 5000
/**
 * @def MAX_LENGTH_INPUT 40
 * @brief A macro that sets the maximal length of every input to 40
 */
#define MAX_LENGTH_INPUT 40
/**
 * @def MAX_AGE 120
 * @brief A macro that sets the id length to be 10
 */
#define ID_LENGTH 10
/**
 * @def MIN_AGE 18
 * @brief A macro that sets the minimal age allowed to be 18
 */
#define MIN_AGE 18
/**
 * @def MAX_AGE 120
 * @brief A macro that sets the maximal age allowed to be 120
 */
#define MAX_AGE 120
/**
 * @def MIN_GRADE 0
 * @brief A macro that sets the minimal grade allowed to be 0
 */
#define MIN_GRADE 0
/**
 * @def MAX_GRADE 100
 * @brief A macro that sets the maximal grade allowed to be 100
 */
#define MAX_GRADE 100
/**
 * @def REGEX_SSCANF
 * @brief A macro that sets REGEX_SSCANF to be a regex that checks most of the required things
 */
#define REGEX_SSCANF "%[0-9]%[\t]%[a-zA-Z -]%[\t]%[0-9]%[\t]%[0-9]%[\t]%[a-zA-Z-]%[\t]%[a-zA-Z-]%[\t]"
/**
 * @def STUDENT_PRINT_FORMAT
 * @brief A macro that sets STUDENT_PRINT_FORMAT to be a regex that prints the student
 */
#define STUDENT_PRINT_FORMAT "%s\t%s\t%d\t%d\t%s\t%s\t\n"
/**
 * @def ERROR_FORMAT
 * @brief A macro that sets ERROR_FORMAT to be a regex that prints the error
 */
#define ERROR_FORMAT "ERROR: the info you entered is not in the correct format \nin line %d\n"
/**
* @def USAGE_WRONG
* @brief A macro that sets the USAGE_WRONG to be an informative msg that the usage of the
* program is wrong
*/
#define USAGE_WRONG "USAGE: to use the program enter one argument that is best, merge or quick"
/**
 * @def BEST_STUDENT
 * @brief A macro that sets the BEST_STUDENT to be the constant to be the best student input to
 * the cmd
 */
#define BEST_STUDENT "best"
/**
 * @def MERGE_STUDENTS
 * @brief A macro that sets the MERGE_STUDENTS to be the constant to be the merge sort input to
 * the cmd
 */
#define MERGE_STUDENTS "merge"
/**
 * @def QUICK_STUDENTS
 * @brief A macro that sets the QUICK_STUDENTS to be the constant to be the quick sort input to
 * the cmd
 */
#define QUICK_STUDENTS "quick"
/**
 * @def BEST_STUDENT_STRING
 * @brief A macro that sets the BEST_STUDENT_STRING to be the string of the best student
 */
#define BEST_STUDENT_STRING "best student info is: "
/**
 * @def NUMBER_OF_STUDENT_PROPERTIES
 * @brief A macro that sets the NUMBER_OF_STUDENT_PROPERTIES to be the number of student
 * properties to get by the sscanf
 */
#define NUMBER_OF_STUDENT_PROPERTIES 6

/**
 * @def ERROR_CANNOT_READ
 * @brief A macro that sets the ERROR_CANNOT_READ to be the cannot read error
 */
#define ERROR_CANNOT_READ "ERROR: could not read the stdin\n"
/**
 * @def END_PROGRAM_INPUT1
 * @brief A macro that sets the END_PROGRAM_INPUT1 to be the q\n
 */
#define END_PROGRAM_INPUT1 "q\n"
/**
 * @def END_PROGRAM_INPUT2
 * @brief A macro that sets the END_PROGRAM_INPUT2 to be q\r\n
 */
#define END_PROGRAM_INPUT2 "q\r\n"
/**
 * @def Student
 * @brief the student struct, contains every trait the student has and a scoringSystem for the
 * merge sort algorithm.
 */
typedef struct Student
{
    char id[MAX_LENGTH_INPUT + 1];
    char name[MAX_LENGTH_INPUT + 1];
    char country[MAX_LENGTH_INPUT + 1];
    char city[MAX_LENGTH_INPUT + 1];
    float scoringSystem;
    int grade;
    int age;
} Student;

/**
 * @brief the helper array to the merge function
 */
Student gArrayHelperMerge[MAX_NUMBER_STUDENTS] = { 0};
/**
 * @brief the students array
 */
Student gStudents[MAX_NUMBER_STUDENTS] = {0};

/**
 * @brief the helper function of the quickSort algorithm, finds an index i (after replacing) such
 * that makes arr[j] < arr[i] for all j < i and arr[j] >= arr[i] for all j > i
 * @param arr, an array of students
 * @param start, the start of the array
 * @param end, the end of the array
 * @return the found index
 */
int partition(Student arr[], int start, int end)
{
    Student pivot = arr[end];
    int i = start;
    for(int j = start; j < end; j++)
    {
        if(strcmp(arr[j].name, pivot.name) < 0)
        {
            Student temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
            i++;
        }
    }
    Student temp = arr[i];
    arr[i] = arr[end];
    arr[end] = temp;
    return i;
}

/**
 * @brief sorts the array up to length with the quickSort algorithm
 * @param arr, an array of students
 * @param start, the start of the array
 * @param end, the end of the array
 * the updated array sorted (in place) with quickSort algorithm from start to end
 */
void quickSortHelper(Student arr[], int start, int end)
{
    if(start < end)
    {
        int p = partition(arr, start, end);
        quickSortHelper(arr, start, p - 1);
        quickSortHelper(arr, p + 1, end);
    }
}

/**
 * @brief sorts the array up to length with the quickSort algorithm
 * @param arr, an array of students
 * @param length, the length of the array
 *the updated array sorted (in place) with quickSort algorithm
 */
void quickSort(Student arr[], int length)
{
    quickSortHelper(arr, 0, length - 1);
}

/**
 * @brief sorts the array up to length with the mergeSort algorithm
 * @param arr, an array of students
 * @param start, the start of the array
 * @param mid, the mid of the array
 * @param end, the end of the array
 * merges the arr[start:mid] (sorted) and arr[mid:end] (sorted) in place
 */
void merge(Student arr[], int start, int mid, int end)
{
    int i = 0, j = 0;
    int length1 = mid - start, length2 = end - mid;
    while((i < length1) || (j < length2))
    {
        if(j == length2)
        {
            gArrayHelperMerge[i + j] = arr[start + i];
            i++;
        }
        else if((i == length1) || (arr[mid + j].scoringSystem < arr[start + i].scoringSystem))
        {
            gArrayHelperMerge[i + j] = arr[mid + j];
            j++;
        }
        else
        {
            gArrayHelperMerge[i + j] = arr[start + i];
            i++;
        }
    }
    for(i = 0; i < end - start; i++)
    {
        arr[start + i] = gArrayHelperMerge[i];
    }
}

/**
 * @brief sorts the array up to length with the mergeSort algorithm
 * @param arr, an array of students
 * @param start, the start of the array
 * @param end, the end of the array
 * the updated array sorted (in place) with mergeSort algorithm from start to end
 */
void mergeSortHelper(Student arr[], int start, int end)
{
    if(end == start + 1)
    {
        return;
    }
    int mid = (start + end) / 2;
    mergeSortHelper(arr, start, mid);
    mergeSortHelper(arr, mid, end);
    merge(arr, start, mid, end);
}
/**
 * @brief sorts the array up to length with the mergeSort algorithm
 * @param arr, an array of students
 * @param length, the length of the array
 * the updated array sorted (in place) with mergeSort algorithm
 */
void mergeSort(Student arr[], int length)
{
    mergeSortHelper(arr, 0, length);
}
/**
 * @brief converts the string to int if possible, else returns -1
 * @param string, the string to convert to int
 * @return the int of string if converted, else -1
 */
int convertToInt(char string[MAX_LENGTH_INPUT])
{
    int num = 0;
    int digit;
    for(unsigned int i = 0; i < strlen(string); i++)
    {
        digit = string[i] - '0';
        if((digit < 0) || (digit > 9))
        {
            return -1;
        }
        num = num * 10 + digit;
    }
    return num;
}

/**
 * @brief checks whether min <= num <= max
 * @param num, the number to check
 * @param min, the min to compare against
 * @param max, the max to compare against
 * @return true if  min <= num <= max else false (-1,0)
 */
int isInRange(int num, int min, int max)
{
    return (min <= num) && (num <= max);
}

/**
 * @brief if string is tab
 * @param string to check
 * @return if string is tab
 */
int isTab(char str[])
{
    return str[0] == '\t' && strlen(str) == 1;
}

/**
 * @brief gets an array of students, updates the one in index index with the line input
 * @param students, an array of students to update
 * @param index, the index to update.
 * @param line, the user's input line
 * @param lineNumber, to print the error line
 * @return 0 if the line is valid and the update aws successful else -1
 */
int checkStudent(Student students[], int index, char input[], int lineNumber)
{
    char stringAge[MAX_LENGTH_INPUT + 1], stringGrade[MAX_LENGTH_INPUT + 1];
    //checks that id, age, grade has only numbers, that name has a-zA-Z - and ' ',  and city,
    // country has only a-zA-Z -. stores them and returns 6 if was successful
    char charHelper1[2], charHelper2[2], charHelper3[2], charHelper4[2], charHelper5[2], charHelper6[2];
    int numberFound = sscanf(input, REGEX_SSCANF, students[index].id, charHelper1, students[index].name, charHelper2,
                             stringGrade, charHelper3, stringAge, charHelper4, students[index].country, charHelper5,
                             students[index].city, charHelper6);
    students[index].grade = convertToInt(stringGrade);
    students[index].age = convertToInt(stringAge);
    if(numberFound == NUMBER_OF_STUDENT_PROPERTIES + 6) //didn't find all the properties
    {
        if(strlen(students[index].id) == ID_LENGTH
           && strlen(students[index].name) != 0
           && isInRange(students[index].grade, MIN_GRADE, MAX_GRADE)
           && isInRange(students[index].age, MIN_AGE, MAX_AGE)
           && strlen(students[index].country) != 0
           && strlen(students[index].city) != 0
           && isTab(charHelper1) && isTab(charHelper2) && isTab(charHelper3) && isTab(charHelper4)
           && isTab(charHelper5) && isTab(charHelper6))
        {
            return 0;
        }
    }
    printf(ERROR_FORMAT, lineNumber);
    return -1;

}

/**
 * @brief gets an array of students, updates it with input from the user when valid
 * @param students, an array of students to update
 * @return the number of students in the updated students array, -1 if error
 */
int readStudents(Student students[MAX_NUMBER_STUDENTS])
{
    char line[MAX_LENGTH_LINE + 1] = {0};
    printf(STUDENT_INFO_STRING);
    if(fgets(line, MAX_LENGTH_LINE + 1, stdin) == NULL) // an error occur
    {
        printf(ERROR_CANNOT_READ);
        return -1;
    }
    int i = 0;
    int lineNumber = 0;
    while(strcmp(line, END_PROGRAM_INPUT1) != 0 && strcmp(line, END_PROGRAM_INPUT2) != 0
          && i < MAX_NUMBER_STUDENTS)
    {
        if(!checkStudent(students, i, line, lineNumber)) //if the student is valid, save him
        {
            i++;
        }
        lineNumber++;
        printf(STUDENT_INFO_STRING);
        if(fgets(line, MAX_LENGTH_LINE + 1, stdin) == NULL) // an error occur
        {
            printf(ERROR_CANNOT_READ);
            return -1;
        }
    }
    return i;
}

/**
 * @brief prints the student
 * @param s, the student to print
 */
void printStudent(Student s)
{
    printf(STUDENT_PRINT_FORMAT, s.id, s.name, s.grade, s.age, s.country, s.city);
}

/**
 * @brief gets an array of students and the length of the array and prints the students
 * @param students, an array of students to print
 * @param length, the length of the array to print
 * @return nothing
 */
void printStudents(Student students[MAX_NUMBER_STUDENTS], int length)
{
    for(int i = 0; i < length; i++)
    {
        printStudent(students[i]);
    }
}

/**
 * @brief gets input on students, sorts (by grade / age)
 * then with merge sort and prints the best one
 * @return 0, if ran as needed, else -1
 */
int handleBestStudent()
{
    int length = readStudents(gStudents);
    if(length == -1)
    {
        return -1;
    }
    for(int i = 0; i < length; i++)
    {
        gStudents[i].scoringSystem = (float)gStudents[i].grade / (float)gStudents[i].age;
    }
    if(length == 0)
    {
        return 0;
    }
    int bestIndex = 0;
    for(int i = 0; i < length; i++)
    {
        if(gStudents[i].scoringSystem > gStudents[bestIndex].scoringSystem)
        {
            bestIndex = i;
        }
    }
    printf(BEST_STUDENT_STRING);
    printStudent(gStudents[bestIndex]);
    return 0;
}
/**
 * @brief gets input on students, sorts (by grade) then with merge sort and prints them
 * @return 0, if ran as needed, else -1
 */
int handleMergeCommand()
{
    int length = readStudents(gStudents);
    if(length == -1)
    {
        return -1;
    }
    for(int i = 0; i < length; i++)
    {
        gStudents[i].scoringSystem = ((float)gStudents[i].grade);
    }
    if(length == 0)
    {
        return 0;
    }
    mergeSort(gStudents, length);
    printStudents(gStudents, length);
    return 0;
}

/**
 * @brief gets input on students, sorts (by name) then with quick sort and prints them
 * @return 0, if ran as needed, else -1
 */
int handleQuickCommand()
{
    int length = readStudents(gStudents);
    if(length == -1)
    {
        return -1;
    }
    if(length == 0)
    {
        return 0;
    }
    quickSort(gStudents, length);
    printStudents(gStudents, length);
    return 0;
}

/**
 * @brief The main function. handles which type of sort to call
 * @return 0, if ran as needed, it the cmd command was wrong then return -1 and if an error
 * occured then -1
 */
int main(int argc, char* argv[])
{
    if(argc != 2)
    {
        printf(USAGE_WRONG);
        return 1;
    }
    if(strcmp(argv[1], BEST_STUDENT) == 0)
    {
        return handleBestStudent();
    }
    else if(strcmp(argv[1], MERGE_STUDENTS) == 0)
    {
        return handleMergeCommand();
    }
    else if(strcmp(argv[1], QUICK_STUDENTS) == 0)
    {
        return handleQuickCommand();
    }
    else
    {
        printf(USAGE_WRONG);
        return 1;
    }
}