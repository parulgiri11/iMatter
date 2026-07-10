import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_app()

    def start_app(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        print("\n🔄 Starting app...")
        self.process = subprocess.Popen([sys.executable, "main.py"])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"\n📝 Changed: {event.src_path}")
            time.sleep(0.2)   # small debounce
            self.start_app()

if __name__ == "__main__":
    handler = RestartHandler()
    observer = Observer()
    observer.schedule(handler, path=".", recursive=True)
    observer.start()
    print("👀 Watching for changes... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if handler.process:
            handler.process.terminate()
    observer.join()