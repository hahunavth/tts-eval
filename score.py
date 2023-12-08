import numpy as np
from scipy import stats

def calculate_mos_confidence(scores):
    mean_scores = np.mean(scores, axis=1)  # Calculate mean scores across testers for each audio
    mean_mos = np.mean(mean_scores)  # Calculate overall mean MOS

    if len(mean_scores) > 1:
        confidence_interval = stats.t.interval(0.95, len(mean_scores) - 1, loc=mean_mos, scale=stats.sem(mean_scores))
        half_interval = (confidence_interval[1] - mean_mos)
    else:
        half_interval = 0
    return mean_mos, half_interval


if __name__ == "__main__":
    # Example usage
    test_scores = [
        [4.5, 4.2, 4.8, 4.0, 4.9],  # Tester 1 scores for different audios
        [3.7, 4.1, 3.9, 4.2, 3.8],  # Tester 2 scores for different audios
        [4.0, 4.3, 4.5, 3.9, 4.1]   # Tester 3 scores for different audios
    ]

    mean_mos, half_interval = calculate_mos_confidence(test_scores)

    print(f"MOS score: {mean_mos} +- {half_interval} with 95% confidence interval")
