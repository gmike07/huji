//
// Created by Mike on 3/16/2020.
//

#ifndef EX2_SCHEDULAR_H
#define EX2_SCHEDULAR_H
#include <map>
#include <iostream>
#include "Thread.h"
#include <signal.h>
#include <deque>
#include <vector>
#include <sys/time.h>
#include "uthreads.h"
#include "Helper.h"


class Scheduler
{
private:
    int _quantum_counter;
    Thread* _running_thread;
    std::map<int, Thread*> _threads;
    std::deque<Thread*> _ready_list;
    std::vector<Thread*> _terminated_resources;
    int* _quantums;
    int _size;
    struct itimerval _vt_timer{};

public:

    /**
     * constructor
     */
    Scheduler(int* _quantums, int _size);

    /**
     * increment number of quantoms by 1
     */
    void advance_quantum();

    /**
     * get the number of quantoms
     * @return number of quantoms since start on success and -1 on failure
     */
    int get_quantums() const;

    /**
     * [delete_from_ready_list description]
     * @param id [description]
     */
    void delete_from_ready_list(int id);

    /**
     * get the ID of the currently running thread
     * @return id of thread on success, and -1 on failure
     */
    int get_running_thread_id() const;

    /**
     * get the number of quantoms that the thread was active
     * @param  tid - id of the thread
     * @return     number of quantoms on success and -1 on failure
     */
    int get_quantums(int tid) const;

    /**
     * get an id of a thread, and resume it
     * @param  tid - id of the thread
     * @return     SUCCESS on success and FAILURE on faliure
     */
    int resume_thread(int tid);

    /**
     * terminate all threads
     */
    void terminate_threads();

    /**
     * add a new ready threads to the threads
     * @param  void function to run on the thread
     * @return      SUCESS on success and FAILURE on failure
     */
    int add_thread(int priority, void (*f)(void));

    /**
     * [choose_new_run_thread description]
     */
    void choose_new_run_thread();

    /**
     * [block_thread description]
     * @param  id [description]
     * @return    [description]
     */
    int block_thread(int id);

    /**
     * [terminate_thread description]
     * @param  id [description]
     * @return    [description]
     */
    int terminate_thread(int id);


    /**
     *  changes the priority of the thread
     * @param tid - index of the thread
     * @param priority - priority of thread
     * @return
     */
    int change_priority(int tid, int priority);

    void delete_terminated_resources();


    void run_new_thread();

};

#endif //EX2_SCHEDULAR_H
