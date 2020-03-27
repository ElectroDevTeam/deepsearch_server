import json
import mimetypes
import os
from pathlib import Path

from notebook.base.handlers import APIHandler


class DeepsearchHandler(APIHandler):
    def get(self, **kwargs):
        query = self.get_argument('query')
        # TODO: consider validating the path. don't allow dir traversal.
        sub_dir = self.get_argument('dir').strip("/").strip("\\")  # joinpath don't like joining "c:\a" and "\b"
        directory = Path(self.settings['contents_manager'].root_dir).joinpath(sub_dir)
        self.finish(json.dumps(self.search_in_files(query, directory)))

    @staticmethod
    def _should_exclude_dir(d):
        return Path(d).name.startswith(".")

    @staticmethod
    def _should_search_in_file(file_path):
        file_types_whitelist = ["ipynb"]
        parts = file_path.split(".")
        # guess_type() returns something like ("text/xml", None). Can also be (None, None).
        mimetype = mimetypes.guess_type(file_path)[0]
        return (mimetype and mimetype.split("/")[0] == "text") or \
               (len(parts) > 2 and parts[-1] in file_types_whitelist)

    @staticmethod
    def search_in_files(query, directory):
        total_results = 0
        results = []
        for folder, dirs, files in os.walk(directory, topdown=True):
            dirs[:] = [d for d in dirs if not DeepsearchHandler._should_exclude_dir(d)]
            for file in files:
                if DeepsearchHandler._should_search_in_file(file):
                    full_path = Path(folder).joinpath(file)
                    # Eliminate the directory from the path.
                    relative_path = full_path.relative_to(directory)
                    results_in_file = DeepsearchHandler.search_in_single_file(full_path, query)
                    if results_in_file:
                        results.append({"filename": str(relative_path),
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
