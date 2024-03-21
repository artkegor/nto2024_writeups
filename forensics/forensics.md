1. Прочитав легенду, понимаем, что скорее всего ПО попало на компьютер через фишинговое письмо.
2. Rambler в истории браузера подтверждает нашу догадку.
> Ответ на вопрос №1 - фишинговое письмо

![mail](https://github.com/artkegor/nto2024_writeups/blob/main/forensics/forensics6.png)

3. Переходим в системные логи Windows, а именно в PowerShell. Пролистав чуть ниже находим подозрительное скачивание, а именно Rjomba.exe. Тут же и злосчастный IP.
> Ответ на вопрос №2 - 95.169.192.220:8080

![ip](https://github.com/artkegor/nto2024_writeups/blob/main/forensics/forensics1.png)

4. Источник вируса - фишинговое письмо, поэтому будем искать возможные дампы emailов.
5. Находим в `C:\Users\Evgeniy\AppData\Local\Microsoft\Outlook` ost-дамп почты.
6. В браузере открываем первый попавшийся восстановитель ost-файлов и получим pst-файл.
7. Найдя любой pst-viewer получаем письма.
8. В одном из писем находим прикрепленный rar-файл. Закидываем его в Virus Total.
9. Отчет VirusTotal не оставляет сомнений, перед нами зараженный файл, с довольно свежей уязвимостью.
> Ответ на вопрос №3 - CVE-2023-38831 (WinRAR)

![cve](https://github.com/artkegor/nto2024_writeups/blob/main/forensics/forensics2.png)

10. Через поиск находим ранее скачанный Rjomba.exe. Запускаем ghidra и приступаем к анализу.
11. В интернете находим [статью](https://anti-debug.checkpoint.com/techniques/misc.html) с типичными способами обойти Windows Debug. Через поиск в Ghidra просматриваем все указанные в статье функции.
12. Обнаруживаем те самые функции в нашем вирусе.
> Ответ на вопрос №4 - IsDebuggerPresent, CheckRemoteDebuggerPresent (winapi)

![badfuncs](https://github.com/artkegor/nto2024_writeups/blob/main/forensics/forensics3.png)

13. Следующий вопрос по теме криптографии, поэтому скачиваем для Ghidra модуль FindCrypto.
14. Находим несколько криптографических функций, одна из них - AES Encryption, а в ней же переменная на 32 символа: `undefined (**ppauVar2) [32];`. Мы имеем дело с AES-256 CBC.
> Ответ на вопрос №5 - AES-256 CBC

![cryptofuncs](https://github.com/artkegor/nto2024_writeups/blob/main/forensics/forensics4.png)

15. Заканчиваем работу с Ghidra и скидываем наш файл на VirusTotal. Начинаем изучать отчет.
16. В разделе Behavior находим связи с `api.telegram.org`. Вирус взаимодействует с Telegram-ботом.
> Ответ на вопрос №7 - в Telegram-бот

![telegramisimposter](https://github.com/artkegor/nto2024_writeups/blob/main/forensics/forensics5.png)

17. Переходим к самой интересной части. А именно нахождению ключей и расшифровке файла на рабочем столе.
18. Для этого запускаем x64dbg на рабочем столе Windows.
19. Итерируем несколько десятков шагов и создаем дампы памяти.

![hardestpart](https://github.com/artkegor/nto2024_writeups/blob/main/forensics/forensics7.png)

20. Проходимся по дампам и обнаруживаем ключ от IV и AES.
21. В интернете ищем любой AES-decoder, где и получаем финальный ответ.
> Ответ на вопрос №6 - amogusamogusamogusamogusamogusam

> Ответ на вопрос №8 - sFYZ#2z9VdUR9sm`3JRz

![gg](https://github.com/artkegor/nto2024_writeups/blob/main/forensics/forensics8.png)

