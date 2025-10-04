

def get_gpu_num(model_name):
    model_name = model_name.lower()
    kws = {
        8: ['65b', '70b'],
        4: ['30b', '33b', '35b', '40b'],
        2: ['13b', '14b', '20b', '8b'],
        1: ['6b', '7b', 'moss'],
    }
    for k in [8, 4, 2, 1]:
        for keyword in kws[k]:
            if keyword in model_name:
                return k
    return 8