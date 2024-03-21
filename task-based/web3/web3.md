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

8. Дальше дело за малым, копируем подходящий эксплоит с той же [статьи](https://book.hacktricks.xyz/generic-methodologies-and-resources/python/bypass-python-sandboxes)
9. Профит

![flag](https://github.com/artkegor/nto2024_writeups/blob/main/task-based/web3/web3-4.png)
