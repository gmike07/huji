//
// Created by Mike on 3/16/2020.
//

#ifndef EX2_HELPER_H
#define EX2_HELPER_H

#include "Thread.h"
#include <map>
#include <signal.h>
#include <iostream>
#include <sys/time.h>
#include "uthreads.h"
#include <string>
#define SYS_ERR "system error: "
#define LIB_ERR "thread library error: "
class Helper
{
public:

  /**
   * print a system error
   * @param msg error to print
   */
  static void system_err_printer(const std::string& msg);

  /**
   * print a library error
   * @param  msg error to print
   * @return     FAILURE
   */
  static int library_err_printer(const std::string& msg);

  /**
   * finds the first free id in a map of threads
   * @param  threads map of threads
   * @return         id of free spot on success, -1 on failure
   */
  static int find_free_id(const std::map<int, Thread*> &threads);

  /**
  * fix the quantum timer according to start and interval
  * @param timer timer
  * @param start    starting time of quantum
  * @param interval interval between quantums (quantum length in usecs)
  */
  static void start_new_quantum(struct itimerval &timer, unsigned int start);


  /**
   * converts usces to timeval
   * @param  usec usecs
   * @return      timeval
   */
  static struct timeval convert_usec_timeval(unsigned int usec);


  /**
   * [check_id_exists description]
   * @param  id [description]
   * @return    [description]
   */
  static int check_id_exists(const std::map<int, Thread*> &threads, int id);

};

#endif //EX2_SCHEDULAR_H
