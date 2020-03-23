import json
import os

from notebook.base.handlers import APIHandler


class DeepsearchHandler(APIHandler):
    def get(self, **kwargs):
        query = self.get_argument('query')
        # TODO: consider validating the path. don't allow dir traversal.
        if self.get_argument('dir'):
            directory = self.settings['contents_manager'].root_dir + "\\" + self.get_argument('dir')
        else:
            directory = self.settings['contents_manager'].root_dir
        self.finish(json.dumps(self.search_in_files(query, directory)))

    @staticmethod
    def search_in_files(query, directory):
        total_results = 0
        results = []
        for folder, dirs, files in os.walk(directory):
            for file in files:
                # TODO: Consider checking for file type (can use mimetypes.guess_type())
                full_path = os.path.join(folder, file)
                # Eliminate the directory from the path.
                partial_path = full_path.rpartition(directory + "\\")[-1]

                results_in_file = DeepsearchHandler.search_in_single_file(full_path, query)
                if results_in_file:
                    results.append({"filename": partial_path,
                                    "results": results_in_file})
                    total_results += len(results_in_file)
        return {"totalResults": total_results,
                "totalFiles": len(results),
                "results": results}

    @staticmethod
    def search_in_single_file(full_path, query):
        """
        :param full_path: The path to the file.
        :param query: The string the search in the file.
        :return: List of dicts of the format {linenumber:, content:}
        """
        results = []
        with open(full_path, 'rb') as f:
            i = 1
            for line in f:
                # Ignore non utf8 chars. We can't cast them to str, and we can't send them as json.
                line = str(line, errors='ignore')
                if query in line:
                    results.append({"linenumber": i,
                                    "content": line.rstrip()})
                i += 1
        return results
