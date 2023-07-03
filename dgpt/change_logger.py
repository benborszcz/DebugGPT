import os
import shutil
import difflib
import time
from collections import deque
from filecmp import dircmp
import os

class ChangeLogger:
    def __init__(self, directory):
        self.directory = directory
        self.backup_directory = f"{os.getcwd()}\\backup"
        self.changes = deque()
        self.create_backup()

    def create_backup(self):
        if os.path.exists(self.backup_directory):
            shutil.rmtree(self.backup_directory, ignore_errors=True)
        shutil.copytree(self.directory, self.backup_directory, ignore=shutil.ignore_patterns('.git'))

    def check_changes(self):
        comparison = dircmp(self.directory, self.backup_directory)
        self.handle_differences(comparison)

    def handle_differences(self, comparison):
        for file in comparison.diff_files:
            original_file = os.path.join(self.backup_directory, file)
            changed_file = os.path.join(self.directory, file)
            with open(original_file, 'r') as f1, open(changed_file, 'r') as f2:
                diff = difflib.unified_diff(
                    f1.readlines(),
                    f2.readlines(),
                    fromfile=original_file,
                    tofile=changed_file,
                )
                self.changes.appendleft((time.time(), ''.join(diff), changed_file))
                #shutil.copy2(changed_file, original_file)  # update backup

    def revert_last_change(self):
        if self.changes:
            _, _, changed_file = self.changes.popleft()
            backup_file = os.path.join(self.backup_directory, os.path.basename(changed_file))
            shutil.copy2(backup_file, changed_file)  # revert to backup

    def display_changes(self):
        for change_time, diff, _ in self.changes:
            print(f"Time: {time.ctime(change_time)}")
            print(diff)

    def get_versions(self):
        versions = []
        for _, _, file in self.changes:
            with open(file, 'r') as f:
                versions.append((file, f.read()))
        return versions