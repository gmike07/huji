CFLAGS = -Wvla -Wall -Wextra -g -std=c99
CC = gcc
AR = ar
CLEANFILES = ProductExample.o Structs.o RBTree.o

presubmit: ProductExample.o RBTree.a Structs.o
	$(CC) -o presubmit ProductExample.o RBTree.a
	./presubmit
	
ProductExample.o: ProductExample.c 
	$(CC) -c $(CFLAGS) ProductExample.c

RBTree.a: RBTree.o
	$(AR) rcs RBTree.a RBTree.o

RBTree.o: RBTree.c
	$(CC) -c $(CFLAGS) RBTree.c

Structs.o: Structs.c
	$(CC) -c $(CFLAGS) Structs.c

school_presubmit: ProductExample.o RBTreeSchool.a
	$(CC) -o school_presubmit ProductExample.o RBTreeSchool.a
	./school_presubmit

RBTreeSchool.a:
	echo "please copy RBTreeSchool.a from ~/labcc/www/c_ex3/school_solution to this folder."

school_tests: test_cases.o RBTreeSchool.a
	$(CC) -o school_tests test_cases.o RBTreeSchool.a
	./school_tests

test_cases.o: test_cases.c
	$(CC) -c $(CFLAGS) test_cases.c

clean:
	rm -f $(CLEANFILES)

tar:
	tar cvf c_ex3 RBTree.c Structs.c