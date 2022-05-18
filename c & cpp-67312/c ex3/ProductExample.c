//
// Created by odedw on 12-Oct-19.
//

#ifndef TA_EX3_PRODUCTEXAMPLE_C
#define TA_EX3_PRODUCTEXAMPLE_C

#include "RBTree.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define LESS (-1)
#define EQUAL (0)
#define GREATER (1)

typedef struct ProductExample
{
	char *name;
	double price;
} ProductExample;

/**
 * Comparator for ProductExample
 * @param a ProductExample*
 * @param b ProductExample*
 * @return -1 if a<b, 0 if a==b, 1 if b<a
 */
int productComparatorByName(const void *a, const void *b)
{
	ProductExample *first = (ProductExample *) a;
	ProductExample *second = (ProductExample *) b;
	double diff = strcmp(first->name, second->name);
	if (diff < 0)
	{
		return LESS;
	}
	else if (diff > 0)
	{
		return GREATER;
	}
	else
	{
		return EQUAL;
	}
}

void productFree(void *a)
{
	ProductExample *pProduct = (ProductExample *) a;
	free(pProduct->name);
	free(a);
}

/**
 *
 * @param pProduct pointer to product to print
 * @param null required argument for typedef
 * @return
 */
int printProduct(const void *pProduct, void *null)
{
	if (null != NULL)
	{
		return 0;
	}
	ProductExample *product = (ProductExample *) pProduct;
	printf("Name: %s.\t\tPrice: %.2f\n", product->name, product->price);

	return 1;
}

/**
 *
 * @return products for tests
 */
ProductExample **getProducts()
{
	char *name0 = (char *) malloc(sizeof(char) * (20));
	char *name1 = (char *) malloc(sizeof(char) * (20));
	char *name2 = (char *) malloc(sizeof(char) * (20));
	char *name3 = (char *) malloc(sizeof(char) * (20));
	char *name4 = (char *) malloc(sizeof(char) * (20));
	char *name5 = (char *) malloc(sizeof(char) * (20));

	strcpy(name0, "MacBook Pro");
	strcpy(name1, "iPod");
	strcpy(name2, "iPhone");
	strcpy(name3, "iPad");
	strcpy(name4, "Apple Watch");
	strcpy(name5, "Apple TV");

	ProductExample **products = (ProductExample **) malloc(sizeof(ProductExample *) * 6);

	products[0] = (ProductExample *) malloc(sizeof(ProductExample));
	products[1] = (ProductExample *) malloc(sizeof(ProductExample));
	products[2] = (ProductExample *) malloc(sizeof(ProductExample));
	products[3] = (ProductExample *) malloc(sizeof(ProductExample));
	products[4] = (ProductExample *) malloc(sizeof(ProductExample));
	products[5] = (ProductExample *) malloc(sizeof(ProductExample));

	products[0]->name = name0;
	products[0]->price = 1499;
	products[1]->name = name1;
	products[1]->price = 199;
	products[2]->name = name2;
	products[2]->price = 599;
	products[3]->name = name3;
	products[3]->price = 499;
	products[4]->name = name4;
	products[4]->price = 299;
	products[5]->name = name5;
	products[5]->price = 199;

	return products;

}

void freeResources(RBTree *tree, ProductExample ***products)
{
	freeRBTree(tree);
	productFree((*products)[1]);
	productFree((*products)[5]);
	free(*products);
}

void assertion(int passed, int assertion_num, char *msg)
{
	if (!passed)
	{
		printf("assertion %d failed: %s\n", assertion_num, msg);
	}

}

int main()
{
	ProductExample **products = getProducts();
	RBTree *tree = newRBTree(productComparatorByName, productFree);
	addToRBTree(tree, products[2]);
	addToRBTree(tree, products[3]);
	addToRBTree(tree, products[4]);
	addToRBTree(tree, products[0]);
	int i = 0;
	for (i = 0; i < 6; i++)
	{
		if (containsRBTree(tree, products[i]))
		{
			printf("\"%s\" is in the tree.\n", products[i]->name);
			if (i == 1 || i == 5)
			{
				printf(" This product should not be in the tree!\nTest failed, aborting");
				freeResources(tree, &products);
				return 1;
			}
		}
		else
		{
			printf("\"%s\" is not in the tree.\n", products[i]->name);
			if (i != 1 && i != 5)
			{
				printf(" This product should be in the tree!\nTest failed, aborting");
				freeResources(tree, &products);
				return 2;
			}
		}
	}

	printf("\nThe number of products in the tree is %d.\n\n", tree->size);
	forEachRBTree(tree, printProduct, NULL);
	freeResources(tree, &products);
	printf("test passed\n");
	return 0;
}


#endif //TA_EX3_PRODUCTEXAMPLE_C
