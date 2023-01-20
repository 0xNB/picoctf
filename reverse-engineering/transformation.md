---
description: Transformation of Hidden Data
---

# 🕵 Transformation

We are initially given a binary with the content that can be seen below. We also received a hint about the function that was used to generate this data blob. The hint is `''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])`, so basically two characters from the _flag_ String are taken, added together and converted to a Unicode character.

```
00000000: e781 a9e6 8daf e48d 94e4 99bb e384 b6e5  ................
00000010: bda2 e6a5 b4e7 8d9f e6a5 aee7 8db4 e38c  ................
00000020: b4e6 919f e6bd a6e5 bcb8 e5bc b2e3 98b6  ................
00000030: e3a0 b4e6 8cb2 e381 bd                   .........
```

The solution to this problem is to reverse this function and re-generate the initial flag string. We see that the result is a concatenation of Unicode chars, so splitting the string character by character and then transforming those characters into their original ASCII characters should work. This can be seen in our implementation below.

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
