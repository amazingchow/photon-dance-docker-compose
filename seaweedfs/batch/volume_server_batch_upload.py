# -*- coding: utf-8 -*-
import hashlib
import os
import ntpath
import requests


def md5sum(filepath):
    fd = open(filepath, "rb")
    h = hashlib.md5(fd.read())
    fd.close()
    return h.hexdigest()


def upload(filepath):
    r = requests.get("http://localhost:9333/dir/assign?collection=faces_image&ttl=90d")
    if r.status_code != 200:
        print("failed to assign {}, status code: {}".format(filepath, r.status_code))
    print(r.json())

    filename = ntpath.basename(filepath)
    multipart_form_data = {
        "file": (filename, open(filepath, "rb")),
    }
    r = requests.post(
        "http://127.0.0.1:8080/{}?ttl=90d".format(r.json()["fid"]),
        files=multipart_form_data,
        headers={"Seaweed-Etag": md5sum(filepath)},
    )
    if r.status_code == 201:
        print("upload {}".format(filepath))
    else:
        print("failed to upload {}, status code: {}".format(filepath, r.status_code))


if __name__ == "__main__":
    cwd = os.getcwd()
    for _ in range(10):
        for idx in range(1, 501):
            upload("{}/imgs/IT001_001_{:08}.jpg".format(cwd, idx))
