import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self, params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK', data=filelist)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}", 'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    # tambah fungsi untuk upload
    def post(self, params=[]):
        if not (len(params) == 2):
            return dict(status='ERROR')

        # cek file yang sama
        filename = params[0]
        if os.path.exists(filename):
            return dict(status='ERROR', data=f'{filename} file sudah ada dalam folder')

        file = base64.b64decode(params[1])
        fp = open(filename, 'wb+')
        fp.write(file)
        fp.close()
        return dict(status='OK', data=f'file {filename} berhasil diupload')

    # tambah fungsi untuk delete
    def delete(self, params=[]):
        if not (len(params) == 1):
            return dict(status='ERROR')

        filename = params[0]
        if not os.path.exists(filename):
            return dict(status='ERROR')

        os.remove(filename)
        return dict(status='OK', data=f'file {filename} berhasil didelete')

    def version(self, params=[]):
        return dict(status='OK', data='versi 1.0')


if __name__ == '__main__':
    f = FileInterface()
    print(f.version())
    print(f.list())
    print(f.get(['pokijan.jpg']))