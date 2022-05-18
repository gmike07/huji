//
// Created by Mike on 3/16/2020.
//
#include "Thread.h"
#include <string>
#ifdef __x86_64__
/* code for 64 bit Intel arch */

typedef unsigned long address_t;
#define JB_SP 6
#define JB_PC 7

/* A translation is required when using an address of a variable.
   Use this as a black box in your code. */
address_t translate_address(address_t addr)
{
    address_t ret;
    asm volatile("xor    %%fs:0x30,%0\n"
		"rol    $0x11,%0\n"
                 : "=g" (ret)
                 : "0" (addr));
    return ret;
}

#else
/* code for 32 bit Intel arch */

typedef unsigned int address_t;
#define JB_SP 4
#define JB_PC 5

/* A translation is required when using an address of a variable.
   Use this as a black box in your code. */
address_t translate_address(address_t addr)
{
    address_t ret;
    asm volatile("xor    %%gs:0x18,%0\n"
		"rol    $0x9,%0\n"
                 : "=g" (ret)
                 : "0" (addr));
    return ret;
}
#endif

/**
 * this function advances the quantum count of this thread
*/
void Thread::advance_quantum()
{
    this->_quantum_count++;
}

/**
 * constructor
*/
Thread::Thread(int id, int priority, void (*f)(void)): _id(id), _state(ThreadStates::READY) ,
_quantum_count(0), _priority(priority)
{
    // sp = stack pointer, pc = program counter
    address_t sp, pc;

    //store the sp address of this thread
    sp = (address_t) this->_stack + STACK_SIZE - sizeof(address_t); //save stack

    //store the pc of this thread
    pc = (address_t)(f);

    //set the buffer to the thread one
    sigsetjmp(this->_env, 1);
    (_env->__jmpbuf)[JB_SP] = translate_address(sp);
    (_env->__jmpbuf)[JB_PC] = translate_address(pc);

    //reset mask set of buffer
    sigemptyset(&_env->__saved_mask);
}

/**
 * constructor for main
*/
Thread::Thread(): _id(0), _state(ThreadStates::RUNNING) ,_quantum_count(1), _priority(0)
{
}


/**
 * this function returns the quantum time of this thread
*/
int Thread::get_quantums() const
{
    return this->_quantum_count;
}


/**
 * this function returns the state
*/
ThreadStates Thread::get_state() const
{
    return this->_state;
}


int Thread::get_id() const
{
    return this->_id;
}


/**
 * this function moves from READY state to RUNNING state
*/
int Thread::run()
{
    if(this->_state != ThreadStates::READY)
    {
        return FAILURE;
    }
    this->_state = ThreadStates::RUNNING;
    this->advance_quantum();
    siglongjmp(this->_env, 1);
    return SUCCESS;
}


/**
 * this function move from BLOCKED state to READY state
 * Scheduler has to check that the state is not running or ready,
 * else not to append it to the ready list
*/
int Thread::resume()
{
    if(this->_state != ThreadStates::BLOCKED)
    {
        return FAILURE;
    }
    this->_state = ThreadStates::READY;
    return SUCCESS;
}


/**
 * this function move from RUNNING state to BLOCK state via blocked flag
*/
int Thread::block()
{
    if(this->_state != ThreadStates::RUNNING)
    {
        this->_state = ThreadStates::BLOCKED;
        return FAILURE;
    }
    this->_state = ThreadStates::BLOCKED;
    return sigsetjmp(this->_env, 1);
}


/**
 * this function moves from RUNNING state to READY state
*/
int Thread::preempt()
{
    if(this->_state != ThreadStates::RUNNING)
    {
        return FAILURE;
    }
    this->_state = ThreadStates::READY;
    //store the current thread before going to ready
    return sigsetjmp(this->_env, 1);
}


int Thread::get_priority() const
{
    return this->_priority;
}


void Thread::set_priority(int priority)
{
    this->_priority = priority;
}
