//
// Created by Mike on 3/16/2020.
//
#include "Thread.h"
#include "Helper.h"
#include "Scheduler.h"
#include <cstring>

static Scheduler* scheduler;
static struct sigaction _vt_handler;
static sigset_t _set_mask;


static void advance_quantum_helper(int)
{
    scheduler->advance_quantum();
}

static void mask_signals()
{
    if(sigprocmask(SIG_BLOCK, &_set_mask, nullptr) == FAILURE)
    {
        Helper::system_err_printer("sig proc mask failed");
    }
}

static void unmask_signals()
{
    if(sigprocmask(SIG_UNBLOCK, &_set_mask, nullptr) == FAILURE)
    {
        Helper::system_err_printer("sig proc mask failed");
    }
}

/*
 * Description: This function initializes the thread library.
 * You may assume that this function is called before any other thread library
 * function, and that it is called exactly once. The input to the function is
 * an array of the length of a quantum in micro-seconds for each priority.
 * It is an error to call this function with an array containing non-positive integer.
 * size - is the size of the array.
 * Return value: On success, return 0. On failure, return -1.
*/
int uthread_init(int *quantum_usecs, int size)
{
    if(size <= 0)
    {
        return Helper::library_err_printer("invalid size");
    }
    if(quantum_usecs == nullptr)
    {
        return Helper::library_err_printer("invalid quantum array");
    }

    for(int i = 0; i < size; i++)
    {
        if(quantum_usecs[i] <= 0)
        {
            return Helper::library_err_printer("invalid quantum in array");
        }
    }

    // initialize quantum advancing signal
    _vt_handler.sa_handler = &advance_quantum_helper;

    // if sigaction failed
    if (sigaction(SIGVTALRM, &_vt_handler, nullptr) < 0)
    {
        Helper::system_err_printer("sigaction failure");
    }

    // initialize the set of signals to get masked
    sigemptyset(&_set_mask);
    sigaddset(&_set_mask, SIGVTALRM);

    try
    {

        // copy the quantum usecs array
        int* quantum_usecs_copy;

        // allocate new quantum array
        quantum_usecs_copy = new int[size];

        // copy the quantum array
        std::memcpy(quantum_usecs_copy, quantum_usecs, sizeof(int) * size);

        // allocate new scheduler
        scheduler = new Scheduler(quantum_usecs_copy, size);
    }

    catch(std::exception& e)
    {
        Helper::system_err_printer("bad allocation");
    }

    return SUCCESS;
}

/*
 * Description: This function creates a new thread, whose entry point is the
 * function f with the signature void f(void). The thread is added to the end
 * of the READY threads list. The uthread_spawn function should fail if it
 * would cause the number of concurrent threads to exceed the limit
 * (MAX_THREAD_NUM). Each thread should be allocated with a stack of size
 * STACK_SIZE bytes.
 * priority - The priority of the new thread.
 * Return value: On success, return the ID of the created thread.
 * On failure, return -1.
*/
int uthread_spawn(void (*f)(void), int priority)
{
    mask_signals();
    int output = scheduler->add_thread(priority, f);
    unmask_signals();
    return output;
}


/*
 * Description: This function changes the priority of the thread with ID tid.
 * If this is the current running thread, the effect should take place only the
 * next time the thread gets scheduled.
 * Return value: On success, return 0. On failure, return -1.
*/
int uthread_change_priority(int tid, int priority)
{
    mask_signals();
    int output = scheduler->change_priority(tid, priority);
    unmask_signals();
    return output;
}

/*
 * Description: This function terminates the thread with ID tid and deletes
 * it from all relevant control structures. All the resources allocated by
 * the library for this thread should be released. If no thread with ID tid
 * exists it is considered an error. Terminating the main thread
 * (tid == 0) will result in the termination of the entire process using
 * exit(0) [after releasing the assigned library memory].
 * Return value: The function returns 0 if the thread was successfully
 * terminated and -1 otherwise. If a thread terminates itself or the main
 * thread is terminated, the function does not return.
*/
int uthread_terminate(int tid)
{
    mask_signals();
    int output = scheduler->terminate_thread(tid);
    if(tid == 0)
    {
        delete scheduler;
        exit(0);
    }
    unmask_signals();
    return output;
}


/*
 * Description: This function blocks the thread with ID tid. The thread may
 * be resumed later using uthread_resume. If no thread with ID tid exists it
 * is considered as an error. In addition, it is an error to try blocking the
 * main thread (tid == 0). If a thread blocks itself, a scheduling decision
 * should be made. Blocking a thread in BLOCKED state has no
 * effect and is not considered an error.
 * Return value: On success, return 0. On failure, return -1.
*/
int uthread_block(int tid)
{
    mask_signals();
    int output = scheduler->block_thread(tid);
    unmask_signals();
    return output;
}


/*
 * Description: This function resumes a blocked thread with ID tid and moves
 * it to the READY state if it's not synced. Resuming a thread in a RUNNING or READY state
 * has no effect and is not considered as an error. If no thread with
 * ID tid exists it is considered an error.
 * Return value: On success, return 0. On failure, return -1.
*/
int uthread_resume(int tid)
{
    mask_signals();
    int output = scheduler->resume_thread(tid);
    unmask_signals();
    return output;
}


/*
 * Description: This function returns the thread ID of the calling thread.
 * Return value: The ID of the calling thread.
*/
int uthread_get_tid()
{
    mask_signals();
    int output = scheduler->get_running_thread_id();
    unmask_signals();
    return output;
}


/*
 * Description: This function returns the total number of quantums since
 * the library was initialized, including the current quantum.
 * Right after the call to uthread_init, the value should be 1.
 * Each time a new quantum starts, regardless of the reason, this number
 * should be increased by 1.
 * Return value: The total number of quantums.
*/
int uthread_get_total_quantums()
{
    mask_signals();
    int output = scheduler->get_quantums();
    unmask_signals();
    return output;
}


/*
 * Description: This function returns the number of quantums the thread with
 * ID tid was in RUNNING state. On the first time a thread runs, the function
 * should return 1. Every additional quantum that the thread starts should
 * increase this value by 1 (so if the thread with ID tid is in RUNNING state
 * when this function is called, include also the current quantum). If no
 * thread with ID tid exists it is considered an error.
 * Return value: On success, return the number of quantums of the thread with ID tid.
 * 			     On failure, return -1.
*/
int uthread_get_quantums(int tid)
{
    mask_signals();
    int output = scheduler->get_quantums(tid);
    unmask_signals();
    return output;
}