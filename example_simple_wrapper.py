#!python3
# -*- coding:utf-8 -*-
###
# File: \simple_wrapper.py
# Project: test
# Created Date: 2022-03-29, 01:26:21
# Author: Siwei Chen <me@chensiwei.space>
# -----
# Copyright (c) 2022
#
# There is nothing right in my left brain and nothing left in my right brain.
# ----------	---	----------------------------------------------------------
###
from libnienet import EnetLib


class GPIBENET:
    def __init__(self, host, addr) -> None:
        self.l = EnetLib(host)
        self.ud = self.l.ibdev(pad=addr, sad=0, tmo=10, eot=1, eos=0)

    def write(self, s):
        self.l.ibwrt(self.ud, s)

    def read(self):
        status, resp = self.l.ibrd(self.ud, 4096)
        return resp

    def query(self, s):
        self.write(s)
        return self.read()


if __name__ == "__main__":
    d = GPIBENET("192.168.3.2", 16)
    d.query(b"*IDN?").decode()
    import IPython
    IPython.embed()