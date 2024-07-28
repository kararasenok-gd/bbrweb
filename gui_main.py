import PySimpleGUI as sg
import requests, json
from bs4 import BeautifulSoup

layout = [
    [sg.Input(size=(30, 1), default_text="findex.wtc"), sg.Button("Go")],
    [sg.Text(key="--OUTPUT--")],
]

domain_url = "https://raw.githubusercontent.com/kararasenok-gd/bbrweb/main/domains.json"
cached_sites = requests.get(domain_url).json()

class TextColor:
    H1 = '\033[95m'
    H2 = '\033[94m'
    H3 = '\033[96m'
    H4 = '\033[92m'
    H5 = '\033[93m'
    H6 = '\033[91m'
    P = '\033[0m'
    A = '\033[0m'
    SPAN = '\033[0m'
    STRONG = '\033[0m'
    EM = '\033[0m'
    B = '\033[0m'
    I = '\033[0m'
    U = '\033[0m'
    SMALL = '\033[0m'
    BLOCKQUOTE = '\033[0m'
    PRE = '\033[0m'
    CODE = '\033[0m'
    ENDC = '\033[0m'

window = sg.Window(title="BebraWEB", layout=layout)

while True:
    event, values = window.Read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    if event == "Go":
        found = False

        for i in cached_sites.get("domains"):
            if i["name"] + "." + i["tld"] == values[0]:
                found = True
                x_url = i["ip"]
                x_content = requests.get(x_url).text
                break
            
        if not found:
            # Change text in output
            window["--OUTPUT--"].update("Domain not found")
            quit()

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
        }

        output_text = ""
        for tag in body.find_all():
            tag_name = tag.name
            # color = color_mapping.get(tag_name, TextColor.ENDC)
            if tag_name == "a" and tag.get("href"):
                if event == "a":
                    window["INPUT"].Update(tag.get("href"))
            output_text += str(tag) + '\n'

        window["--OUTPUT--"].update(output_text)

window.Close()

