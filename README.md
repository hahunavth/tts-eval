# An Online Human Evaluation Form Template

This online form template functions like [Google Forms](https://www.google.com/forms/about/) but is more customizable.
Please feel free to use this as a template to create your own online human evaluation form.

### Usage

1. On GitHub:
    - Using this repository as template, generate your own public or private repository.
    - Go to *settings* and enable GitHub Pages.
2. On Google Drive:
    - Create a Google Spreadsheet and copy its ID from its URL:
        ```
        https://docs.google.com/spreadsheets/d/{YOUR_SPREADSHEET_ID}/edit
        ```
    - Create a Google Apps Script from **app.gs** and fill in `YOUR_SPREADSHEET_ID` you just copied.
    - Customize the script to meet your need and deploy it as a Web App (Allow *anyone, even anonymous* to access the Web App).
3. Locally:
    - Clone the repository you just created from the template.
    - Take a look at **templates** directory and several rendered HTMLs there as example.
    - Modify **render_mos.py** or **render_pair_comparison.py** and generate HTMLs.
    - Commit and push all the modifications back to GitHub.


### Run

```
python create_mos_config.py -a /kaggle/repo/output/infer/vlsp2023emo/12-05-EXP14-emofs2+shuffle_ref_mel+without_aug-120k /kaggle/repo/output/infer/vlsp2023emo/12-07-EXP17_multi_speaker_move_emo_enc_819177ad/GiangOi -c -t test_create_test
python render_mos.py -c ./configs/1.json > mos_test_1.html
```

### Bug
- Web player giang oi