import os
import shutil
import argparse
import random
import json
from itertools import chain


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create MOS configuration', usage='%(prog)s [-h] -t TITLE -a AUDIO_DIRS AUDIO_DIRS [-c | --clean | --no-clean] [-m MAX_FILE_PER_EXP]')
    parser.add_argument("-t", "--title", help='<Required> Form title', required=True)
    parser.add_argument("-a", "--audio_dirs", nargs=2, help='<Required> Experiment', metavar=('EXPERIMENT_NAME', 'AUDIO_DIRS'), action='append',required=True)
    parser.add_argument("-c", "--clean", help='Clean wav dir', action='store_true')
    parser.add_argument('--no-clean', dest='clean', action='store_false', help='Do not clean wav dir')
    parser.add_argument("-m", "--max_file_per_exp", help='Max file per experiment', type=int, default=8)
    args = parser.parse_args()
    
    print("Args: ")
    print(f"\tTitle: {args.title}")
    print("\tExperiments dirs: ")
    for idx, d in enumerate(args.audio_dirs):
        print(f"\t\t{d[0]}: {d[1]}")
    print(f"\tClean: {args.clean}")
    print(f"\tMax file per exp: {args.max_file_per_exp}")
    
    print()
    print("Creating...")
    
    out_audio_dir = "./wavs"
    out_cfg_dir = "./configs"
    max_file_per_exp=args.max_file_per_exp
    symmetry = True
    
    exp_dic = {e[0]: e[1] for e in args.audio_dirs}
    assert len(exp_dic.keys()) == len(args.audio_dirs), "Experiment name must be unique!"
    
    if args.clean and os.path.exists(out_audio_dir):
        print("Clean wavs folder!")
        shutil.rmtree(out_audio_dir)
    
    os.makedirs(out_audio_dir, exist_ok=True)
    
    print("Audio dirs: ")
    n_files = None
    for idx, exp_name in enumerate(exp_dic):
        d = exp_dic[exp_name]
        files = os.listdir(d)
        files = [f for f in files if f.endswith(".wav")]
        assert len(files) != 0, d + " does not contain .wav files!" 
        assert not n_files or len(files) == n_files
        if symmetry:
            n_files = len(files)
        print(f"\tExperiment: {exp_name}: {len(files)} files")
    
    selected = range(1, n_files)
    if symmetry and max_file_per_exp < n_files:
        selected = random.sample(selected, max_file_per_exp)
        selected = sorted(selected)
    qids = list(range(1, 2*len(selected)+1))
    random.shuffle(qids)
    
    print("Copying...")
    selected_dic = {}
    for d_idx, exp_name in enumerate(exp_dic):
        d = exp_dic[exp_name]
        files = os.listdir(d)
        for flid, fid in enumerate(selected):
            if flid == 0 and not os.path.exists(os.path.join(out_audio_dir, exp_name)):
                os.makedirs(os.path.join(out_audio_dir, exp_name), exist_ok=True)
            f = files[fid]
            if exp_name not in selected_dic:
                selected_dic[exp_name] = []
            new_fname = f"{exp_name}/{f}"
            selected_dic[exp_name].append({
                "_new_fpath": new_fname,
                "fname": f,
                "fid": fid,
                "qid": f"q{qids[d_idx * len(selected) + flid]}",
            })
            shutil.copyfile(os.path.join(d, f), os.path.join(out_audio_dir, new_fname))

    print("Create config")
    try:
        last_form_id = len(os.listdir(out_cfg_dir))
    except Exception:
        last_form_id = 1
    form_id = last_form_id+1
    out_cfg = {
        "page_title": args.title, 
        "form_id": form_id, 
        "questions": [],
        "_meta": {
            "max_file_per_exp": max_file_per_exp,
            "symmetry": symmetry,
            "experiments": exp_dic,
            "selected_dic": selected_dic
        }
    }
    for idx, dic in enumerate(sorted(list(chain.from_iterable(selected_dic.values())), key=lambda d: int(d['qid'].replace("q", "")))):
        audio = dic['_new_fpath']
        del dic['_new_fpath']
        dic = {k: v for k, v in dic.items() if k != "_new_fpath"}
        name = dic['qid']
        audio_path = os.path.join(out_audio_dir, audio)
        title = f"Câu hỏi {idx+1}"
        out_cfg['questions'].append({
            "name": name,
            "audio_path": audio_path,
            "title": title
        })
    
    print("Id: ", out_cfg['form_id'])
    print("N question: ", len(out_cfg["questions"]))
    
    os.makedirs(out_cfg_dir, exist_ok=True)
    with open(os.path.join(out_cfg_dir, f"{form_id}.json"), "w") as f:
        f.write(json.dumps(out_cfg, indent=4))
    
    print("Done!")