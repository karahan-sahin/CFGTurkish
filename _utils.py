def import_grammar():
    return NotImplemented

def import_morphology():
    return NotImplemented

def import_lexicon():
    return NotImplemented


def dense_results(parse):
    constituents = []
    for c in range(len(parse.columns)):
        x = [list(x_1) for x_1 in parse.values[c] if x_1]
        constituents.extend([item for sublist in x for item in sublist])
    return constituents


def evaluation(y_pred, y_true, beta=1):
    """
    
    """
    y_pred = dense_results(y_pred)
    precision = len(set(y_pred).intersection(set(y_true))) / len(y_pred)
    recall = len(set(y_pred).intersection(set(y_true))) / len(y_true)
    f_measure = ((beta**2 + 1)*precision*recall) /  ((beta**2)*(precision+recall))

    return precision, recall, f_measure