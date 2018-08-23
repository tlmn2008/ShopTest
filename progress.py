#!/usr/bin/env python
"""
progress : Class for printing progress
"""

import os
import sys
import time
import argparse
import threading
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def setup_logging_params(parser):
    """
    Set up the logging parameters used by the logging
    """
    parser.add_argument("-g", "--debug", action="store_true", dest="debug", help="enable debug mode")
    parser.add_argument('-l', '--logfile', help='the file used for logging')

def setup_logger(module, args):
    """
    Format the logger and return to sender, send the logs to the stdout and optionally to a logfile
    @return: the logger
    """
    slick_format = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d [%(funcName)s]: %(message)s',
        '%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(module)
    logger.setLevel(logging.DEBUG)

    # The standard out logger is configuerable to show debug, else it will just show warning and above
    logstd = logging.StreamHandler()
    logstd.setLevel(logging.DEBUG if args.debug else logging.WARNING)
    logstd.setFormatter(slick_format)
    logger.addHandler(logstd)

    # The log file will truncate the file and always log with debug level
    if args.logfile is not None:
        logfile = logging.FileHandler(args.logfile, mode='w+')
        logfile.setFormatter(slick_format)
        logfile.setLevel(logging.DEBUG)
        logger.addHandler(logfile)

    # Handle stderr, let stdout operate as normal, in order for print() to work
    class StreamToLogger(object):
        ''' Will just forward logs to the logger '''
        def __init__(self, logger, log_level):
            self.logger = logger
            self.log_level = log_level
            self.linebuf = ''

        def write(self, buf):
            ''' Standard write function '''
            for line in buf.rstrip().splitlines():
                self.logger.log(self.log_level, line.rstrip())

        def flush(self):
            ''' Standard flush function, nothing to do though '''
            pass
    sys.stderr = StreamToLogger(logger, logging.ERROR)

    return logger

def time_string():
    """ returns a string with short date format """
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return str(time_str)

def elapsed_time_string(seconds):
    """ Converts elapsed seconds to an HH:MM:SS string """
    elapsed_h = int(seconds / 3600)
    elapsed_m = int((seconds - elapsed_h * 3600) / 60)
    elapsed_s = int((seconds - elapsed_h * 3600 - elapsed_m * 60))
    elapsed_str = '{:02d}:{:02d}:{:02d}'.format(elapsed_h, elapsed_m, elapsed_s)
    return elapsed_str

def display_message(logger, task, message):
    """ displays the message on the chosen device and format """
    tree_level = task.get_tree_level()
    indent_string = ' '.ljust((tree_level * 2), ' ')
    module_name = indent_string + task.task_name
    task_id = '[' + str(task.task_number) + ']'
    formated_message = indent_string + message
    print '[{:s}] ::{:24s} {:>4s} --  {:s}'.format(time_string(), module_name, task_id, formated_message)
    logger.info(' ::{:24s} {:>4s} --  {:s}'.format(module_name, task_id, formated_message))

class Task(object):
    """ Class for separate tasks """
    def __init__(self, logger, task_name, task_number, parent_task):
        self.__logger = logger
        self.__logger.info('Creating task')
        self.task_name = task_name
        self.task_number = task_number
        self.__start_time = time.time()
        self.__end_time = 0
        self.__child_tasks = []
        self.__parent_task = parent_task
        if parent_task is not None:
            parent_task.add_child_task(self)

    def end(self):
        """ ends a task """
        self.__logger.info('Task ' + self.task_name + ' done')
        self.__end_time = time.time()
        if self.__parent_task is not None:
            self.__logger.debug(
                'Task.end() removing child task ' + self.task_name +
                ' from parent task ' + self.__parent_task.task_name)
            remove_ok = self.__parent_task.remove_child_task(self)
            if not remove_ok:
                self.__logger.error(
                    'Task.end() tried to remove a non existing child task ' + self.task_name +
                    ' from parent task ' + self.__parent_task.task_name)
                return False

        if self.is_child_tasks_done():
            return True
        else:
            self.__logger.error(
                'Task.end() tried to remove a task ' + self.task_name + ' but all child tasks are not done.')
            return False

    def duration(self):
        """ returns duration of a task """
        return int(time.time() - self.__start_time)

    def get_parent_task(self):
        """ return a tasks parent """
        return self.__parent_task

    def remove_child_task(self, task):
        """ remove a child task from a parent """
        try:
            self.__child_tasks.remove(task)
            return True
        except ValueError:
            return False

    def add_child_task(self, task):
        """ add a child task to a parent """
        self.__child_tasks.append(task)

    def get_child_list(self, child_list):
        """ get a list of all children of a task, including the called task itself """
        child_list.append(self.task_number)
        for task in self.__child_tasks:
            task.get_child_list(child_list)
        return child_list

    def is_child_tasks_done(self):
        """ check if all child tasks is done """
        self.__logger.debug('is_child_task_done :: number of remaining child tasks ' + str(len(self.__child_tasks)))
        if len(self.__child_tasks) == 0:
            return True
        else:
            return False

    def get_tree_level(self):
        """ Count the number of parent tasks from this task """
        level = 0
        current_task = self
        while (current_task is not None):
            current_task = current_task.get_parent_task()
            level = level + 1
        return level

class ProgressInactivityThread(threading.Thread):
    """
    Class to report 'inactivity progress' when no other progress has been reported.
    """
    def __init__(self, logger, progress):
        threading.Thread.__init__(self)
        self.__logger = logger
        self.__progress = progress
        self.__lock = threading.Lock()
        self.__cond = threading.Condition(self.__lock)
        # below members are protected by self.__lock and upon change, notified via self.__cond
        self.__num_messages = 0
        self.__done = False

        # set the thread name.
        self.name = 'ProgressInactivityThread'
        logger.debug('Created thread "' + self.name + '" to report progress when no other thread/task does.')

    def run(self):
        """ Main thread method. Called be threading system when start() is called for a thread object. """
        self.__logger.debug('Entering thread run function')
        self.__cond.acquire()
        while self.__num_messages == 0 and not self.__done:
            # If silent in 15min, print remaining tasks.
            self.__cond.wait(15 * 60)
            # check for notifies for progress and done.
            if self.__done:
                self.__logger.info('Have been notified to quit, will exit.')
            elif self.__num_messages > 0:
                self.__logger.debug('Have received ' + str(self.__num_messages) + ' messages, resetting timer.')
                self.__num_messages = 0
            else:
                self.__logger.debug('No progress report has occurred. Will print remaining tasks.')
                self.__progress.progress_report_running_tasks()
        self.__cond.release()
        self.__logger.debug('Exiting thread run function')

    def notify_progress(self):
        """ Method used to notify that progress reporting has occurred. I.e. timer should be reset """
        self.__cond.acquire()
        self.__num_messages += 1
        self.__cond.notify()
        self.__cond.release()

    def notify_done(self):
        """ Method used to notify that thread should quit. I.e. exit it's run method so that it can be joined """
        self.__cond.acquire()
        self.__done = True
        self.__cond.notify()
        self.__cond.release()

class Progress(object):
    """
    Class for printing progress
    """

    def __init__(self, logger):
        self.__logger = logger
        self.__logger.debug('New progress object')
        self.__current_tasks = {}
        self.__task_number = 1
        # Mutex used to assure that a thread is allowed to print its full progress without task switch
        self.__lock = threading.Lock()
        self.__progress_inactivity_thread = None

    def _display_message(self, task, message, notify=True):
        """ Internal wrapper to handle lock etc upon displaying progress report message """
        # make sure lock is held when calling display_message().
        with self.__lock:
            display_message(self.__logger, task, message)
        # notify no progress thread that progress has been received.
        if notify and self.__progress_inactivity_thread is not None:
            self.__progress_inactivity_thread.notify_progress()

    def progress_report_running_tasks(self):
        """ Method that reports remaing running tasks as a progress report message. """
        for _, tasks in self.__current_tasks.items():
            # task 1 is always first in list of tasks
            if len(tasks) > 0 and tasks[0].task_number == 1:
                top_task = tasks[0]
                # False means we shouldn't notify. Makes no sence to notify the object calling this method,
                # would cause deadlock.
                self._display_message(
                    top_task, 'Still running, waiting for tasks: ' + str(top_task.get_child_list([])), False)
                break

    def start(self, task_name, parent_task=None):
        """ start a task """
        self.__logger.info('Progress starting a new task ' + task_name)
        if self.__progress_inactivity_thread is None:
            self.__progress_inactivity_thread = ProgressInactivityThread(self.__logger, self)
            self.__logger.debug('Starting ' + self.__progress_inactivity_thread.name)
            # Set the thread to be daemon. Will make it possible to interrupt (ctrl-C) a running program.
            self.__progress_inactivity_thread.daemon = True
            self.__progress_inactivity_thread.start()

        if parent_task is None:
            parent_task = self.get_current_thread_task()
        task = Task(self.__logger, task_name, self.__task_number, parent_task)
        self.__logger.debug('Started new task ' + task.task_name + ', new task number ' + str(self.__task_number))
        self.__task_number = self.__task_number + 1

        self._display_message(task, 'Started')

        thread_id = threading.current_thread().ident
        if self.__current_tasks.get(thread_id) is None:
            tasks = []
            self.__current_tasks[thread_id] = tasks

        self.__current_tasks[thread_id].append(task)

        return task

    def update(self, task, message):
        """ update progress of a running task  """
        self.__logger.info('Progress updating an existing task ' + task.task_name + ' message: ' + message)
        self._display_message(task, '  > ' + message)

    def _remove_from_dictionary(self, task):
        """ Remove task from current_tasks dictonary. """
        thread_id = threading.current_thread().ident
        self.__current_tasks[thread_id].remove(task)

    def stop(self, task):
        """ finish a running task  """
        self.__logger.info('Progress finished a task ' + task.task_name)
        return_value = task.end()
        if not return_value:
            self.abort(task, 'Error when stopping a task. See log for info')
        self._display_message(task, 'Done! Elapsed time: ' + elapsed_time_string(task.duration()))
        return_value = task.is_child_tasks_done()
        # Remove task from current_tasks dictonary
        self._remove_from_dictionary(task)

        # Stop the no progress thread if top level task is being stopped
        self.__logger.debug('At stop of: ' + task.task_name + ', tree level is: ' + str(task.get_tree_level()))
        if task.get_tree_level() == 1 and self.__progress_inactivity_thread is not None:
            self.__logger.debug('Stopping/joining ' + self.__progress_inactivity_thread.name)
            self.__progress_inactivity_thread.notify_done()
            self.__progress_inactivity_thread.join()

        return return_value

    def abort(self, task, message):
        """ Scream and die """
        self.__logger.info('Progress aborting task ' + task.task_name + ' message: ' + message)
        self._display_message(task, 'ABORTED! ' + message)
        # need to end task as below sys.exit may only exit current thread. Thus, main thread will still be alive
        # and since it requires that all its childrens are stopped when it stops/exits we need to end this task.
        task.end()
        # also, remove task from current_tasks dictonary
        self._remove_from_dictionary(task)

        sys.exit('Execution aborted')

    def get_current_thread_task(self):
        """ Get the last appended task for the current thread """
        thread_id = threading.current_thread().ident
        if (self.__current_tasks.get(thread_id) is None) or (len(self.__current_tasks.get(thread_id)) == 0):
            return None
        # return the last (that is -1) attached task for current thread.
        current_thread_task = self.__current_tasks[thread_id][-1]
        return current_thread_task

def main():
    """
    Main method used if invoked as stand alone script
    Mainly used to test class
    """
    parser = argparse.ArgumentParser(description='Example of progress usage')
    setup_logging_params(parser)
    params = parser.parse_args()
    logger = setup_logger(os.path.basename(sys.argv[0]), params)
    logger.info('Started')

    # start progress
    prog = Progress(logger)
    task1 = prog.start('Task 1')
    prog.update(task1, 'Update 1')
    task2 = prog.start('Task 2')
    prog.update(task2, 'Update 1')
    task3 = prog.start('Task 3')
    prog.update(task3, 'Update 1')
    print task1.get_child_list([])
    print 'again, to assure that a same result is received.'
    print task1.get_child_list([])
    task4 = prog.start('Task 4')
    prog.update(task4, 'Update 1')
    print task1.get_child_list([])
    if not prog.stop(task4):
        prog.abort(task4, 'Task 4 has remaining childs')
    task5 = prog.start('Task 5')
    prog.update(task5, 'Update 1')
    if not prog.stop(task5):
        prog.abort(task5, 'Task 5 has remaining childs')
    if not prog.stop(task3):
        prog.abort(task3, 'Task 3 has remaining childs')
    if not prog.stop(task2):
        prog.abort(task2, 'Task 2 has remaining childs')
    prog.stop(task1)
    task6 = prog.start('Task 6')
    prog.abort(task6, 'Aborted because of test!')

if __name__ == '__main__':
    main()
