from pathlib import Path

class Paragraph:
    def __init__(self, text=""):
        self.text = text

class Document:
    def __init__(self, path=None):
        self.paragraphs = []
        if path and Path(path).exists():
            with open(path, 'r', encoding='utf-8') as f:
                for line in f.read().splitlines():
                    if line:
                        self.paragraphs.append(Paragraph(line))

    def add_paragraph(self, text):
        self.paragraphs.append(Paragraph(text))

    def save(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            for p in self.paragraphs:
                f.write(p.text + '\n')
