# Z80Links
Плагин для Sublime Text 2. Добавляет возможность перемещаться с помощью Ctrl + Click к исходным файлам ASM (z80) и прокручивать до места, где определена метка.

# Установка #
Просто скопируйте файлы в каталог Packages вашего Sublime Text 2:

    Sublime Text 2/Data/Packages/z80links/

После установки на верхней панели появится пункт меню Z80Links. 

# Использование #

Плагин использует кеш-файл «labelsList.json», расположенный в папке проекта, рядом с файлами «* .sublime-project» и «* .sublime-workspace».

Чтобы создать «labelList.json», в меню Z80Links выберете «Rebuild links». 

Эта операция выполняется один раз, после чего файл «labelsList.json» автоматически обновляется при сохранении файлов с расширением «*.asm». 

# Лицензия #

BSD 3-Clause "New" or "Revised" License

# Автор #

2021 © Written by breeze\fishbone crew

