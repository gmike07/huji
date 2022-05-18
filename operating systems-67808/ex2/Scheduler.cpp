
// Created by Mike on 3/16/2020.
//


#include "Scheduler.h"
#include "Helper.h"
#include <string>
#include <algorithm>

void Scheduler::advance_quantum()
{

    // check if we got here through siglongjmp
    if(this->_running_thread->preempt() != SUCCESS)
    {
        return;
    }
    this->_ready_list.push_back(this->_running_thread);

    this->run_new_thread();
}


void Scheduler::run_new_thread()
{
    // add 1 to the quantoms counter
    this->_quantum_counter++;
    this->_running_thread = nullptr;
    this->choose_new_run_thread();
    Helper::start_new_quantum(this->_vt_timer, this->_quantums[this->_running_thread->get_priority()]);
    this->_running_thread->run();
}

void Scheduler::delete_from_ready_list(int id)
{
    auto it = std::find(this->_ready_list.begin(), this->_ready_list.end(), this->_threads[id]);
    if(this->_ready_list.end() != it)
    {
        this->_ready_list.erase(it);
    }
}

int Scheduler::get_quantums() const
{
    return this->_quantum_counter;
}


int Scheduler::get_quantums(int id) const
{
    // check if the id exists
    if(Helper::check_id_exists(this->_threads, id) == FAILURE)
    {
        return FAILURE;
    }
    return this->_threads.at(id)->get_quantums();
}

int Scheduler::get_running_thread_id() const
{
    return this->_running_thread->get_id();
}

void Scheduler::terminate_threads()
{
    // loop on all threads and terminate threads
    delete_terminated_resources();
    for(auto& it: this->_threads)
    {
        delete it.second;
    }

    delete[] this->_quantums;
}

int Scheduler::add_thread(int priority, void (*f)(void))
{
    if(f == nullptr)
    {
        return Helper::library_err_printer("the spawn got nullptr instead of f");
    }
    // find the first free id to insert the thread to
    int id = Helper::find_free_id(this->_threads);

    // if id not found
    if(id == FAILURE)
    {
        return Helper::library_err_printer("there is no place for new id");
    }

    // if priority is out of range
    if(priority >= this->_size || priority < 0)
    {
        return Helper::library_err_printer("priority is not in range");
    }
    Thread* thread;

    // try to allocate a new thread
    try
    {
        thread = new Thread(id, priority,  f);
    }

    // put an error
    catch(std::exception& e)
    {
        Helper::system_err_printer("bad allocation");
        return FAILURE;
    }

    // add the thread to the map of threads and to the vector of ready threads
    this->_threads[id] = thread;
    this->_ready_list.push_back(thread);

    return id;
}



void Scheduler::choose_new_run_thread()
{
    // get the first ready thread
    Thread* thread = this->_ready_list.front();

    // remove thread from ready list
    this->_ready_list.pop_front();

    // update running tread
    this->_running_thread = thread;
}


int Scheduler::terminate_thread(int id)
{
    // check if the id exists
    if(Helper::check_id_exists(this->_threads, id) == FAILURE)
    {
        return FAILURE;
    }

    // if trying to terminate the main thread
    if(id == 0)
    {
        terminate_threads();
        return SUCCESS;
    }
    Thread* thread = this->_threads[id];

    delete_from_ready_list(id);
    this->_threads.erase(id);

    //delete previous allocated threads
    delete_terminated_resources();
    this->_terminated_resources.push_back(thread);
    if(thread == this->_running_thread)
    {
        this->run_new_thread();
    }
    return SUCCESS;
}

int Scheduler::block_thread(int id)
{
    // check if the id exists
    if(Helper::check_id_exists(this->_threads, id) == FAILURE)
    {
        return FAILURE;
    }

    // if trying to block the main thread
    if(id == 0)
    {
        return Helper::library_err_printer("the main thread can't be blocked!!! it will block you");
    }

    // get ready for switching state to blocked
    Thread* thread = this->_threads[id];

    // in case of ready || blocked
    if(thread->get_state() != ThreadStates::RUNNING)
    {
        delete_from_ready_list(id);
        thread->block();
        return SUCCESS;
    }
    
    //in case we got here not through siglongjmp
    if(thread->block() == SUCCESS)
    {
        this->run_new_thread();
    }
    return SUCCESS;
}

int Scheduler::resume_thread(int id)
{
    // check if the id exists
    if(Helper::check_id_exists(this->_threads, id) == FAILURE)
    {
        return FAILURE;
    }

    // resume state
    Thread* thread = this->_threads[id];
    if(thread->get_state() != ThreadStates::BLOCKED)
    {
        return SUCCESS;
    }

    ThreadStates state = thread->get_state();
    thread->resume();

    // check if state changed to ready
    if(state != ThreadStates::READY && thread->get_state() == ThreadStates::READY)
    {
        this->_ready_list.push_back(thread);
    }
    return SUCCESS;
}


Scheduler::Scheduler(int* quantums, int size) : _quantum_counter(1), _running_thread(nullptr), 
_quantums(quantums), _size(size)
{
    Thread* thread;
    try
    {
        // allocate a new thread for the main
        thread = new Thread();
    }

    catch(std::exception& e)
    {
        Helper::system_err_printer("bad allocation");
        return;
    }

    // start new quantom count
    Helper::start_new_quantum(this->_vt_timer, this->_quantums[thread->get_priority()]);

    // initialize the starting thread
    this->_threads[thread->get_id()] = thread;
    this->_running_thread = thread;
}


int Scheduler::change_priority(int tid, int priority)
{
    if(Helper::check_id_exists(this->_threads, tid) == FAILURE)
    {
        return FAILURE;
    }
    if(priority >= this->_size || priority < 0)
    {
        return Helper::library_err_printer("priority is not in range");
    }
    this->_threads[tid]->set_priority(priority);
    return SUCCESS;
}


void Scheduler::delete_terminated_resources()
{
    for(Thread* thread: this->_terminated_resources)
    {
        delete thread;
    }
    this->_terminated_resources.clear();
}