#!/usr/bin/env python3
"""Generate forms for human evaluation."""

from jinja2 import FileSystemLoader, Environment


def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mos.html.jinja2")

    html = template.render(
        page_title="MOS Test 1",
        form_url="https://script.google.com/macros/s/AKfycbwRj5-lIESg3zj8dDgaYRsupOfmUnHhyKvgph1Y5HfqbLYdosSehDZvB-q01o15EGbIKw/exec",
        form_id=1,
        questions=[
            {
                "title": "Câu hỏi 1",
                "audio_path": "wavs/test1.wav",
                "name": "q1"
            },
            {
                "title": "Câu hỏi 2",
                "audio_path": "wavs/test2.wav",
                "name": "q2"
            },
        ]
    )
    print(html)


if __name__ == "__main__":
    main()
