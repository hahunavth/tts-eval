#!/usr/bin/env python3
"""Generate HTML forms for AXY test."""

from jinja2 import FileSystemLoader, Environment
import json
import argparse

def render_html(config):
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("axy_test.html.jinja2")

    assert config
    html = template.render(
        form_url="https://script.google.com/macros/s/AKfycbwoHjEpHLsf-h5Bd4axFzQjLWN2MeJcv728LN8A-3TAssnSq4VnLXDggI2L2LdWEAR63w/exec",  # Replace with your form URL
        questions=config["questions"],
        form_id=config["form_id"],
    )
    print(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help='<Required> AXY Test Configuration JSON', required=True)
    args = parser.parse_args()
    
    cfg = None
    if args.config:
        with open(args.config) as f:
            cfg = json.load(f)
    render_html(cfg)
