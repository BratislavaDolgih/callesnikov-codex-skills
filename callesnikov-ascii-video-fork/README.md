# Callesnikov ASCII Video Fork

Это локальный AI-форк навыка для работы с ASCII-видео и ASCII-фотографиями из Codex.

## Структура

- `SKILL.md` - инструкция для Codex: когда использовать навык и какие команды запускать.
- `README.md` - человеческая инструкция для тебя.
- `repository/` - оригинальный клон `https://github.com/stepanussaruran/ASCII-Video-Player`.
- `fork/` - наши добавления поверх оригинала: конвертация фото, сохранение ASCII-файлов, цветной вывод, PowerShell-обёртка.

## Быстрый старт

Сначала поставь зависимости для форка:

```bash
cd "%USERPROFILE%\.codex\skills\callesnikov-ascii-video-fork\fork"
python -m pip install -r requirements.txt
```

Если нужен только ASCII для фотографий, обычно достаточно `numpy` и `pillow`. Для видео нужен `opencv-python`.

## Оригинальный видеоплеер

Оригинал лежит в `repository/` и запускается так:

```bash
cd "%USERPROFILE%\.codex\skills\callesnikov-ascii-video-fork\repository"
python ASCII_v4_ultimate.py "C:\path\video.mp4" --color --width 100
python ASCII_v4_ultimate.py "C:\path\video.mp4" --info
```

## Форк: фотографии в ASCII

Показать цветную фотографию в терминале:

```bash
cd "%USERPROFILE%\.codex\skills\callesnikov-ascii-video-fork\fork"
python ascii_media_tools.py image "C:\path\photo.jpg" --width 120 --color --print
```

Сохранить ASCII-текст:

```bash
python ascii_media_tools.py image "C:\path\photo.jpg" --width 120 --save-text "ascii_outputs\photo.txt"
```

Сохранить цветную ASCII-картинку:

```bash
python ascii_media_tools.py image "C:\path\photo.jpg" --width 140 --color --save-image "ascii_outputs\photo_ascii.png"
```

Сделать картинку ярче, контрастнее и насыщеннее:

```bash
python ascii_media_tools.py image "C:\path\photo.jpg" --width 140 --color --vivid --save-image "ascii_outputs\photo_ascii_vivid.png"
```

Более ручной “светящийся” вариант:

```bash
python ascii_media_tools.py image "C:\path\photo.jpg" --width 180 --color --brightness 1.2 --contrast 1.55 --saturation 2.1 --gamma 1.25 --glow 1.4 --save-image "ascii_outputs\photo_ascii_glow.png"
```

Задать точный размер итоговой картинки:

```bash
python ascii_media_tools.py image "C:\path\photo.jpg" --width 160 --output-size 1280x720 --color --save-image "ascii_outputs\photo_1280x720.png"
```

## Форк: видео в ASCII

Цветной предпросмотр в терминале:

```bash
python ascii_media_tools.py video "C:\path\video.mp4" --width 90 --color --preview
```

Сохранить цветное ASCII-видео:

```bash
python ascii_media_tools.py video "C:\path\video.mp4" --width 120 --color --save-video "ascii_outputs\video_ascii.mp4"
```

Сохранить более яркое ASCII-видео:

```bash
python ascii_media_tools.py video "C:\path\video.mp4" --width 120 --color --vivid --save-video "ascii_outputs\video_ascii_vivid.mp4"
```

Сохранить видео как набор текстовых ASCII-кадров:

```bash
python ascii_media_tools.py video "C:\path\video.mp4" --width 100 --save-frames "ascii_outputs\frames"
```

## Цвет в PowerShell

Цветной вывод возможен через ANSI 24-bit escape codes. Лучше всего он работает в Windows Terminal, PowerShell 7 или современном терминале VS Code. Старый классический `cmd.exe` и старые окна Windows PowerShell могут показывать escape-последовательности текстом или работать медленнее.

Для PowerShell добавлена обёртка:

```powershell
cd "%USERPROFILE%\.codex\skills\callesnikov-ascii-video-fork\fork"
.\run_color_preview.ps1 -InputPath "C:\path\photo.jpg" -Width 120
.\run_color_preview.ps1 -InputPath "C:\path\video.mp4" -Width 90
```

Внутри песочницы Codex можно генерировать цветные PNG/MP4 и ANSI-текст, но интерактивный цветной видеопросмотр зависит от того, как приложение показывает терминал. Надёжнее всего проверять живой цветной предпросмотр в обычном Windows Terminal.

## Java Swing-обёртка

Простой GUI лежит в `fork\java-swing`.

Что уже есть:

- кнопка выбора файла;
- кнопка обработки фотографии;
- кнопка обработки по натуральному размеру;
- кнопка внезапной остановки обработки;
- прогресс-бар обработки видео/фото;
- поле ширины ASCII;
- лог выполнения;
- запуск Python-скрипта `ascii_media_tools.py` под капотом;
- сохранение результата в `ascii_outputs\photo_ascii_yyyyMMdd_HHmmss.png`.

Кнопка `По натуральному размеру` сохраняет результат в исходном пиксельном размере файла. Для фото размер читается Java-приложением напрямую. Для видео размер читается через Python/OpenCV, поэтому для видео нужен `opencv-python`.

Важно: натуральный размер означает размер итогового PNG/MP4 в пикселях. Поле `Ширина ASCII` всё равно управляет детализацией ASCII-символов.

Во время видеообработки GUI показывает прогресс по кадрам. Кнопка `Остановить` завершает текущий Python-процесс; уже частично созданный видеофайл может остаться неполным.

Собрать JAR:

```powershell
cd "%USERPROFILE%\.codex\skills\callesnikov-ascii-video-fork\fork\java-swing"
.\build.ps1
```

Запустить GUI:

```powershell
.\run_gui.ps1
```

Для двойного клика проще всего использовать:

```text
%USERPROFILE%\.codex\skills\callesnikov-ascii-video-fork\fork\java-swing\run_gui.bat
```

Также можно открыть двойным кликом:

```text
%USERPROFILE%\.codex\skills\callesnikov-ascii-video-fork\fork\java-swing\dist\AsciiPhotoSwingApp.jar
```

Но двойной клик по `.jar` зависит от ассоциации Java в Windows. `.bat` обычно надёжнее.

Про JVM: JVM не вшивается внутрь JAR. Для приложения без установленной Java нужен `jpackage`, который собирает app-image с bundled runtime:

```powershell
cd "%USERPROFILE%\.codex\skills\callesnikov-ascii-video-fork\fork\java-swing"
.\package_windows.ps1
```

Если команда скажет, что `jpackage` не найден, установи полный JDK с `jpackage` и добавь его `bin` в PATH. На текущей машине видны `java` и `javac`, но `jpackage` может быть не доступен из PATH.

Важно: `jpackage` бандлит Java runtime, но не Python. GUI всё равно вызывает `ascii_media_tools.py`, поэтому Python и зависимости из `requirements.txt` должны быть доступны, либо следующим шагом нужно отдельно упаковывать Python-runtime.

## Как просить Codex

Примеры запросов:

```text
Используй $callesnikov-ascii-video-fork и сделай из C:\path\photo.jpg цветную ASCII-картинку шириной 140 символов, сохрани PNG.
```

```text
Используй $callesnikov-ascii-video-fork и сделай из C:\path\video.mp4 цветное ASCII-видео шириной 100 символов, сохрани MP4.
```

Codex сам выберет `repository/`, если нужен оригинальный плеер, и `fork/`, если нужна конвертация, сохранение или фото.
