import threading
import itertools
import time
import sys

class Signal:
    go = True

def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:
            break
    write(' ' * len(status) + '\x08' * len(status))
    # write(' ' * len(status))        

def slow_function(n):
    time.sleep(n)
    return 77

def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin,
                            args=('waiting...', signal))
    spinner.start()
    result = slow_function(4)
    signal.go = False
    spinner.join()
    return result

def main():
    result = supervisor()
    print('Answer:', result)

if __name__ == '__main__':
    main()