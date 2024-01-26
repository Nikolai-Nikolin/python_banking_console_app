import sys
from colorama import Fore, Back, Style
import time
from tqdm import tqdm


# Функция полоски загрузки
def progress_bar():
    print(Fore.GREEN + 'Секунду...', end='', flush=True)
    for i in range(20):
        time.sleep(0.05)
        print(Fore.GREEN + '█', end='', flush=True)
    print(Fore.GREEN + ' 100%', end='\n')

# def progress_bar(duration=0.03):
#     print()
#     for i in range(1, 101):
#         print(f"Обработка: {i}% ", end="")
#         print("█" * (i // 2), end="")
#         print("\r", end="")
#         time.sleep(duration)
#     print()

# def progress_bar(duration=0.02):
#     total_iterations = 100
#     with tqdm(total=total_iterations, desc=Fore.GREEN + 'Секунду...', ncols=70) as pbar:
#         for _ in range(total_iterations):
#             time.sleep(duration)
#             pbar.update(1)
#     print()

# def progress_bar(duration=0.03):
#     print()
#
#     def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end='\r'):
#         percent = ("{0:." + str(decimals) + "f}").format(100 *
#                                                          (iteration / float(total)))
#         filled_length = int(length * iteration // total)
#         bar = fill * filled_length + '-' * (length - filled_length)
#         print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
#         sys.stdout.flush()
#         if iteration == total:
#             print()
#
#     total_iterations = 100
#     for i in range(1, total_iterations + 1):
#         time.sleep(duration)
#         print_progress_bar(i, total_iterations,
#                            prefix='Обработка:', suffix='Завершено.', length=30)
#
#
# print("Готово!")
