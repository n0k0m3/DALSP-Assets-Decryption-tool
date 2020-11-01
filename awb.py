import json
import os
import posixpath
import re
import struct
import urllib.parse
import urllib.request
from argparse import ArgumentParser
from multiprocessing.pool import ThreadPool
from shutil import rmtree

from pkg_resources import parse_version as pv


def write(path, content):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except:
            pass
    open(path, 'wb').write(content)


def fetch_url(entry):
    path, uri = entry
    if not os.path.exists(path):
        r = urllib.request.urlopen(uri).read()
        write(path, r)
        return uri
    else:
        return path


def extract_awb(args):
    fp, output = args
    with open(fp, "rb") as f:
        n = struct.unpack('<I', f.read(4))[0]
        file_dict = {}
        for i in range(n):
            path_size = int.from_bytes(f.read(1), "little")
            file_size = int.from_bytes(f.read(4), "little")
            file_path = f.read(path_size).decode("utf-8")
            file_dict[file_path] = file_size
        for path, size in file_dict.items():
            write(os.path.join(output, path), f.read(size))
    return fp, output


def main():
    parser = ArgumentParser(
        description='Download and extract external .awb assets')
    parser.add_argument(dest="output",
                        help="Extracted Data Destination (MUST BE A FOLDER)", metavar="OUTPUT")
    parser.add_argument("-r", "--region", dest="region", default="CN",
                        help="Choose the region of the assets (EN/CN), default: CN", metavar="REGION",
                        choices=["EN", "CN"])
    parser.add_argument("-t", "--test",
                        action="store_true", dest="test", default=False,
                        help="Test mode, only download 3 files.")
    options = parser.parse_args()

    url = {
        "CN": "http://c.dal.heitao2014.com/dal/ext_assets/release_android/",
        "EN": "http://c-dal-en.heitaoglobal.com/dal_eng/ext_assets/release_android/"
    }
    url = url[options.region]

    content = urllib.request.urlopen(url).read().decode("utf-8")
    stripped = re.sub('<[^<]+?>', '', content)

    # getting highest version ext_assets
    ver = re.findall(r"(\d.+)\/", stripped)
    ver_pv = [pv(i) for i in ver]
    ver = ver[ver_pv.index(max(ver_pv))]

    # get the file list
    extlist = posixpath.join(ver, "extlist.json")
    filelist = json.loads(urllib.request.urlopen(
        urllib.parse.urljoin(url, extlist)).read().decode("utf-8"))
    urls = [(os.path.join(options.output, "dl_tmp", f"{f}.awb"), urllib.parse.urljoin(
        url, posixpath.join(ver, f"{f}.awb"))) for f in filelist]
    if options.test:
        urls = urls[:3]

    # download external assets
    results = ThreadPool(16).imap_unordered(fetch_url, urls)
    for i in results:
        print(f"Downloaded {i}")

    # extract awb files
    file_list = []
    for root, _, files in os.walk(os.path.join(options.output, "dl_tmp")):
        for name in files:
            file_list.append((os.path.join(root, name), options.output))
    results = ThreadPool(16).imap_unordered(extract_awb, file_list)
    for i, j in results:
        print(f"Extracted {i} to {j}")

    # delete tmp download folder
    rmtree(os.path.join(options.output, "dl_tmp"))


if __name__ == "__main__":
    main()
