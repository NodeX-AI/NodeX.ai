MODELS = {
    'grok4fast' : 'Grok 4 fast',
    'gpt5mini' : 'GPT-5 mini',
}

MODEL_DISPLAY_NAMES = {
    'grok4fast' : 'Grok 4 fast',
    'gpt5mini' : 'GPT-5 mini',
}

def get_model_display_name(model_alias: str) -> str:
    return MODEL_DISPLAY_NAMES.get(model_alias)