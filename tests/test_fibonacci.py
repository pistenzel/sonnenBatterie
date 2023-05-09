import pytest

from fibonacci import FibonacciGeneratorFactory, RECURSIVE, GENERATOR, CLASS, ITERATIVE


@pytest.fixture
def fibonacci_factory(request):
    generator = request.param
    yield FibonacciGeneratorFactory.get_fibonacci_generator(generator)


@pytest.mark.parametrize(
    "fibonacci_factory, number, expected_sequence",
    [
        (GENERATOR, 10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]),
        (RECURSIVE, 10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]),
        (CLASS, 10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]),
        (ITERATIVE, 10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]),
    ], indirect=['fibonacci_factory']
)
def test_fibonacci(fibonacci_factory, number, expected_sequence):
    assert fibonacci_factory(number) == expected_sequence
