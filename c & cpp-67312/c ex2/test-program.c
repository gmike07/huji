#include <stdio.h>
#include <stdlib.h>
#include "queue.h"

/**
 * @brief The main function that runs the program.
 * @param argc Non-negative value representing the number of arguments passed
 * to the program from the environment in which the program is run.
 * @param argv Pointer to the first element of an array of pointers to null-terminated
 * multibyte strings that represent the arguments passed to the program from the execution
 * environment. The value of argv[argc] is guaranteed to be a null pointer.
 * @return 0, to tell the system the execution ended without errors, or 1, to
 * tell the system that the code has executione errors.
 */
int main()
{
    /* Allocates a new queue */
    Queue* q = allocQueue();

    /* Read numbers until we tackle -1 */
    int number = 0;
    while (1)
    {
        printf("Add a positive number to the queue (-1 to stop):\n");
        /* !! WARNING !!
         * As mentioned in the course guidelines, "scanf" is not safe and thus you shouldn't
         * use it! This code is meant only to test and demonstrate queue.h! */
        scanf("%d", &number);
        if (number < 0)
        {
            break;
        }

        /* Add to the queue */
        enqueue(q, number);
    }

    /* Display */
    printQueue(q);

    /* Frees the allocated queue */
    freeQueue(&q);
    return EXIT_SUCCESS;
}