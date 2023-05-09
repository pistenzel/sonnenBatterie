"""
https://en.wikipedia.org/wiki/Fibonacci_sequence
In mathematics, the Fibonacci sequence is a sequence in which each number is the sum of the two preceding ones.
Numbers that are part of the Fibonacci sequence are known as Fibonacci numbers, commonly denoted Fn.
The sequence commonly starts from 0 and 1, although some authors start the sequence from 1 and 1 or sometimes
(as did Fibonacci) from 1 and 2. Starting from 0 and 1, the first few values in the sequence are:
    0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144.
"""


def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def get_fibonacci_sequence_from_generator(n: int = 1) -> list:
    generator = fibonacci_generator()
    return [next(generator) for i in range(n)]


class Fibonacci:

    def __init__(self):
        self.sequence = [0, 1]

    def __call__(self, n):
        if n < len(self.sequence):
            return self.sequence[n]
        else:
            fib_number = self(n - 1) + self(n - 2)
            self.sequence.append(fib_number)
        return self.sequence[n]


def get_fibonacci_sequence_from_class(n: int = 1) -> list:
    generator = Fibonacci()
    return [generator(i) for i in range(n)]


def fibonacci_recursive(n: int):
    if n in {0, 1}:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def get_fibonacci_sequence_from_recursive_method(n: int = 1) -> list:
    return [fibonacci_recursive(i) for i in range(n)]


def fibonacci_iterative(n: int):
    if n in {0, 1}:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def get_fibonacci_sequence_from_iterative_method(n: int = 1) -> list:
    return [fibonacci_iterative(i) for i in range(n)]


# ######################################################################################################################
GENERATOR = 1
RECURSIVE = 2
CLASS = 3
ITERATIVE = 4

GENERATOR_TYPES = {
    GENERATOR: get_fibonacci_sequence_from_generator,
    RECURSIVE: get_fibonacci_sequence_from_recursive_method,
    CLASS: get_fibonacci_sequence_from_class,
    ITERATIVE: get_fibonacci_sequence_from_iterative_method,
}


class FibonacciGeneratorFactory:

    @staticmethod
    def get_fibonacci_generator(generator: int):
        generator = GENERATOR_TYPES.get(generator)
        return generator


if __name__ == '__main__':
    gen = FibonacciGeneratorFactory.get_fibonacci_generator(RECURSIVE)
    print(gen(10))
