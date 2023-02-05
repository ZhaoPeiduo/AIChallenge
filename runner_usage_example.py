from datetime import datetime

import runner
import time

if __name__ == '__main__':
    start_time = time.time()
    runner = runner.Runner(datetime(2023, 1, 20), datetime(2023, 2, 4), "chatgpt", 100, "chrome")
    runner()  # Call the __call__ method
    end_time = time.time()
    print(f"Total time taken = {end_time - start_time}")
