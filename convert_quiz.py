import genanki, random
from markdown import markdown

def create_anki_package(name: str, num: int) -> None:
    # convert markdown code to html: str -> str
    def convert_markdown(md: str) -> str:
        return markdown(md, extensions=[
            'extra', 'admonition', 'codehilite', 'meta', 'nl2br', 'sane_lists', 'smarty', 'wikilinks'
        ])

    # convert markdown file to html: str -> str
    def load_markdown(filename: str) -> str:
        with open(filename, 'rb') as f:
            return convert_markdown(f.read().decode('utf-8'))

    # Anki Deck
    deck = genanki.Deck(
        random.randrange(1 << 30, 1 << 31), # 任意のデッキIDを振る
        '基本情報技術者試験' # デッキ名
    )

    # Anki Model: Card Stylings
    model = genanki.Model(
        random.randrange(1 << 30, 1 << 31), # 任意のモデルIDを振る
        '基本情報技術者試験', # モデル名
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ]
    )

    # add Anki cards
    for i in range(1, num + 1):
        dir = './{:s}/{:03d}'.format(name, i)
        q = load_markdown(f'{dir}/q.md') # 質問
        a = load_markdown(f'{dir}/a.md') # 解答
        print(dir, q)
        note = genanki.Note(
            model=model,
            fields=[q, a]
        )
        deck.add_note(note)

    # generate Anki Deck to Package
    pkg = genanki.Package(deck)
    pkg.write_to_file(f'{name}.apkg')

create_anki_package('quiz', 200)
create_anki_package('casl2', 3)
