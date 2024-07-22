import requests
import time
import re

from random import randint

BOOK_PATH = 'https://www.gutenberg.org/files/2638/2638-0.txt'


def benchmark(func):
    """
    Декоратор, выводящий время, которое заняло выполнение декорируемой функции
    """
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Время выполнения функции {func.__name__}: {end - start:.6f}\n')
        return result
    return wrapper


def logging(func):
    """
    Декоратор, который выводит параметры с которыми была вызвана функция
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'Функция вызвана с параметрами\n{args}, {kwargs}\n')
        return result
    return wrapper


def counter(func):
    """
    Декоратор, считающий и выводящий количество вызовов декорируемой функции
    """
    count = 0

    def wrapper(*args, **kwargs):
        nonlocal count
        result = func(*args, **kwargs)
        count += 1
        print(f'Функция была вызвана: {count} раз\n')
        return result
    return wrapper


def memo(func):
    """
    Декоратор, запоминающий результаты исполнения функции func, чьи аргументы args должны быть хешируемыми
    """
    cache = {}

    def fmemo(*args):
        if args not in cache:
            cache[args] = func(*args)  # создаем словарь для хранения аргументов
            # фунции, если текущих аргументов нет в словаре, то добавляем их туда вместе с результатом выполнения функции
            # с текущими аргументами
        return cache[args]

    fmemo.cache = cache
    return fmemo


@counter
@logging
@benchmark
def word_count(word, url=BOOK_PATH):
    """
    Функция для посчета указанного слова на html-странице
    """

    # отправляем запрос в библиотеку Gutenberg и забираем текст
    raw = requests.get(url).text

    # заменяем в тексте все небуквенные символы на пробелы
    processed_book = re.sub(r'[^a-zA-Z]', ' ', raw).lower()

    # считаем
    cnt = len(re.findall(word.lower(), processed_book))

    return f"Cлово {word} встречается {cnt} раз"


#print(word_count('whole'))


@benchmark
def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)


fib(5)