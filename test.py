#!/usr/bin/env python3
import argparse
import tale_java

p = argparse.ArgumentParser()
p.add_argument("tale_java_output") # 位置引数fooを定義
args = p.parse_args()

data = tale_java.load(args.tale_java_output)
for i_row, row in enumerate(data):
    print(f'{i_row}: {row["simu"]["logE0"] = :.3f}, {row["recon"]["logE0"] = :.3f}')
