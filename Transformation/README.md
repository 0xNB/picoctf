---
description: Transformation of Hidden Data
---

# 🕵 Transformation

We are initially given a binary with the content that can be seen below and a hint for a transformation function. This transformation function probably resulted in Unicode content below

```
00000000: e781 a9e6 8daf e48d 94e4 99bb e384 b6e5  ................
00000010: bda2 e6a5 b4e7 8d9f e6a5 aee7 8db4 e38c  ................
00000020: b4e6 919f e6bd a6e5 bcb8 e5bc b2e3 98b6  ................
00000030: e3a0 b4e6 8cb2 e381 bd                   .........
```

Now we get the ordinals of our characters and just have to transform the result back to its char variant byte by byte.

We are given the transformatoin function `''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])` and just solve with the reverse function then that looks like this, so basically we read the unicode characters and transform their code points back into two separater characters.

```python
with open("enc", "r" ) as f:
    fc = f.read()
    flag = ""
    for i in range(0, len(fc), 1):
        print(fc[i])
        first_char = chr((ord(fc[i]) >> 8))
        second_char = chr(ord(fc[i]) & 0xff)
        flag += first_char + second_char
    print(flag)
```

Giving us the flag `picoCTF{16_bits_inst34d_of_8_26684c20}`!
