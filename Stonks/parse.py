#!/usr/bin/python3

x = "0x9a16390_0x804b000_0x80489c3_0xf7f4fd80_0xffffffff_0x1_0x9a14160_0xf7f5d110_0xf7f4fdc7_(nil)_0x9a15180_0x1_0x9a16370_0x9a16390_0x6f636970_0x7b465443_0x306c5f49_0x345f7435_0x6d5f6c6c_0x306d5f79_0x5f79336e_0x62633763_0x65616336_0xffd3007d_0xf7f8aaf8_0xf7f5d440_0x2c391000_0x1_(nil)_0xf7decce9_"

x = x.replace("0x", "")
x = x.replace("_(nil)_", "")

s = ""
# parse to characters
for i in x.split('_'):
    # read hex 
    for k in range(0, len(i), 2):
        h = i[k:k+2]
        h = int(h, 16)
        s += chr(h)

s = s[46:]
# little endian flip packs of 4 chars
for i in range(0, len(s), 4):
    s = s[:i] + s[i:i+4][::-1] + s[i+4:]

print(s)