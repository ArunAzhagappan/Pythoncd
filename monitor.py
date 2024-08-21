import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

class Watcher:
    DIRECTORY_TO_WATCH = "https://github.com/ArunAzhagappan/pythonreplacingargo.git"  # Replace with your directory path

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Observer Stopped")
        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'modified':
            # Trigger the GitHub Actions workflow
            print(f"Detected change in {event.src_path}")
            response = requests.post(
                "https://api.github.com/repos/<ArunAzhagappan>/<pythonreplacingargo>/dispatches",
                headers={
                    "Authorization": "token <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>",
                    "Accept": "application/vnd.github.v3+json",
                },
                json={
                    "event_type": "manual-trigger"
                }
            )
            if response.status_code == 204:
                print("GitHub Actions workflow triggered successfully!")
            else:
                print(f"Failed to trigger GitHub Actions workflow: {response.status_code}")

if __name__ == '__main__':
    w = Watcher()
    w.run()
