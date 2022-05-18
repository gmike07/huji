
// Created by Mike on 3/16/2020.
//

#include "Helper.h"
#include "Scheduler.h"
#define SECOND 1000000

void Helper::system_err_printer(const std::string& msg)
{
    std::cerr << SYS_ERR << msg << std::endl;
    exit(1);
}

int Helper::library_err_printer(const std::string& msg)
{
    std::cerr << LIB_ERR << msg << std::endl;
    return FAILURE;
}


int Helper::find_free_id(const std::map<int, Thread*> &threads)
{
    // check if the number of threads is maximized
    if(threads.size() == MAX_THREAD_NUM)
    {
        return FAILURE;
    }

    // loop through the id's and find a free id
    for(int i = 0; i < MAX_THREAD_NUM; i++)
    {
        if(threads.count(i) == 0)
        {
            return i;
        }
    }
    return FAILURE;
}

void Helper::start_new_quantum(struct itimerval &timer, unsigned int start)
{
    timer.it_value = Helper::convert_usec_timeval(start);
    timer.it_interval = Helper::convert_usec_timeval(0);

    if(setitimer(ITIMER_VIRTUAL, &timer, nullptr))
    {
        system_err_printer("error in calling setitimer");
    }
}

struct timeval Helper::convert_usec_timeval(unsigned int usec)
{
    struct timeval curr{};
    curr.tv_usec = usec % SECOND;
    curr.tv_sec = usec / SECOND;
    return curr;
}

int Helper::check_id_exists(const std::map<int, Thread*> &threads, int id)
{
    // check if id exists
    if(threads.count(id) == 0)
    {
        return Helper::library_err_printer("invalid id of thread");
    }
    return SUCCESS;
}
