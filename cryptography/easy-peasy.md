---
description: OTP Challenge
---

# Easy Peasy

A one-time pad is unbreakable, but can you manage to recover the flag? (Wrap with picoCTF{}) `nc mercury.picoctf.net 20266` [otp.py](https://mercury.picoctf.net/static/84c434ada6e2f770b5000292cadae7eb/otp.py)

The solution here was to simply wrap over the key length and then output the key afterwards.

```python
from pwn import *

KEY_LEN = 50000
MAX_CHUNK = 10000

r = remote("mercury.picoctf.net", 20266)
r.recvuntil(b"This is the encrypted flag!\n")
flag = r.recvlineS(keepends = False)
log.info(f"Flag: {flag}")
bin_flag = unhex(flag)

counter = KEY_LEN - len(bin_flag)

with log.progress('Causing wrap-around') as p:
    while counter > 0:
        p.status(f"{counter} bytes left")
        chunk_size = min(MAX_CHUNK, counter)
        r.sendlineafter(b"What data would you like to encrypt? ", b'a' * chunk_size)
        
        counter -= chunk_size

r.sendlineafter(b"What data would you like to encrypt? ", bin_flag)
r.recvlineS()
log.success("The flag: {}".format(unhex(r.recvlineS())))
```
