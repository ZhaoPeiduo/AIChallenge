import runner

if __name__ == '__main__':
    runner = runner.Runner(5, "covid", 40)
    print(runner())  # Call the __call__ method