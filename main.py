# FASTER CODE USING CONCURRENT.FUTURES
import concurrent.futures
import pikepdf
import itertools
import colorama
import os


locked_file = input("Input the directory of the locked pdf file: ")
if not os.path.isfile(locked_file):
    print("File does not exist")
    exit(1)
choices = [''.join(x) for x in itertools.permutations('0123456789', 4)]
total_password = len(choices)


def progress_bar(progress, total, color=colorama.Fore.YELLOW):
    percent = (progress / float(total)) * 100
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(color + f"\r|{bar}| {percent:.2f}%", end=" ", flush=True)
    if progress == total:
        print(colorama.Fore.GREEN + f"\r|{bar}| {percent:.2f}%", end="\r")


def brute_force(password):

    try:
        with pikepdf.open(locked_file, password=password) as pdf_file:
            pdf_file.save(f"{locked_file}_unlocked.pdf")
        return password
    except:
        return False


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        i = 0
        for result in executor.map(brute_force, choices):
            if result:
                bar = '█' * 100
                print(colorama.Fore.GREEN + f"\r|{bar}| 100%" + colorama.Fore.RESET, end=" ", flush=True)
                print("\nSuccess---------- File is Unlocked and the password is: ", result)
                print("File is saved as: ", f"{locked_file}_unlocked.pdf")
                exit()
            else:
                progress_bar(i, total_password)
            i += 1
    print("\nCould not find the password")