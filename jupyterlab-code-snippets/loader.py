import os

from pathlib import PurePath

from jupyter_core.paths import jupyter_path

import tornado


class SnippetsLoader:
    def __init__(self):
        self.snippet_paths = jupyter_path("code_snippets")

    def collect_snippets(self):
        snippets = []
        for root_path in self.snippet_paths:
            for dirpath, dirnames, filenames in os.walk(root_path):
                for f in filenames:
                    fullpath = PurePath(dirpath).relative_to(root_path).joinpath(f)

                    if fullpath.parts not in snippets:
                        snippets.append(fullpath.parts)

        snippets.sort()
        return snippets

    def get_snippet_content(self, snippet):
        try:
            for root_path in self.snippet_paths:
                path = os.path.join(root_path, *snippet)

                # Prevent access to the entire file system when the path contains '..'
                accessible = os.path.realpath(path).startswith(root_path)

                if accessible and os.path.isfile(path):
                    with open(path) as f:
                        return f.read()
        except:
            raise tornado.web.HTTPError(status_code=500)

        raise tornado.web.HTTPError(status_code=404)
