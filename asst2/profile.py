PROFILE_FUNCTIONS = True
PROFILE_RESULTS = {}

def profile(func):
    def wrapper(*args, **kwargs):
        if not PROFILE_FUNCTIONS:
            func(*args, **kwargs)
        else:
            from time import clock
            start = clock()
            func(*args, **kwargs)
            time_taken = clock() - start
            if func.__name__ not in PROFILE_RESULTS:
                PROFILE_RESULTS[func.__name__] = {
                    "avg_time": time_taken,
                    "num_times_called": 1
                }
            else:
                old_result = PROFILE_RESULTS[func.__name__]
                old_avg = old_result["avg_time"] * old_result["num_times_called"]
                new_avg = (old_avg + time_taken) / (old_result["num_times_called"]+1)
                PROFILE_RESULTS[func.__name__]["avg_time"] = new_avg
                PROFILE_RESULTS[func.__name__]["num_times_called"] += 1

    return wrapper

@profile
def my_func():
    sum = 0
    for i in xrange(1 << 25):
        sum += i

my_func()
print PROFILE_RESULTS
