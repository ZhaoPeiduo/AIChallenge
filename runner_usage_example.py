import runner

if __name__ == '__main__':
    runner = runner.Runner(20, "the wandering earth", 40, "chrome")
    print(runner())  # Call the __call__ method
