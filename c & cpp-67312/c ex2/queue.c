#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <limits.h>
#include "queue.h"

/**
 * Allocates a new, empty, queue.
 * @return The queue.
 */
Queue* allocQueue()
{
    Queue* q = malloc(sizeof(Queue));
    assert(q != NULL);

    q->head = NULL;
    q->tail = NULL;

    return q;
}

/**
 * Frees the given queue.
 * @param queue The queue to free.
 */
void freeQueue(Queue** queue)
{
    /* If we already free'd the memory, we shall stop here */
    if (*queue == NULL)
    {
        return;
    }

    /* If the queue is not empty, free all of it's items.
     * Remember: free'ing the Queue object alone won't free its
     * nodes - which means they'll cause a memory leak. */
    QueueNode* ptr = (*queue)->head;
    QueueNode* next = NULL;
    while (ptr != NULL)
    {
        next = ptr->next;
        free(ptr);
        ptr = next;
    }
    (*queue)->head = NULL;
    (*queue)->tail = NULL;

    /* Now we can free the queue itself and mark it as NULL so we can
     * know that it was de-allocated. */
    free(*queue);
    *queue = NULL;
}

/**
 * Checks whether or not the queue is empty.
 * @param queue The queue.
 * @return 1 if it's empty, false otherwise.
 */
int queueIsEmpty(Queue* queue)
{
    return queue->head == NULL;
}

/**
 * Enqueues the given value.
 * @param queue The queue.
 * @param value The value to enqueue.
 */
void enqueue(Queue* queue, unsigned int value)
{
    /* Allocates a new queue item */
    QueueNode* item = malloc(sizeof(QueueNode));
    assert(item != NULL);

    item->data = value;
    item->next = NULL;

    /* Connect */
    if (queue->head == NULL)
    {
        queue->head = queue->tail = item;
    }
    else
    {
        queue->tail = queue->tail->next = item;
    }
}

/**
 * Dequeues an item from the given queue.
 * @param queue The queue.
 * @return The dequeued item value, or INT_MIN if there's no such item.
 */
unsigned int dequeue(Queue* queue)
{
    if (queueIsEmpty(queue))
    {
        return UINT_MAX;
    }

    /* Save the removed value */
    unsigned int value = queue->head->data;
    QueueNode* next = queue->head->next;

    /* Remove from the queue head */
    free(queue->head);
    queue->head = next;

    if (queue->head == NULL)
    {
        queue->tail = NULL;
    }

    return value;
}

/**
 * Peeks at the value of the queue front item.
 * @param queue The queue.
 * @return The front item value.
 */
unsigned int peekQueue(Queue* queue)
{
    return queue->head->data;
}


/**
 * Prints the given queue to stdout.
 * @param queue A pointer to the queue.
 */
void printQueue(Queue* queue)
{
    if (queue->head == NULL)
    {
        printf("[]");
        return;
    }

    QueueNode* ptr = queue->head;

    printf("[head -> ");
    while (ptr != NULL)
    {
        printf("[%d]", ptr->data);
        ptr = ptr->next;
    }

    printf(" <- tail]\n");
}
