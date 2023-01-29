import runner
import time

if __name__ == '__main__':
    start_time = time.time()
    runner = runner.Runner(5, "the wandering earth", 40, "chrome")
    runner()  # Call the __call__ method
    end_time = time.time()
    print(f"Total time taken = {end_time - start_time}")
