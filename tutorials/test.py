#!/usr/bin/env python3
import tajava.reader.fd.simple1
import tajava.reader.fd.simple2
import tajava.reader.fd.tubeinfo

simple1_data = tajava.reader.fd.simple1.load("fdrecon_result_simple1.dat", mode="hybrid")
simple2_data = tajava.reader.fd.simple2.load("fdrecon_result_simple2.dat")

pmt_info = tajava.reader.fd.tubeinfo.load("tubeInfo_talemono.dat")
