import json
import os

from notebook.base.handlers import APIHandler


class DeepsearchHandler(APIHandler):
    def get(self, **kwargs):
        query = self.get_argument('query')
        # TODO: consider validating the path. don't allow dir traversal.
        directory = self.settings['contents_manager'].root_dir + "\\" + self.get_argument('dir')
        self.finish(json.dumps(self.search_in_files(query, directory)))

    @staticmethod
    def search_in_files(query, directory):
        results = []
        for folder, dirs, files in os.walk(directory):
            for file in files:
                # TODO: Consider checking for file type (can use mimetypes.guess_type())
                full_path = os.path.join(folder, file)
                results += DeepsearchHandler.search_in_single_file(full_path, query, directory)
        return results

    @staticmethod
    def search_in_single_file(full_path, query, root_directory=None):
        """
        :param full_path: The path to the file.
        :param query: The string the search in the file.
        :param root_directory: The root directory - only so we can eliminate it from the results.
        :return: [(partial_path, line_number, the_line), ...]
        """
        results = []
        with open(full_path, 'rb') as f:
            partial_path = full_path.rpartition(root_directory + "\\")[-1]
            i = 1
            for line in f:
                # Ignore non utf8 chars. We can't cast them to str, and we can't send them as json.
                line = str(line, errors='ignore')
                if query in line:
                    results.append((partial_path, i, line.rstrip()))
                i += 1
        return results
