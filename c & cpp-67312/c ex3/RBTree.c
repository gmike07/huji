#include <stdio.h>
#include <stdlib.h>
#include "RBTree.h"
#define ERROR 0
#define SUCCESS 1

/**
 * @param node the current node to free
 * @param freeFunc the free function in the tree
 * frees all data from the tree
 */
static void freeNodes(Node *node, FreeFunc freeFunc);
/**
 * @param node the current node to check
 * @param compareFunc the compare func in the tree
 * @param data the data to check if exists in the tree
 * @return SUCCESS if the data was found, else ERROR
 */
static int containsRBNodes(Node *node, CompareFunc compareFunc, void *data);
/**
 * @param parent the parent of the new node
 * @param child the child of the new node
 * @param compareFunc the compare func in the tree
 * update the pointer of the parent to point at the child
 */
static void updateParent(Node *parent, Node *child, CompareFunc compareFunc);
/**
 * @param parent the parent of the new node
 * @param data the data of the new node
 * @param color the color of the new node
 * @param compareFunc the function to know if it left or right of the parent
 * @return the new node if it was created, else NULL
 */
static Node* initNode(Node *parent, void *data, Color color, CompareFunc compareFunc);
/**
 * @param tree the tree to add the node to
 * @param child the new added node
 * @param parent the parent of the node
 * rotates the connection between the child and the parent
 */
static void rotate(RBTree *tree, Node *child, Node *parent);
/**
 * @param tree the tree to add the node to
 * @param child the new added node
 * @param parent the parent of the node
 * @param grandParent the grand parent of the node
 * updates the pointers of the grand parent correctly
 */
static void updateGrandParentRotation(RBTree *tree, Node *child, const Node *parent, Node *grandParent);
/**
 * @param tree the tree to add the node to
 * @param node the new added node
 * @param parent the parent of the node
 * @param grandParent the grand parent of the node
 * fixes the connections between them so the tree will still be a black red tree (rotations)
 */
static void handleRotation(RBTree *tree, Node *node, Node *parent, Node *grandParent);
/**
 * @param tree the tree to add the node to
 * @param node the new added node
 * @return SUCCESS if there were no errors fixing the tree to be a black red tree, else ERROR
 */
static int fixNode(RBTree *tree, Node *node);
/**
 * @param tree the tree to add the node to
 * @param parent the parent of the child to add
 * @param current the current node to search where to add the child
 * @param data the data of the child to add
 * @return SUCCESS if there were no errors adding the node, else ERROR
 */
static int addToRBNode(RBTree *tree, Node *parent, Node* current, void *data);
/**
 * @param tree the tree to add the node to
 * @param parent the parent of the child to add
 * @param data the data of the child to add
 * @return SUCCESS if there were no errors adding the node, else ERROR
 */
static int addNodeToTree(RBTree *tree, Node *parent, void *data);
/**
 * @param node the current node to apply the func to
 * @param func the func to apply
 * @param args the args of the func
 * @return SUCCESS if there were no errors, else ERROR
 */
static int forEachRBNode(Node *node, forEachFunc func, void *args);


RBTree *newRBTree(CompareFunc compFunc, FreeFunc freeFunc)
{
    if(compFunc == NULL || freeFunc == NULL)
    {
        return NULL;
    }
    RBTree *tree = (RBTree*) malloc(sizeof(RBTree));
    if(tree == NULL)
    {
        return NULL;
    }
    tree->compFunc = compFunc;
    tree->root = NULL;
    tree->freeFunc = freeFunc;
    tree->size = 0;
    return tree;
}

static void freeNodes(Node *node, FreeFunc freeFunc)
{
    if(node == NULL)
    {
        return;
    }
    freeNodes(node->left, freeFunc);
    freeNodes(node->right, freeFunc);
    if(node->data != NULL)
    {
        freeFunc(node->data);
    }
    free(node);
}

void freeRBTree(RBTree *tree)
{
    if(tree == NULL)
    {
        return;
    }
    freeNodes(tree->root, tree->freeFunc);
    free(tree);
}

static int containsRBNodes(Node *node, CompareFunc compareFunc, void *data)
{
    if(node == NULL || node->data == NULL)
    {
        return ERROR;
    }
    if(compareFunc(data, node->data) == 0)
    {
        return SUCCESS;
    }
    if(compareFunc(data, node->data) > 0)
    {
        return containsRBNodes(node->right, compareFunc, data);
    }
    return containsRBNodes(node->left, compareFunc, data);
}


int containsRBTree(RBTree *tree, void *data)
{
    if(tree == NULL || data == NULL)
    {
        return ERROR;
    }
    return containsRBNodes(tree->root, tree->compFunc, data);
}

static void updateParent(Node *parent, Node *child, CompareFunc compareFunc)
{
    if(compareFunc(child->data, parent->data) > 0)
    {
        parent->right = child;
        return;
    }
    parent->left = child;
}

static Node* initNode(Node *parent, void *data, Color color, CompareFunc compareFunc)
{
    Node *node = (Node*) malloc(sizeof(Node));
    if(node == NULL)
    {
        return NULL;
    }
    node->parent = parent;
    node->data = data;
    node->left = NULL;
    node->right = NULL;
    node->color = color;
    if(parent != NULL)
    {
        updateParent(parent, node, compareFunc);
    }
    return node;
}


static void rotate(RBTree *tree, Node *child, Node *parent)
{
    Node *grandChild = NULL, *grandParent = NULL;
    if(parent->left == child)
    {
        grandChild = child->right;
        child->right = parent;
        parent->left = grandChild;
    }
    else
    {
        grandChild = child->left;
        child->left = parent;
        parent->right = grandChild;
    }
    if(grandChild != NULL)
    {
        grandChild->parent = parent;
    }
    grandParent = parent->parent;
    parent->parent = child;
    child->parent = grandParent;
    updateGrandParentRotation(tree, child, parent, grandParent);
}

static void updateGrandParentRotation(RBTree *tree, Node *child, const Node *parent, Node *grandParent)
{
    if(grandParent == NULL)
    {
        tree->root = child;
        return;
    }
    if(grandParent->right == parent)
    {
        grandParent->right = child;
        return;
    }
    grandParent->left = child;
}

static void handleRotation(RBTree *tree, Node *node, Node *parent, Node *grandParent)
{
    if((grandParent->right != NULL && grandParent->right->left == node)
       || (grandParent->left != NULL && grandParent->left->right == node))
    {
        rotate(tree, node, parent);
        parent = node;
    }
    rotate(tree, parent, grandParent);
    //one is red and one is black, we can replace the colors before rotation
    grandParent->color = RED;
    parent->color = BLACK;
}

static int fixNode(RBTree *tree, Node *node)
{
    if(node->parent == NULL) //this is the root
    {
        node->color = BLACK;
        return SUCCESS;
    }
    if(node->parent->color == BLACK) //the sub tree is OK :)
    {
        return SUCCESS;
    }
    Node *grandParent = node->parent->parent;
    if(grandParent == NULL) //not a correct black red tree
    {
        return ERROR;
    }
    if(grandParent->left != NULL && grandParent->right != NULL && grandParent->left->color == RED
       && grandParent->right->color == RED) //both the parent and it's cousin are red :)
    {
        grandParent->left->color = BLACK;
        grandParent->right->color = BLACK;
        grandParent->color = RED;
        return fixNode(tree, grandParent);
    }
    handleRotation(tree, node, node->parent, grandParent);
    return SUCCESS;
}


static int addToRBNode(RBTree *tree, Node *parent, Node* current, void *data)
{
    if(tree == NULL)
    {
        return ERROR;
    }
    if(current == NULL)
    {
        return addNodeToTree(tree, parent, data);
    }
    if(current->data == NULL || tree->compFunc(data, current->data) == 0)
    {
        return ERROR;
    }
    if(tree->compFunc(data, current->data) > 0)
    {
        return addToRBNode(tree, current, current->right, data);
    }
    return addToRBNode(tree, current, current->left, data);
}

static int addNodeToTree(RBTree *tree, Node *parent, void *data)
{
    Node *node = initNode(parent, data, RED, tree->compFunc);
    if(node == NULL)
    {
        return ERROR;
    }
    if(fixNode(tree, node) == ERROR)
    {
        tree->freeFunc(node->data);
        if(node->parent->left == node)
        {
            node->parent->left = NULL;
        }
        else
        {
            node->parent->right = NULL;
        }
        free(node);
        return ERROR;
    }
    tree->size++;
    return SUCCESS;
}


int addToRBTree(RBTree *tree, void *data)
{
    if(tree == NULL || data == NULL || tree->compFunc == NULL)
    {
        return ERROR;
    }
    if(tree->root == NULL)
    {
        tree->root = initNode(NULL, data, BLACK, tree->compFunc);
        if(tree->root == NULL)
        {
            return ERROR;
        }
        tree->size = 1;
        return SUCCESS;
    }
    return addToRBNode(tree, tree->root->parent, tree->root, data);
}

static int forEachRBNode(Node *node, forEachFunc func, void *args)
{
    if(node == NULL)
    {
        return SUCCESS;
    }
    if(forEachRBNode(node->left, func, args) == ERROR)
    {
        return ERROR;
    }
    if(func(node->data, args) == 0)
    {
        return ERROR;
    }
    return forEachRBNode(node->right, func, args);
}


int forEachRBTree(RBTree *tree, forEachFunc func, void *args)
{
    if(tree == NULL || func == NULL)
    {
        return ERROR;
    }
    return forEachRBNode(tree->root, func, args);
}
