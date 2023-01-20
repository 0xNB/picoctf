# Problem Definition

I decided to try something noone else has before. I made a bot to automatically trade stonks for me using AI and machine learning. I wouldn't believe you if you told me it's unsecure! [vuln.c](https://mercury.picoctf.net/static/fdf270d959fa5231e180e2bd11421d0c/vuln.c) `nc mercury.picoctf.net 16439`

# Solution

When we examine the program with a code editor we see that it's using the unsafe version of `printf` when getting the users' authorization token.

With the unsafe version of `printf` we can then dump content of the binary and execute code.