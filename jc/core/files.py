import os
import pandas as pd
from django.conf import settings
from core import clients
from core import data


class FileManager:
    def __init__(self):
        self.client = clients.CtpClient()

    def make_filename(self, name):
        name = name if name.endswith('s') else f"{name}s"
        ext = data.SOURCES[name]['ext']
        name = os.path.join(settings.DATA_DIR, name)
        filename = f"{name}.{ext}"
        return filename

    def save_content(self, name, content):
        filename = self.make_filename(name)
        os.makedirs(os.path.dirname(filename))
        with open(filename, 'w') as fd:
            fd.write(content.decode())

    def update_data(self, name):
        url = data.SOURCES[name]['url']
        response = self.client.get(url)
        self.save_content(
            name=f'{name}.csv',
            content=response.content,
        )

    def check_file_exists(self, filename):
        try:
            with open(filename, 'r') as fd:
                pass
            return True
        except IOError:
            return False

    def download(self, name, update=False):
        filename = self.make_filename(name)
        if update:
            self.update_data(filename)
        else:
            if not self.check_file_exists(filename):
                self.update_data(name)

    def open(self, name):
        filename = self.make_filename(name)
        return open(filename)

    def read_csv(self, name):
        filename = self.make_filename(name)
        return pd.read_csv(filename)
