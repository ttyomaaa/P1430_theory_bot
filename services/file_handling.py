BOOK_PATH = 'book/book.txt'

book: dict[int, dict[int, str]] = {}

def prepare_book(path = BOOK_PATH) -> None:
    with open(path, "r", encoding='UTF-8') as f:
        text = f.readlines()

    curr_line = ''
    prev_line = ''
    page = 1
    chapter = 0
    text = text[1:]
    for line in text:
        #line.lstrip()
        #print(book,chapter,page, list(curr_line), list(prev_line), list(line))
        if (prev_line == '\n') and line == '\n':
            chapter += 1
            page = 1
            book[chapter] = {}
        else:
            if line == '\n' and curr_line != '':
                book[chapter][page] = curr_line
                curr_line = ''
                page += 1
            else:
                if curr_line != '':
                    curr_line = '\n'.join([curr_line, line])
                else:
                    curr_line += line
        prev_line = line
    book[chapter][page] = curr_line

prepare_book(BOOK_PATH)


PAGE_SIZE = 1050
# Функция, возвращающая строку с текстом страницы и ее размер
# def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
#     signs = ['!', '?', '.', ',', ':', ';']
#     last = min(len(text) - 1, start + size - 1)
#     for i in range(last, start - 1, -1):
#         if text[i] in signs and (i == (len(text) -1) or text[i + 1] not in signs):
#             return text[start: i + 1], i - start + 1


# Функция, формирующая словарь книги
# def prepare_book(path: str) -> None:
#     with open(path, "r", encoding='UTF-8') as f:
#         text = f.read()
#     start = 0
#     last = len(text) - 1
#     n_page = 1
#     count = 0
#     while start < last and count < 20:
#         count += 1
#         page, n_signs = _get_part_text(text=text, start=start, size=PAGE_SIZE)
#         start += n_signs
#         book[n_page] = page.lstrip()
#         n_page += 1

# Вызов функции prepare_book для подготовки книги из текстового файла
#prepare_book(BOOK_PATH)