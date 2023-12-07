import os
import shutil
import argparse
import random
import json

from sympy import EX


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--title", help='<Required> Audio dir', required=True)
    parser.add_argument("-a", "--audio_dirs", nargs='+', help='<Required> Audio dir', required=True)
    parser.add_argument("-c", "--clean", help='Clean wav dir',  action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    
    out_audio_dir = "./wavs"
    max_file_per_exp=8
    symmetry = True
    
    if args.clean:
        print("Clean wavs folder!")
        shutil.rmtree(out_audio_dir)
    
    os.makedirs(out_audio_dir, exist_ok=True)
    
    print("Audio dirs: ")
    audio_dirs = args.audio_dirs
    n_files = None
    for idx, d in enumerate(audio_dirs):
        files = os.listdir(d)
        files = [f for f in files if f.endswith(".wav")]
        assert len(files) != 0, d + " does not contain .wav files!" 
        assert not n_files or len(files) == n_files
        if symmetry:
            n_files = len(files)
        print(f"\tDir: {d}: {len(files)} files")
    
    selected = range(1, n_files)
    if symmetry and max_file_per_exp < n_files:
        selected = random.sample(selected, max_file_per_exp)
    
    print("Copying...")
    for idx, d in enumerate(audio_dirs):
        files = os.listdir(d)
        for fid in selected:
            f = files[fid]
            shutil.copyfile(os.path.join(d, f), os.path.join(out_audio_dir, f"ID{idx}_{f}"))
    
    print("Create config")
    audios = os.listdir(out_audio_dir)
    random.shuffle(audios)
    try:
        last_form_id = len(os.listdir("./configs"))
    except Exception:
        last_form_id = 1
    form_id = last_form_id+1
    out_cfg = {"page_title": args.title, "form_id": form_id, "questions": []}
    for idx, audio in enumerate(audios):
        name = f"q{idx+1}" # audio.replace(".wav", "")
        audio_path = os.path.join(out_audio_dir, audio)
        title = f"Câu hỏi {idx+1}"
        out_cfg['questions'].append({
            "name": name,
            "audio_path": audio_path,
            "title": title
        })
    
    print("Id: ", out_cfg['form_id'])
    print("N question: ", len(out_cfg["questions"]))
    
    os.makedirs("./configs", exist_ok=True)
    with open(os.path.join("./configs", f"{form_id}.json"), "w") as f:
        f.write(json.dumps(out_cfg, indent=4))
    