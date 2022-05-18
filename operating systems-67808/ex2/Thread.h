//
// Created by Mike on 3/16/2020.
//

#ifndef EX2_THREAD_H
#define EX2_THREAD_H
#include "uthreads.h"
#include <csetjmp>
#include <csignal>
#define FAILURE -1
#define SUCCESS 0


enum ThreadStates
{
    READY,
    RUNNING,
    BLOCKED
};

class Thread
{
private:
    //the id of this thread
    int _id;

    //the current state of this thread
    ThreadStates _state;

    //the amount of virtual time the thread ran on the cpu
    int _quantum_count;


    //the stack of this thread
    char _stack[STACK_SIZE];

    //the buffer of this
    sigjmp_buf _env;

    //priority
    int _priority;

public:

    /**
     * constructor for main
     * after construction of main, call advance_quantum
    */
    Thread();

    /**
    * constructor for thread
    */
    Thread(int id, int priority, void (*f)(void));


    /**
     * this function advances the quantum count of this thread
    */
    void advance_quantum();

    /**
     * this function moves from READY state to RUNNING state
    */
    int run();

    /**
     * this function move from BLOCKED state to READY state
    */
    int resume();

    /**
     * this function move from RUNNING state to BLOCK state
    */
    int block();

    /**
     * this function moves from RUNNING state to READY state
    */
    int preempt();

    /**
     * this function returns the state
    */
    ThreadStates get_state() const;

    /**
     * this function returns the quantum time of this thread
    */
    int get_quantums() const;

    /**
    * this function returns the id
    */
    int get_id() const;

    /**
    * this function returns the priority
    */
    int get_priority() const;

    void set_priority(int priority);
};



#endif //EX2_THREAD_H
