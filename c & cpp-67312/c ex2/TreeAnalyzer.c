#include <stdio.h>
#include "queue.h"
#include <string.h>
#include <limits.h>
#include <stdlib.h>

#define MAX_LINE_LIMIT (1024 + 1)
#define INVALID_INPUT_ERROR "Invalid input\n"
#define USAGE_INPUT_ERROR "Usage: TreeAnalyzer <Graph File Path> <First Vertex> <Second Vertex>\n"

#define ROOT_STRING "Root Vertex: %d\n"
#define VERTICES_STRING "Vertices Count: %d\n"
#define EDGES_STRING "Edges Count: %d\n"
#define MIN_BRANCH_STRING "Length of Minimal Branch: %d\n"
#define MAX_BRANCH_STRING "Length of Maximal Branch: %d\n"
#define DIAMETER_STRING "Diameter Length: %d\n"
#define SHORTEST_PATH_STRING "Shortest Path Between %d and %d:"
#define MEMORY_ALLOC_ERROR "Memory allocation failed\n"

/**
 * the Node object represents a vertex of the tree
 */
typedef struct Node
{
    Queue *childrenList; //the children of the node
    struct Node *dad; //the dad of the node
    struct Node *prev; //the previous one for the bfs run
    struct Node *next; //the next one for the bfs run
    int value; //the value of the node
    int dist; //the distance from the start for the bfs run
} Node;

/**
 * the Tree object represents a tree
 */
typedef struct Tree
{
    Node *nodes; //the nodes of the tree
    int numberOfNodes; //the number of nodes in the tree
    int numberOfEdges; //the amount of edges in the tree
} Tree;

/**
 * @brief returns whether the double is an int
 * @param d the number to check
 * @return EXIT_FAILURE if it is not an int, else EXIT_SUCCESS
 */
int isInteger(double number);
/**
 * @brief get a node reference and its value and initialize that node with the value given
 * @param node the node to initialize
 * @param index the value of the node
 */
void initNode(Node *node, int index);
/**
 * @brief gets the length of the tree and returns a tree pointer to a tree with that length
 * @param n the number of nodes for the tree
 * @return a tree pointer to the new tree create if successful, else null
 */
Tree* initTree(int n);
/**
 * @brief frees the memory of the node
 * @param node the node to free
 */
void freeNode(Node *node);
/**
 * @brief frees the memory of the tree and sets the tree pointer to NULL
 * @param tree pointer to pointer to free
 */
void freeTree(Tree **tree);
/**
 * @brief updates an edges in the tree
 * @param tree the tree to update
 * @param i the dad of the j'th in the tree
 * @param j the child of i
 * @return EXIT_FAILURE if there was a problem, else EXIT_SUCCESS
 */
int updateEdge(Tree *tree, int i, int j);
/**
 * @brief updates a node in the tree
 * @param tree tree the tree to update
 * @param line the children of the index
 * @param index the index to update
 * @return EXIT_FAILURE if there was a problem, else EXIT_SUCCESS
 */
int updateNode(Tree *tree, char *line, int index);
/**
 * @brief update the length variable to be the length written in the given line
 * @param line the input line containing the length
 * @param length, a pointer to the variable that will hold the length if the function was successful
 * @return EXIT_FAILURE if there was a problem, else EXIT_SUCCESS
 */
int checkLength(const char *line, int *length);
/**
 * @brief finds the head of the tree and returns it
 * @param tree the tree to search the head in
 * @return NULL if there was a problem, else a pointer to the head of the tree
 */
Node* findHead(Tree *tree);
/**
 * @brief finds the minimum amount of NODES in the sub tree
 * @param tree the tree to search
 * @param node the node to return the minimum height of the tree in (should be head at first)
 * @return the minimum amount of NODES in the sub tree
 */
int minimumHeightTree(Tree *tree, Node *node);
/**
 * @brief finds the maximal amount of NODES in the sub tree, and updates the height of all nodes
 * @param tree the tree to search
 * @param node the node to return the maximal height of the tree in (should be head at first)
 * @return the maximal amount of NODES in the sub tree
 */
int maximumHeightTree(Tree *tree, Node *node);
/**
 * @brief finds the diameter in the sub tree
 * @param tree the tree to search
 * @return the diameter in the sub tree
 */
int diameter(Tree *tree);
/**
 * @brief prints the path from start to end
 * @param node a pointer to the last node to print
 * @param start the start to print from
 * @param end the end to print to
 */
void printPath(Node *node, int start, int end);
/**
 * @brief adds a child \ dad of node with value u to the given queue
 * @param tree the tree to find the children
 * @param queue the queue to update
 * @param u the node to adds its children
 * @param currentValue the value to update with u
 */
void addNodeBfsSearch(const Tree *tree, Queue *queue, unsigned int u, unsigned int currentValue);
/**
 * @brief runs the bfs algorithm
 * @param tree the tree to bfs
 * @param start the start of the bfs
 * @param end the end goal
 * @return EXIT_FAILURE if didn't reach to end, else EXIT_SUCCESS
 */
int bfs(const Tree *tree, int start, int end);
/**
 * @brief initializes the tree to run the bfs algorithm
 * @param tree the tree to initialize
 * @param start the start node of the bfs
 */
void initBfsTree(const Tree *tree, int start);
/**
 * @brief adds all the children of node with value u to the given queue
 * @param tree the tree to find the children
 * @param queue the queue to update
 * @param u the node to adds its children
 */
void addChildrenBfsSearch(const Tree *tree, Queue *queue, unsigned int u);
/**
 * @brief prints the info of the tree if possible
 * @param tree the tree to print the data from
 * @param start the start node of the path
 * @param end the end node of the path
 * @return EXIT_FAILURE without printing if there was a problem, else EXIT_SUCCESS
 */
int printInfoTree(Tree *tree, int start, int end);
/**
 * @brief reads the file and update the tree pointer to point at a tree with the data from the file
 * @param filepath the filepath to read from
 * @param tree the pointer to update
 * @return EXIT_FAILURE if there was a problem (closes the file and FREES the tree), else EXIT_SUCCESS and closes fp
 */
int readFile(const char *filepath, Tree **tree);
/**
 * @brief checks if the tree is a tree
 * @param tree the tree to check
 * @return if the tree is connected and has N - 1 edges then EXIT_SUCCESS, else EXIT_FAILURE
 */
int isTree(Tree **tree);
/**
 * @brief updates the tree with the info in the file and then closes the file
 * @param tree the tree to update
 * @param fp the file to read from
 * @param line the line to store what was read
 * @param length the amount of nodes to expect
 * @return EXIT_FAILURE if there was a problem (closes the file and FREES the tree), else EXIT_SUCCESS and closes fp
 */
int updateTree(Tree **tree, FILE *fp, char *line, int length);

int isInteger(double number)
{
    if(number != (int)number)
    {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}

int minimum(int a, int b)
{
    if(a <= b)
    {
        return a;
    }
    return b;
}

int maximum(int a, int b)
{
    if(a <= b)
    {
        return b;
    }
    return a;
}

void initNode(Node *node, int index)
{
    node->childrenList = allocQueue();
    node->dad = NULL;
    node->value = index;
}

Tree* initTree(int n)
{
    Tree *tree = (Tree *) malloc(sizeof(Tree));
    if(tree == NULL)
    {
        fprintf(stderr, MEMORY_ALLOC_ERROR);
        exit(EXIT_FAILURE);
    }
    tree->nodes = (Node *) malloc((n * sizeof(Node)));
    if(tree->nodes == NULL)
    {
        fprintf(stderr, MEMORY_ALLOC_ERROR);
        free(tree);
        exit(EXIT_FAILURE);
    }
    tree->numberOfNodes = n;
    tree->numberOfEdges = 0;
    for(int i = 0; i < n; i++)
    {
        initNode(&tree->nodes[i], i);
    }
    return tree;
}

void freeNode(Node *node)
{
    freeQueue(&node->childrenList);
}

void freeTree(Tree **tree)
{
    for(int i = 0; i < (*tree)->numberOfNodes; i++)
    {
        freeNode(&(*tree)->nodes[i]);
    }
    free((*tree)->nodes);
    free(*tree);
    *tree = NULL;
}

int updateEdge(Tree *tree, int i, int j)
{
    if((i >= tree->numberOfNodes) || (j >= tree->numberOfNodes) || (i < 0) || (j < 0))
    {
        return EXIT_FAILURE;
    }
    enqueue(tree->nodes[i].childrenList, j);
    if(tree->nodes[j].dad != NULL)
    {
        return EXIT_FAILURE;
    }
    tree->numberOfEdges++;
    tree->nodes[j].dad = &tree->nodes[i];
    return EXIT_SUCCESS;
}


int updateNode(Tree *tree, char *line, int index)
{
    if((strcmp(line, "-\n") == 0) || (strcmp(line, "-") == 0) || (strcmp(line, "-\r\n") == 0))
    {
        return EXIT_SUCCESS;
    }
    char *endPointer = line - 1;
    char *lastPointer;
    double number;
    do
    {
        endPointer = endPointer + 1;
        if(*endPointer == ' ')
        {
            continue;
        }
        lastPointer = endPointer;
        number = strtod(endPointer, &endPointer);
        if(isInteger(number) == EXIT_FAILURE || (endPointer - lastPointer == 0))
        {
            return EXIT_FAILURE;
        }
        if(updateEdge(tree, index, (int)number) == EXIT_FAILURE)
        {
            return EXIT_FAILURE;
        }
    }
    while(*endPointer == ' ');
    if (strcmp(endPointer, "\r\n") == 0 || strcmp(endPointer, "\n") == 0 || strcmp(endPointer, "") == 0)
    {
        return EXIT_SUCCESS;
    }
    return EXIT_FAILURE;
}


int checkLength(const char *line, int *length)
{
    char *endPointer;
    double n = strtod(line, &endPointer);
    *length = (int)n;
    if (isInteger(n) == EXIT_FAILURE || (*length <= 0))
    {
        return EXIT_FAILURE;
    }
    if(*endPointer != '\0' && *endPointer != '\n' && *endPointer != '\r')
    {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}

Node* findHead(Tree *tree)
{
    for(int i = 0; i < tree->numberOfNodes; i++)
    {
        if(tree->nodes[i].dad == NULL)
        {
            return &tree->nodes[i];
        }
    }
    return NULL;
}

int minimumHeightTree(Tree *tree, Node *node)
{
    if(queueIsEmpty(node->childrenList))
    {
        return 0;
    }
    int minimumHeight = tree->numberOfNodes;
    for(QueueNode *temp = node->childrenList->head; temp != node->childrenList->tail->next; temp = temp->next)
    {
        minimumHeight = minimum(minimumHeight, 1 + minimumHeightTree(tree, &tree->nodes[temp->data]));
    }
    return minimumHeight;
}

int maximumHeightTree(Tree *tree, Node *node)
{
    if(queueIsEmpty(node->childrenList))
    {
        return 0;
    }
    int maximumHeight = 0;
    for(QueueNode *temp = node->childrenList->head; temp != node->childrenList->tail->next; temp = temp->next)
    {
        maximumHeight = maximum(maximumHeightTree(tree, &tree->nodes[temp->data]) + 1, maximumHeight);
    }
    return maximumHeight;
}

int diameter(Tree *tree)
{
    int diameter = -1;
    for(int i = 0; i < tree->numberOfNodes; i++)
    {
        bfs(tree, i, tree->numberOfNodes + 1);
        for(int j = 0; j < tree->numberOfNodes; j++)
        {
            diameter = maximum(diameter, tree->nodes[j].dist);
        }
    }
    return diameter;
}


void printPath(Node *node, int start, int end)
{
    printf(SHORTEST_PATH_STRING, start, end);
    Node *nodeHelper = node;
    for(; nodeHelper->prev != NULL; nodeHelper = nodeHelper->prev)
    {
        nodeHelper->prev->next = nodeHelper;
    }
    node->next = NULL;
    for(; nodeHelper != NULL; nodeHelper = nodeHelper->next)
    {
        printf(" %d", nodeHelper->value);
    }
    printf("\n");
}

void addNodeBfsSearch(const Tree *tree, Queue *queue, unsigned int u, unsigned int currentValue)
{
    if (tree->nodes[currentValue].dist == -1)
    {
        enqueue(queue, currentValue);
        tree->nodes[currentValue].dist = tree->nodes[u].dist + 1;
        tree->nodes[currentValue].prev = &tree->nodes[u];
    }
}

int bfs(const Tree *tree, int start, int end)
{
    initBfsTree(tree, start);
    Queue *queue = allocQueue();
    enqueue(queue, start);
    unsigned int u;
    while (!queueIsEmpty(queue) && (int)peekQueue(queue) != end)
    {
        u = dequeue(queue);
        if(!queueIsEmpty(tree->nodes[u].childrenList))
        {
            addChildrenBfsSearch(tree, queue, u);
        }
        if(tree->nodes[u].dad != NULL)
        {
           addNodeBfsSearch(tree, queue, u, tree->nodes[u].dad->value);
        }
    }
    if(queueIsEmpty(queue) || (int)peekQueue(queue) != end)
    {
        freeQueue(&queue);
        return EXIT_FAILURE;
    }
    freeQueue(&queue);
    return EXIT_SUCCESS;
}

void initBfsTree(const Tree *tree, int start)
{
    for(int i = 0; i < tree->numberOfNodes; i++)
    {
        tree->nodes[i].dist = -1;
        tree->nodes[i].prev = NULL;
    }
    tree->nodes[start].dist = 0;
}

void addChildrenBfsSearch(const Tree *tree, Queue *queue, unsigned int u)
{
    for(QueueNode *temp = tree->nodes[u].childrenList->head; temp != tree->nodes[u].childrenList->tail->next;
        temp = temp->next)
    {
        addNodeBfsSearch(tree, queue, u, temp->data);
    }
}

int printInfoTree(Tree *tree, int start, int end)
{
    Node *head;
    if((head = findHead(tree)) == NULL)
    {
        return EXIT_FAILURE;
    }
    if((tree->numberOfNodes <= start) || (tree->numberOfNodes <= end) || (start < 0) || (end < 0)
       || (bfs(tree, start, end) == EXIT_FAILURE))
    {
        return EXIT_FAILURE;
    }
    printf(ROOT_STRING, head->value);
    printf(VERTICES_STRING, tree->numberOfNodes);
    printf(EDGES_STRING, tree->numberOfEdges);
    printf(MIN_BRANCH_STRING, minimumHeightTree(tree, head));
    printf(MAX_BRANCH_STRING, maximumHeightTree(tree, head));
    printf(DIAMETER_STRING, diameter(tree));
    bfs(tree, start, end);
    printPath(&tree->nodes[end], start, end);
    return EXIT_SUCCESS;
}

int readFile(const char *filepath, Tree **tree)
{
    FILE *fp = fopen(filepath, "r");
    if(fp == NULL)
    {
        return EXIT_FAILURE;
    }
    char line[MAX_LINE_LIMIT];
    int length;
    if(fgets(line, MAX_LINE_LIMIT, fp) == NULL || checkLength(line, &length) == EXIT_FAILURE)
    {
        fclose(fp);
        return EXIT_FAILURE;
    }
    if((*tree = initTree(length)) == NULL)
    {
        return EXIT_FAILURE;
    }
    return updateTree(tree, fp, line, length);
}

int isTree(Tree **tree)
{
    bfs(*tree, 0, (*tree)->numberOfNodes);
    //check you got to every node, i.e. connected
    for(int i = 0; i < (*tree)->numberOfNodes; i++)
    {
        if((*tree)->nodes[i].dist == -1)
        {
            return EXIT_FAILURE;
        }
    }
    // too much nodes, else it is a tree
    if((*tree)->numberOfEdges != (*tree)->numberOfNodes - 1)
    {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}

int updateTree(Tree **tree, FILE *fp, char *line, int length)
{
    int i = 0;
    for (; fgets(line, MAX_LINE_LIMIT, fp) != NULL; i++)
    {
        if(length <= i || updateNode(*tree, line, i) == EXIT_FAILURE)
        {
            fclose(fp);
            freeTree(tree);
            return EXIT_FAILURE;
        }
    }
    fclose(fp);
    if((i < length) || (isTree(tree) == EXIT_FAILURE))
    {
        freeTree(tree);
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}

int main(int argc, char *argv[])
{
    if(argc != 4)
    {
        fprintf(stderr, USAGE_INPUT_ERROR);
        return EXIT_FAILURE;
    }
    Tree *tree;
    char *p1, *p2;
    double input2 = strtod(argv[2], &p1);
    double input3 = strtod(argv[3], &p2);
    if((p1 == argv[2]) || (*p1 != '\0') || (p2 == argv[3]) || (*p2 != '\0') || (isInteger(input2) == EXIT_FAILURE)
       || (isInteger(input3) == EXIT_FAILURE))
    {
        fprintf(stderr, INVALID_INPUT_ERROR);
        return EXIT_FAILURE;
    }
    if(readFile(argv[1], &tree) == EXIT_FAILURE)
    {
        fprintf(stderr, INVALID_INPUT_ERROR);
        return EXIT_FAILURE;
    }
    if(printInfoTree(tree, (int)input2, (int)input3) == EXIT_FAILURE)
    {
        fprintf(stderr, INVALID_INPUT_ERROR);
        freeTree(&tree);
        return EXIT_FAILURE;
    }
    freeTree(&tree);
    return EXIT_SUCCESS;
}