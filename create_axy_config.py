import os
import shutil
import argparse
import random
import json

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create AXY Test Configuration')
    parser.add_argument("-t", "--title", help='<Required> Form title', required=True)
    parser.add_argument("-a", "--audio_A", help='Directory containing Audio A (Ground Truth)', required=True)
    parser.add_argument("-x", "--audio_X", help='Directory containing Audio X (Experiment 1)', required=True)
    parser.add_argument("-y", "--audio_Y", help='Directory containing Audio Y (Experiment 2)', required=True)
    parser.add_argument("-n", "--num_questions", type=int, default=5, help='Number of questions for the test')
    args = parser.parse_args()
    
    print("Title: ", args.title)
    print("Audio A (Ground Truth): ", args.audio_A)
    print("Audio X (Experiment 1): ", args.audio_X)
    print("Audio Y (Experiment 2): ", args.audio_Y)
    print("Number of questions: ", args.num_questions)

    out_audio_dir = "./wavs"
    out_cfg_dir = "./configs"

    os.makedirs(out_audio_dir, exist_ok=True)
    
    # Creating configuration dictionary
    out_cfg = {
        "page_title": args.title, 
        "questions": []
    }

    # Generating multiple questions
    for i in range(args.num_questions):
        question = {
            "name": f"q{i + 1}",
            "audio_A": os.path.join(args.audio_A, f"audio_A_{i + 1}.wav"),
            "audio_X": os.path.join(args.audio_X, f"audio_X_{i + 1}.wav"),
            "audio_Y": os.path.join(args.audio_Y, f"audio_Y_{i + 1}.wav"),
            "title": f"Comparison Test {i + 1}"
        }
        out_cfg["questions"].append(question)

    # Write configuration to a JSON file
    os.makedirs(out_cfg_dir, exist_ok=True)
    with open(os.path.join(out_cfg_dir, "axy_test.json"), "w") as f:
        f.write(json.dumps(out_cfg, indent=4))
    
    print(f"{args.num_questions} AXY Test configurations created successfully.")
