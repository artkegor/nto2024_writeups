# Решение Forensics-1 (Linux)
1. Для начала посмотрим логи. Один из интересующих нас - /var/log/nginx/access.log.1
2. Увидим что в нем много обращений к сервису Gitlab. Проверим его наличие в системе.
3. Дальше посмотрим историю пользователя и увидим там множество команд. Некоторые из них, например, по установке Gitlab.
> Ответ на вопрос №1 - Gitlab 15.2.2

![badlab](https://github.com/artkegor/nto2024_writeups/blob/main/forensics2/forensics2-3.png)

![badlab15.2.2](https://github.com/artkegor/nto2024_writeups/blob/main/forensics2/forensics2-4.png)

4. Так как хакер получил прямой доступ к управлению Linux-машиной и выполнению команд, то использовался RCE.
> Ответ на вопрос №2 - RCE
5. Посмотрим файл /root/.ssh/authorized_keys на предмет пользователей которые могут подключиться к серверу по SSH с помощью ключей и увидим там постороннего пользователя. 
> Ответ на вопрос №5 - amongus@debian оставил ключ в authorized_keys

![hugekeys](https://github.com/artkegor/nto2024_writeups/blob/main/forensics2/forensics2-6.png)

6. Посмотрим историю root'a в `.bash_history` и увидим там, что хакер удалял /tmp/linpeas.txt, это известный скрипт для поиска уязвимостей на Linux-серверах.
> Ответ на вопрос №6 - скрипт linpeas.sh

`rm -rf /tmp/linpeas.txt`

7. Также в истории можем увидеть jynx2, загуглив информацию про него мы понимаем, что это Root-Kit.
> Ответ на вопрос №7 - jynx2.so

![jynx2](https://github.com/artkegor/nto2024_writeups/blob/main/forensics2/forensics2-1.png)
