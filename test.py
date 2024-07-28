import re

def execute_script(code):
    exec(code, globals())

def parse_line(line):
    if line.startswith('!>'):
        script_content = line[2:].strip()
        return f"<pre><code>{script_content}</code></pre>"  # Для показа скрипта в HTML формате
    elif line.startswith('!_'):
        return f"<u>{line[2:].strip()}</u>"
    elif line.startswith('!!'):
        return f"<b>{line[2:].strip()}</b>"
    elif line.startswith('!/'):
        return f"<i>{line[2:].strip()}</i>"
    elif line.startswith('!col>#'):
        match = re.match(r'!col>#([0-9a-fA-F]+)>>\s*(.*)', line)
        if match:
            color = match.group(1)
            text = match.group(2)
            return f'<span style="color:#{color}">{text}</span>'
    elif line.startswith('!'):
        return line[1:].strip()
    else:
        return line

def parse_text(text):
    lines = text.split('\n')
    parsed_lines = []

    for line in lines:
        if not line.startswith('!'):
            continue  # Игнорирование комментариев
        if line.startswith('!>'):
            script_content = line[2:].strip()
            execute_script(script_content)  # Выполнение скрипта
        else:
            parsed_lines.append(parse_line(line))

    return '\n'.join(parsed_lines)

# Пример использования
input_text = """
! обычный
!/ курсив
!! жирный
!_ подчёркнутый
!> print("Hello from script!")
!col>#0000ff>> цветной текст (синий)
комментарий :3 (не отображается)
"""
parsed_text = parse_text(input_text)
print(parsed_text)