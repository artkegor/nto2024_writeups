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
