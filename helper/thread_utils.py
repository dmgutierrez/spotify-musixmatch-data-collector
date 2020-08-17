from helper.settings import logger, http_response_500, http_response_200
from helper.streaming_thread import StreamingThread
from typing import Optional


def kill_streaming_thread(streaming_thread: StreamingThread):
    response = False
    try:
        # Still alive then kill it
        if streaming_thread.is_alive():
            streaming_thread.kill()
            streaming_thread.join()
            response = True
            logger.warning("Thread %s was killed!", str(streaming_thread.name))
    except Exception as e:
        logger.error(e)
    return response


def generate_batch_thread(batch_threads: list, thread_name: str, target_func, args):
    try:
        add_thread = True

        # If the list of threads is not empty
        if batch_threads:
            # Check if there is a thread with the same name running
            thread_names = [i.name for i in batch_threads]
            # Thread with the same name
            if thread_name in thread_names:
                thread_idx = thread_names.index(thread_name)

                # If it is still alive
                if batch_threads[thread_idx].is_alive():
                    add_thread = False
                else:
                    # remove old thread from list
                    batch_threads.pop(thread_idx)
        if add_thread:
            streaming_thread: StreamingThread = create_new_streaming_thread(
                thread_name=thread_name,
                target_func=target_func,
                args=args)
            # Save thread into list
            batch_threads.append(streaming_thread)

    except Exception as e:
        logger.error(e)
    return batch_threads


def start_all_batch_threads(batch_threads: list):
    try:
        # Start thread process
        # from the main-thread, starts child threads
        for thread in batch_threads:
            thread.start()
    except Exception as e:
        logger.error(e)


def create_new_streaming_thread(thread_name: str, target_func, args):
    streaming_thread: Optional[StreamingThread] = None
    try:
        # Create new thread
        streaming_thread: StreamingThread = StreamingThread(
            name=thread_name, target=target_func, args=args)
    except Exception as e:
        logger.error(e)
    return streaming_thread


def join_threads(batch_threads: list, thread_names: list):
    try:
        logger.info("Waiting for threads to finish ... ")
        for thread_name in thread_names:
            # Find thread by name
            if thread_name in batch_threads:
                thread_idx: int = thread_names.index(thread_name)
                thread: StreamingThread = batch_threads[thread_idx]
                # Join
                thread.join()
    except Exception as e:
        logger.error(e)


def clean_batch_threads(batch_threads: list):
    try:
        logger.info("Cleaning Batch threads ")
        for idx, thread in enumerate(batch_threads):
            batch_threads.pop(idx)
    except Exception as e:
        logger.error(e)