import json
import os

from notebook.base.handlers import APIHandler


class DeepsearchHandler(APIHandler):
    def get(self, **kwargs):
        quarry = self.get_argument('quarry')
        # TODO: consider validating the path. don't allow dir traversal.
        directory = self.settings['contents_manager'].root_dir + "\\" + self.get_argument('dir')
        self.finish(json.dumps(self.search_in_files(quarry, directory)))

    @staticmethod
    def search_in_files(quarry, directory):
        results = []
        for folder, dirs, files in os.walk(directory):
            for file in files:
                # TODO: Consider checking for file type (can use mimetypes.guess_type())
                full_path = os.path.join(folder, file)
                with open(full_path, 'rb') as f:
                    i = 1
                    for line in f:
                        line = str(line, errors='ignore')
                        if quarry in line:
                            results.append((full_path, i, line.rstrip()))
                        i += 1
        return results
