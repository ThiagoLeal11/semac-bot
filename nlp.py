import re
import unidecode

'''Default structure is like
    {
        intent: "deploy or rollback",
        parameters: {type: "frontend"}
    }
'''

INTENTS = {
    'hi': ['oi', 'ola', 'opa', 'ha quanto tempo', 'fala ai', 'saudacoes', 'e ai', 'eae', 'salve'],
    'ruok': ['tudo bem', 'como voce esta', 'esta bem', 'joia', 'beleza', 'blz', 'tranquil', 'como ta', 'ce ta'],
    'exit': ['sair', 'exit', 'quit', 'leave', 'die', 'off',],
    'badword': ['put', 'cu', 'fud', 'pinto', 'caralho', 'buceta', 'pau', 'xereca', 'xota', 'bosta', 'porra', 'carai',
                'pica', 'merda', 'cacete', 'viado', 'desgraca', 'pqp', 'vsf', 'fdp', 'rola', 'piroca'],
    'deploy': ['deploy', 'sub', 'atualiz', 'carregu', 'uploud', 'up',],
    'roolback': ['volt', 'retorn', 'roolback', 'restaur', ],
    'view': ['qual', 'em que', 'atual', 'ultima']
}

PARAMETERS = {
    'type': {
        'frontend': ['front', 'frontend', 'front-end', 'site', ],
        'backend': ['back', 'backend', 'back-end', 'server', 'servidor', ]
    },
    'time': {
        'now': ['agora', 'ja', ]
    }
}


def clean_text(text):
    # Clean spaces
    text = re.sub(' +', ' ', text)
    # To lower
    text = text.lower()
    # Remove accents
    text = unidecode.unidecode(text)
    return text


def analyze_text(text, context):
    if not text:
        context['intent'] = 'none'
        context['parameters'] = {}
        return context

    text = clean_text(text)
    context['intent'] = intent_detector(text)
    context['parameters'] = parameters_detector(text)
    return context


def intent_detector(text):
    for key in INTENTS:
        for i in INTENTS[key]:
            if i in text:
                return key
    else:
        return 'none'


def parameters_detector(text):
    param = {}
    for key in PARAMETERS:
        for p in PARAMETERS[key]:
            for k in PARAMETERS[key][p]:
                if k in text:
                    param[key] = p
    return param