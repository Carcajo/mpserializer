from serializers.serializer import Serializer
serializers_names = ['json', 'yaml', "toml", "pickle"]


def restore_from_file(serializer_name, serializer, func):
    if serializer_name == 'pickle':
        c = 'b'
    else:
        c = ''
    with open("test_test.txt", 'w' + c + '+') as file:
        serializer.dump(func, file)
    with open("test_test.txt", 'r' + c) as file:
        restored_func = serializer.load(file)
    return restored_func


def simple_func(a, b):
    return a + b


def test_1():
    def test(serializer_name):
        serializer = Serializer(serializer_name)
        restored_func = serializer.loads(serializer.dumps(simple_func))
        restored_from_file_func = restore_from_file(serializer_name, serializer, simple_func)
        assert restored_func(10, 20) == restored_from_file_func(10, 20) == simple_func(10, 20)

    for name in serializers_names:
        test(name)


def fib(n):
    if n < 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def test_2():
    def test(serializer_name):
        serializer = Serializer(serializer_name)
        restored_func = serializer.loads(serializer.dumps(fib))
        restored_from_file_func = restore_from_file(serializer_name, serializer, fib)
        assert restored_func(10) == restored_from_file_func(10) == fib(10)
        assert restored_func(6) == restored_from_file_func(6) == fib(6)

    for name in serializers_names:
        test(name)


def power2(x):
    return x * x


def power3(x):
    return x * x * x


d = 228


def my_func(a=2, b=3):
    c = power3(a) + power2(b) + d
    return c


def test_3():
    def test(serializer_name):
        serializer = Serializer(serializer_name)
        restored_func = serializer.loads(serializer.dumps(my_func))
        restored_from_file_func = restore_from_file(serializer_name, serializer, my_func)
        assert restored_func(10, 20) == restored_from_file_func(10, 20) == my_func(10, 20)
        assert restored_func(10) == restored_from_file_func(10) == my_func(10)
        assert restored_func() == restored_from_file_func() == my_func()

    for name in serializers_names:
        test(name)


def get_max(a, b):
    return max(a, b)


def test_4():
    def test(serializer_name):
        serializer = Serializer(serializer_name)
        restored_func = serializer.loads(serializer.dumps(get_max))
        restored_from_file_func = restore_from_file(serializer_name, serializer, get_max)
        assert restored_func(10, 20) == restored_from_file_func(10, 20) == get_max(10, 20)
        assert restored_func(20, 10) == restored_from_file_func(20, 10) == get_max(20, 10)
        assert restored_func(100, 100) == restored_from_file_func(100, 100) == get_max(100, 100)

    for name in serializers_names:
        test(name)


def test_5():
    def test(serializer_name):
        serializer = Serializer(serializer_name)
        func = lambda x: x + 2
        restored_func = serializer.loads(serializer.dumps(func))
        restored_from_file_func = restore_from_file(serializer_name, serializer, func)
        assert restored_func(10) == restored_from_file_func(10) == func(10)
        assert restored_func(20) == restored_from_file_func(20) == func(20)

    for name in serializers_names:
        test(name)
