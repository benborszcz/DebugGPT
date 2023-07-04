import os
import shutil
import difflib
import time
from collections import deque
from filecmp import dircmp

class ChangeLogger:
    def __init__(self, directory):
        self.directory = directory  # directory to be monitored
        self.backup_directory = f"{os.getcwd()}\\backup7Hu9lsxU802skPuy2"  # backup directory
        self.changes = deque()  # deque to store changes
        self.create_backup()  # create initial backup

    def create_backup(self):
        # if backup directory exists, remove it
        if os.path.exists(self.backup_directory):
            shutil.rmtree(self.backup_directory, ignore_errors=True)
        # copy the directory to be monitored to the backup directory
        shutil.copytree(self.directory, self.backup_directory, ignore=shutil.ignore_patterns('.git'))

    def check_changes(self):
        # compare the directory and the backup directory
        comparison = dircmp(self.directory, self.backup_directory)
        # handle the differences found
        self.handle_differences(comparison)

    def handle_differences(self, comparison):
        # for each file that differs
        for file in comparison.diff_files:
            # get the path of the original file and the changed file
            original_file = os.path.join(self.backup_directory, file)
            changed_file = os.path.join(self.directory, file)
            # open both files
            with open(original_file, 'r') as f1, open(changed_file, 'r') as f2:
                # get the differences between the two files
                diff = difflib.unified_diff(
                    f1.readlines(),
                    f2.readlines(),
                    fromfile=original_file,
                    tofile=changed_file,
                )
                # append the differences to the changes deque
                self.changes.appendleft((time.time(), ''.join(diff), changed_file))

    def revert_last_change(self):
        # if there are changes
        if self.changes:
            # get the last change
            _, _, changed_file = self.changes.popleft()
            # get the path of the backup file
            backup_file = os.path.join(self.backup_directory, os.path.basename(changed_file))
            # copy the backup file to the changed file (revert the change)
            shutil.copy2(backup_file, changed_file)

    def display_changes(self):
        # for each change
        for change_time, diff, _ in self.changes:
            # print the time of the change and the differences
            print(f"Time: {time.ctime(change_time)}")
            print(diff)

    def get_versions(self):
        versions = []
        # for each change
        for _, _, file in self.changes:
            # open the file
            with open(file, 'r') as f:
                # append the file name and its content to the versions list
                versions.append((file, f.read()))
        return versions
