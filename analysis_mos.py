import os
import shutil
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import Dict
from score import calculate_mos_confidence
import argparse


def load_config(file_path):
    try:
        with open(file_path) as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}.")
        return None

parser = argparse.ArgumentParser(description='Load configuration from a JSON file')
parser.add_argument('file_path', metavar='FILE_PATH', type=str, help='Path to the JSON configuration file')

args = parser.parse_args()
config = load_config(args.file_path)
print("Form:\t", config['page_title'])
print("Id:\t", config['form_id'])

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet_url = "https://docs.google.com/spreadsheets/d/1P9GaXH36mT-lMgnpMs1RaifGgYTiPQNqAXFlXqFJfDU"
sheet = client.open_by_url(sheet_url)
worksheet = sheet.get_worksheet(0)

titles = worksheet.row_values(1)
answers = []
for i in range(2, 1000):
    values = worksheet.row_values(i)
    if not values:
        break
    
    assert len(values) >= len(titles)
    
    answer = {key: value for key, value in zip(titles, values)}
    if int(answer['exp_id']) != config['form_id']:
        continue
    
    answer['answers'] = [int(o) for o in values[len(titles):]]
    
    model_score_qid_dic = {}
    model_score_fid_dic = {}
    answer['scores'] = {key: [] for key in config['_meta']['experiments']}
    for exp_name in config['_meta']['experiments']:
        d = config['_meta']['experiments'][exp_name]
        model_score_qid_dic[exp_name] = {}
        model_score_fid_dic[exp_name] = {}
        for fobj in config['_meta']['selected_dic'][exp_name]:
            idx = int(fobj['qid'].replace('q', '')) - 1
            model_score_qid_dic[exp_name][fobj['qid']] = answer['answers'][idx]
            model_score_fid_dic[exp_name][str(fobj['fid'])] = answer['answers'][idx]
        model_score_list = [v for k, v in sorted(model_score_fid_dic[exp_name].items(), key=lambda x: int(x[0]))]
        answer['scores'][exp_name].append(model_score_list)
    # print(answer['scores'])
    
    print("Score:")
    for exp_name in config['_meta']['experiments']:
        d = config['_meta']['experiments'][exp_name]
        model_score_mat = answer['scores'][exp_name]
        score, half_interval = calculate_mos_confidence(model_score_mat)
        print("\t", exp_name, ":\t", score, "+-", half_interval)