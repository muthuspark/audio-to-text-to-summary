import queue
import os


# Request class to store request data
class PersistentQueueRequest:
    def __init__(self, data, recording_name):
        self.data = data
        self.recording_name = recording_name


# Queue with custom put and get methods
class PersistentQueue(queue.Queue):
    """
    PersistentQueue class ensures that request data is persisted to a file when a request is added to the queue and
    removed from the file when the request is retrieved from the queue. This way, even if the program crashes or is
    terminated unexpectedly, the requests that haven't been processed yet will still be available in the file when
    the program is restarted.
    """

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        if os.path.exists(self.file_path):
            self.load_from_file()

    def put(self, item, block=True, timeout=None):
        # Persist request data to file
        with open(self.file_path, 'a') as file:
            file.write(f"{item.data}\n")
        super().put(item, block, timeout)

    def get(self, block=True, timeout=None):
        item = super().get(block, timeout)
        # Remove request data from file
        self.remove_from_file(item.data)
        return item

    def load_from_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                for line in file:
                    data = line.strip()
                    request = Request(data)
                    self.put(request)

    def remove_from_file(self, data):
        # Create a temporary file
        tmp_file_path = f"{self.file_path}.tmp"
        with open(self.file_path, 'r') as file, open(tmp_file_path, 'w') as tmp_file:
            for line in file:
                if line.strip() != data:
                    tmp_file.write(line)
        # Replace the original file with the temporary file
        os.replace(tmp_file_path, self.file_path)

    def is_empty(self):
        """
        Check if the queue is empty by combining the results
        of the base class is_empty method and the existence
        of data in the file.
        """
        base_empty = super().empty()
        file_empty = not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0
        return base_empty and file_empty
