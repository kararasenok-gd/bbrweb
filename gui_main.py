import PySimpleGUI as sg
import requests
import re
from bs4 import BeautifulSoup

def create_layout():
    return [
        [sg.Input(size=(30, 1), default_text="findex.wtc", key="INPUT"), sg.Button("Go")],
        [sg.Column([], key="--OUTPUT--", scrollable=True, vertical_scroll_only=True, size=(400, 500))],
        [sg.Text("", key="--LINKS--", font=("Arial", 15, "underline"))],
    ]

layout = create_layout()

def execute_script(code):
    exec(code, globals())

def bbr_parse_line(line):
    if line.startswith('!<'):
        return f"<title>{line[2:].strip()}</title>"
    elif line.startswith('!_'):
        return f"<u>{line[2:].strip()}</u>"
    elif line.startswith('!!'):
        return f"<b>{line[2:].strip()}</b>"
    elif line.startswith('!/'):
        return f"<i>{line[2:].strip()}</i>"
    elif line.startswith('!col>'):
        match = re.match(r'!col>(.*)>>\s*(.*)', line)
        if match:
            color = match.group(1).strip()
            text = match.group(2).strip()
            
            if color == "purple":
                color = "h1"
            elif color == "blue":
                color = "h2"
            elif color == "cyan":
                color = "h3"
            elif color == "green":
                color = "h4"
            elif color == "orange":
                color = "h5"
            elif color == "red":
                color = "h6"
            elif color == "gray":
                color = "p"
            elif color == "white":
                color = "a"
            else:
                color = "footer"
            
            return f'<{color}>{text}</{color}>'
    elif line.startswith('!'):
        return f"<footer>{line[1:].strip()}</footer>"
    else:
        return line

def bbr_parse_text(text):
    lines = text.split('\n')
    parsed_lines = []

    for line in lines:
        if not line.startswith('!'):
            continue
        
        parsed_line = bbr_parse_line(line)
        parsed_lines.append(parsed_line)

    parslines = '\n'.join(parsed_lines)
    htmltemplete = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
[[CONTENT]]
</body>
</html>
    """
    
    parsed_html = htmltemplete.replace("[[CONTENT]]", parslines)
    
    return parsed_html

domain_url = "https://raw.githubusercontent.com/kararasenok-gd/bbrweb/main/domains.json"
cached_sites = requests.get(domain_url).json()

class TextColor:
    H1 = '#d670d6'
    H2 = '#3b8de8'
    H3 = '#27afd0'
    H4 = '#24d18b'
    H5 = '#eeee42'
    H6 = '#f04c4c'
    P = '#809090'
    A = '#e2e2e2'
    SPAN = '#808080'
    STRONG = '#ee4b4b'
    EM = '#28aaca'
    B = '#22be7f'
    I = '#e6e640'
    U = '#d56fd5'
    SMALL = '#7a7a7a'
    BLOCKQUOTE = '#27b0d1'
    PRE = '#e2e2e2'
    CODE = '#e2e2e2'
    ENDC = '#909090'

window = sg.Window(title="BebraWEB", layout=layout, finalize=True)

def update_window_with_content(content):
    window.extend_layout(window["--OUTPUT--"], content)
    window["--OUTPUT--"].contents_changed()

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    if event == "Go":
        found = False

        for i in cached_sites.get("domains"):
            if i["name"] + "." + i["tld"] == values["INPUT"]:
                found = True
                x_url = i["ip"]
                x_content = requests.get(x_url).text
                if x_url.endswith(".bbr"):
                    x_content = bbr_parse_text(x_content)
                window["--LINKS--"].update("")
                break

        if not found:
            # Change text in output
            window["--OUTPUT--"].update("Domain not found")
            continue

        soup = BeautifulSoup(x_content, 'html.parser')
        body = soup.find('body')

        color_mapping = {
            'h1': TextColor.H1,
            'h2': TextColor.H2,
            'h3': TextColor.H3,
            'h4': TextColor.H4,
            'h5': TextColor.H5,
            'h6': TextColor.H6,
            'p': TextColor.P,
            'a': TextColor.A,
            'span': TextColor.SPAN,
            'strong': TextColor.STRONG,
            'em': TextColor.EM,
            'b': TextColor.B,
            'i': TextColor.I,
            'u': TextColor.U,
            'small': TextColor.SMALL,
            'blockquote': TextColor.BLOCKQUOTE,
            'pre': TextColor.PRE,
            'code': TextColor.CODE,
            'footer': TextColor.ENDC
        }

        output_elements = []
        links = []
        title = soup.find('title').text + " - BBRWEB" if soup.find('title') else values["INPUT"] + " - BBRWEB"
        window.TKroot.title(title)

        for tag in body.find_all():
            tag_name = tag.name
            color = color_mapping.get(str(tag_name), TextColor.ENDC)
            if tag_name == "a" and tag.get("href"):
                output_elements.append([sg.Text(f"{tag.text} - {tag.get('href')}", text_color=color)])
            else:
                output_elements.append([sg.Text(tag.text, text_color=color)])

        # Clear the entire layout
        window.close()
        window = sg.Window(title="BebraWEB", layout=create_layout(), finalize=True)
        update_window_with_content(output_elements)
        window["--LINKS--"].update(links)

    for key in window.key_dict:
        if key.endswith("+CLICK+"):
            if event == key:
                link = key.split("+")[0]
                window["INPUT"].update(link)
                window.write_event_value("Go", None)

window.close()