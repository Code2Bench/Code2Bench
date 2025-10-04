

def group_sentences(corrected_srt, threshold=1.0):
    """按时间间隔分句"""
    if not corrected_srt:
        return []
    sentences = []
    current_sentence = [corrected_srt[0]]
    for i in range(1, len(corrected_srt)):
        prev_end = corrected_srt[i-1]["end"]
        curr_start = corrected_srt[i]["start"]
        if curr_start - prev_end > threshold:
            sentences.append(current_sentence)
            current_sentence = [corrected_srt[i]]
        else:
            current_sentence.append(corrected_srt[i])
    sentences.append(current_sentence)
    return sentences