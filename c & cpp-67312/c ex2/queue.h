#ifndef QUEUE_H
#define QUEUE_H

/**
 * @brief Describes a node in the queue.
 */
typedef struct queue_node_t
{
    unsigned int data;
    struct queue_node_t* next;
} QueueNode;

/**
 * @brief Describes a simple queue.
 */
typedef struct
{
    QueueNode* head;
    QueueNode* tail;
} Queue;

/**
 * Allocates a new, empty, queue.
 * @return The allocated queue.
 */
Queue* allocQueue();

/**
 * Frees the reference to the given queue pointer from the heap.
 * @param queue The queue to free.
 */
void freeQueue(Queue** queue);

/**
 * Checks whether or not the given queue is empty.
 * @param queue The queue.
 * @return 1 if the queue is empty, 0 otherwise.
 */
int queueIsEmpty(Queue* queue);

/**
 * Enqueues the given value in the beginning of the queue.
 * @param queue The queue.
 * @param value The value to enqueue.
 */
void enqueue(Queue* queue, unsigned int value);

/**
 * Dequeue an item from the given queue.
 * @param queue The queue.
 * @return The dequeued item value, or UINT_MAX if there's no such item.
 * @note UINT_MAX defined in limits.h.
 */
unsigned int dequeue(Queue* queue);

/**
 * Peeks at the value of the queue front item.
 * @param queue The queue.
 * @return The front item value.
 */
unsigned int peekQueue(Queue* queue);

/**
 * Prints the given queue to stdout.
 * @param queue A pointer to the queue.
 */
void printQueue(Queue* queue);

#endif // QUEUE_H
