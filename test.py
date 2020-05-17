#!/usr/bin/env python3
import argparse
import tajava.reader.tale

p = argparse.ArgumentParser()
p.add_argument("tale_java_output")
args = p.parse_args()

data = tajava.reader.tale.load(args.tale_java_output)
for i_row, row in enumerate(data):
    print(
        '{}: row["simu"]["logE0"] = {:.3f}, row["recon"]["logE0"] = {:.3f}'.format(
            i_row,
            row["simu"]["logE0"],
            row["recon"]["logE0"]            
        )
    )
