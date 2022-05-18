//
// Created by Mike on 3/12/2020.
//
#define SUCCESS 0
#define FAILURE -1
#define MICRO_TO_NANO 1000
#define SEC_TO_NANO 1000000000L
#define LOOP_UNROLLING 20

#include "osm.h"
#include <sys/time.h>
#include <iostream>

/*
 *  returns the amount of nano time the operations took between t1 and t2
 */
static unsigned long differenceNanoSecTimes(struct timeval* t1, struct timeval* t2)
{
    return (t2->tv_sec - t1->tv_sec) * SEC_TO_NANO + (t2->tv_usec - t1->tv_usec) * MICRO_TO_NANO;
}

/*
*   returns the average amount of nano time an operation
*/
static double differenceNanoSecTimesAverage(struct timeval* t1, struct timeval *t2, unsigned int iterations)
{
    double iter = iterations;
    return differenceNanoSecTimes(t1, t2) / iter;
}

/* Time measurement function for a simple arithmetic operation.
   returns time in nano-seconds upon success,
   and -1 upon failure.
   */
double osm_operation_time(unsigned int iterations)
{
    if(iterations == 0)
    {
        return FAILURE;
    }

    struct timeval startTime, endTime;
    unsigned int i = 0;
    if(gettimeofday(&startTime, nullptr) == FAILURE)
    {
        return FAILURE;
    }
    for(; i < iterations; i += LOOP_UNROLLING)
    {
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
        asm("add $4, %dx");
    }
    if(gettimeofday(&endTime, nullptr) == FAILURE)
    {
        return FAILURE;
    }
    return differenceNanoSecTimesAverage(&startTime, &endTime, i);
}

static void emptyFunc(){}

/* Time measurement function for an empty function call.
   returns time in nano-seconds upon success,
   and -1 upon failure.
   */
double osm_function_time(unsigned int iterations)
{
    if(iterations == 0)
    {
        return FAILURE;
    }
    struct timeval startTime, endTime;
    unsigned int i = 0;
    if(gettimeofday(&startTime, nullptr) == FAILURE)
    {
        return FAILURE;
    }
    for(; i < iterations; i += LOOP_UNROLLING)
    {
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
        emptyFunc();
    }
    if(gettimeofday(&endTime, nullptr) == FAILURE)
    {
        return FAILURE;
    }
    return differenceNanoSecTimesAverage(&startTime, &endTime, i);
}


/* Time measurement function for an empty trap into the operating system.
   returns time in nano-seconds upon success,
   and -1 upon failure.
   */
double osm_syscall_time(unsigned int iterations)
{
    if(iterations == 0)
    {
        return FAILURE;
    }
    struct timeval startTime, endTime;
    unsigned int i = 0;
    if(gettimeofday(&startTime, nullptr) == FAILURE)
    {
        return FAILURE;
    }
    for(; i < iterations; i += LOOP_UNROLLING)
    {
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
        OSM_NULLSYSCALL;
    }
    if(gettimeofday(&endTime, nullptr) == FAILURE)
    {
        return FAILURE;
    }
    return differenceNanoSecTimesAverage(&startTime, &endTime, i);
}

//int main()
//{
//    long iterations = 200000;
//    std::cout << "Operation call: " << osm_operation_time(iterations) << std::endl;
//    std::cout << "Function call: " << osm_function_time(iterations) << std::endl;
//    std::cout << "System call: " << osm_syscall_time(iterations) << std::endl;
//}