[![Check code style](https://github.com/JetBrains-Research/formal-lang-course/actions/workflows/code_style.yml/badge.svg)](https://github.com/JetBrains-Research/formal-lang-course/actions/workflows/code_style.yml)
[![Code style](https://img.shields.io/badge/Code%20style-black-000000.svg)](https://github.com/psf/black)
---
# Formal Language Course

Курс по формальным языкам: шаблон структуры репозитория для выполнения домашних работ,
а также материалы курса и другая сопутствующая информация.

Актуальное:
- [Таблица с текущими результатами](https://docs.google.com/spreadsheets/d/1IXeAhVb_cRRQf0UwHjw2AeBqNwpcY-XcnVs3-t9HBYc/edit#gid=0)
- [Список задач](https://github.com/JetBrains-Research/formal-lang-course/tree/main/tasks)
- [Стиль кода как референс](https://www.python.org/dev/peps/pep-0008/)
- [Материалы по курсу](https://github.com/JetBrains-Research/formal-lang-course/blob/main/docs/lecture_notes/Formal_language_course.pdf)
- [О достижимости с ограничениями в терминах формальных языков](https://github.com/JetBrains-Research/FormalLanguageConstrainedReachability-LectureNotes)

Технологии:
- Python 3.8+
- Pytest для unit тестирования
- GitHub Actions для CI
- Google Colab для постановки и оформления экспериментов
- Сторонние пакеты из `requirements.txt` файла
- Английский язык для документации или самодокументирующийся код

## Работа с проектом

- Для выполнения домашних практических работ необходимо сделать **приватный** `fork` этого репозитория к себе в `GitHub`.
- Рекомендуется установить [`pre-commit`](https://pre-commit.com/#install) для поддержания проекта в адекватном состоянии.
  - Установить `pre-commit` можно выполнив следующую команду в корне вашего проекта:
    ```shell
    pre-commit install
    ```
  - Отформатировать код в соответствии с принятым стилем можно выполнив следующую команду в корне вашего проекта:
    ```shell
    pre-commit run --all-files
    ```
- Ссылка на свой `fork` репозитория размещается в [таблице](https://docs.google.com/spreadsheets/d/1IXeAhVb_cRRQf0UwHjw2AeBqNwpcY-XcnVs3-t9HBYc/edit#gid=0) курса с результатами.
- В свой репозиторий необходимо добавить проверяющих с `admin` правами на чтение, редактирование и проверку `pull-request`'ов.

## Домашние практические работы

### Дедлайны

- **мягкий**: воскресенье 23:59
- **жёсткий**: среда 23:59

### Выполнение домашнего задания

- Каждое домашнее задание выполняется в отдельной ветке. Ветка должна иметь осмысленное консистентное название.
- При выполнении домашнего задания в новой ветке необходимо открыть соответствующий `pull-request` в `main` вашего `fork`.
- `Pull-request` снабдить понятным названием и описанием с соответствующими пунктами прогресса.
- Проверка заданий осуществляется посредством `review` вашего `pull-request`.
- Как только вы считаете, что задание выполнено, вы можете запросить `review` у проверяющего.
  - Если `review` запрошено **до мягкого дедлайна**, то вам гарантированна дополнительная проверка (до жёсткого дедлайна), позволяющая исправить замечания до наступления жёсткого дедлайна.
  - Если `review` запрошено **после мягкого дедлайна**, но **до жесткого дедлайна**, задание будет проверено, но нет гарантий, что вы успеете его исправить.
- Когда проверка будет пройдена, и задание **зачтено**, его необходимо `merge` в `main` вашего `fork`.
- Результаты выполненных заданий будут повторно использоваться в последующих домашних работах.

### Опциональные домашние задания
Часть задач, связанных с работой с GPGPU, будет помечена как опциональная. Это означает что и без их выполнения (при идеальном выполнении остальных задач) можно набрать полный балл за курс.

### Получение оценки за домашнюю работу

- Если ваша работа **зачтена** _до_ **жёсткого дедлайна**, то вы получаете **полный балл за домашнюю работу**.
- Если ваша работа **зачтена** _после_ **жёсткого дедлайна**, то вы получаете **половину полного балла за домашнюю работу**.
  - Если ревью было запрошено _до_ **жёсткого дедлайна** и задача зачтена сразу без замечаний, то вы всё ещё получаете **полный балл за домашнюю работу**.

## Код

- Исходный код практических задач по программированию размещайте в папке `project`.
- Файлам и модулям даем осмысленные имена, в соответствии с официально принятым стилем.
- Структурируем код, используем как классы, так и отдельно оформленные функции. Чем понятнее код, тем быстрее его проверять и тем больше у вас будет шансов получить полный балл.

## Тесты

- Тесты для домашних заданий размещайте в папке `tests`.
- Формат именования файлов с тестами `test_[какой модуль\класс\функцию тестирует].py`.
- Для работы с тестами рекомендуется использовать [`pytest`](https://docs.pytest.org/en/6.2.x/).
- Для запуска тестов необходимо из корня проекта выполнить следующую команду:
  ```shell
  python ./scripts/run_tests.py
  ```

## Эксперименты

- Для выполнения экспериментов потребуется не только код, но окружение и некоторая его настройка.
- Эксперименты должны быть воспроизводимыми (например, проверяющими).
- Эксперимент (настройка, замеры, результаты, анализ результатов) оформляется как Python-ноутбук, который публикуется на GitHub.
  - В качестве окружения для экспериментов с GPGPU (опциональные задачи) можно использовать [`Google Colab`](https://research.google.com/colaboratory/) ноутбуки. Для его создания требуется только учетная запись `Google`.
  - В `Google Colab` ноутбуке выполняется вся настройка, пишется код для экспериментов, подготовки отчетов и графиков.

## Структура репозитория

```text
.
├── .github - файлы для настройки CI и проверок
├── docs - текстовые документы и материалы по курсу
├── project - исходный код домашних работ
├── scripts - вспомогательные скрипты для автоматизации разработки
├── tasks - файлы с описанием домашних заданий
├── tests - директория для unit-тестов домашних работ
├── README.md - основная информация о проекте
└── requirements.txt - зависимости для настройки репозитория
```

## Контакты

- Семен Григорьев [@gsvgit](https://github.com/gsvgit)
- Егор Орачев [@EgorOrachyov](https://github.com/EgorOrachyov)
- Вадим Абзалов [@vdshk](https://github.com/vdshk)
- Рустам Азимов [@rustam-azimov](https://github.com/rustam-azimov)
- Екатерина Шеметова [@katyacyfra](https://github.com/katyacyfra)

## Язык запросов к графам

### Описание абстрактного синтаксиса языка

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Graph of graph
  | Labels of labels
  | Vertices of vertices
  | Edges of edges

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход

lambda = Lambda of List<var> * expr
```

### Конкретный синтаксис
```
prog --> (stmt)*

stmt -->
    var '=' expr ';'
  | 'print ' expr ';'

var --> initial_letter string
initial_letter --> '_' | char
char --> [a-z] | [A-Z]
string --> (initial_letter | '/' | '.' | int)*
int --> [1-9] [0-9]* | 0
bool --> 'true' | 'false'

expr -->
    '(' expr ')'
  | var
  | val
  | map
  | filter
  | intersect
  | concat
  | union
  | star

val -->
    '(' val ')'
  | '"' string '"'
  | int
  | bool
  | graph
  | labels
  | vertices
  | edges

graph -->
    'set_start' '(' vertices, graph ')'
  | 'set_final' '(' vertices, graph ')'
  | 'add_start' '(' vertices, graph ')'
  | 'add_final' '(' vertices, graph ')'
  | 'load_graph' '(' path ')'

path --> '"' string '"'

vertices -->
    'get_start' '(' graph ')'
  | 'get_final' '(' graph ')'
  | 'get_reachable' '(' graph ')'
  | 'get_vertices' '(' graph ')'
  | set

labels --> 'get_labels' '(' graph ')' | set

edges --> 'get_edges' '(' graph ')' | set

set --> '{' expr (',' expr)* } | 'set()' | '{' ( '(' int, (val | var), int ')' )* '}'

lambda --> 'fun' '(' var ')' '{' expr '}'
map --> 'map' '(' lambda ',' expr ')'
filter --> 'filter' '(' lambda ',' expr ')'

intersert --> 'intersect' '(' expr ',' expr ')' | expr '&' expr
concat --> 'concat' '(' expr ',' expr ')' | expr '.' expr
union --> 'union' '(' expr ',' expr ')' | expr '|' expr
star --> '(' expr ')' '*'
```
### Пример скриптов
1. Загрузка графа
2. Получение финальных вершин в переменную `vertices`
3. Назначение стартовыми всех вершин
4. Печать `vertices`
5. Печать меток обновленного графа
```
graph = load_graph("p/a/t/h");
vertices = get_final(graph);
graph_upd = set_start(get_vertices(graph), graph);
print vertices;
print get_labels(graph_upd);
```
1. Загрузка графа
2. Получение всех ребер графа
3. Назначение финальными вершинами стартовые
4. Печать финальных вершин
5. Печать ребер
```
graph = load_graph("p/a/t/h/2");
edges = get_edges(graph);
graph_upd = set_final(get_start(graph), graph);
print get_final(graph_upd);
print edges;
```
1. Регулярный запрос
2. Регулярный запрос, использующий предыдущий
3. печать конкатенации используемых регулярных запросов
```
a = "A" | "a";
b_a = ("b" | a)*;
print concat (a, b_a);
```
