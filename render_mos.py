#!/usr/bin/env python3
"""Generate forms for human evaluation."""

from ast import arg
from jinja2 import FileSystemLoader, Environment


def main(cfg):
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mos.html.jinja2")

    assert cfg
    html = template.render(
        form_url="https://script.google.com/macros/s/AKfycbwRj5-lIESg3zj8dDgaYRsupOfmUnHhyKvgph1Y5HfqbLYdosSehDZvB-q01o15EGbIKw/exec",
        **cfg
    )
    print(html)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help='<Required> Config.json', required=True)
    args = parser.parse_args()
    
    cfg = None
    if args.config:
        import json
        f = open(args.config)
        cfg = json.load(f)
    main(cfg)
