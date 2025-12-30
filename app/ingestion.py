import time 
def tail_log(file_path):
    """
    Generator that yields new log lines as they are written.
    Mimics `tail -F` behavior.
    """
    with open(file_path, "r") as file:
        file.seek(0, 2)  # move to end of file
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)  # <-- critical
                continue
            yield line.strip()
