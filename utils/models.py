MODELS = {
    'gemma' : 'google/gemma-3-27b-it:free',
    'deepseek' : 'tngtech/deepseek-r1t2-chimera:free',
    'nemotron' : 'nvidia/nemotron-nano-9b-v2:free',
    'grok4fast' : 'Grok 4 fast',
    'gpt5mini' : 'GPT-5 mini',
}

MODEL_DISPLAY_NAMES = {
    'gemma' : 'Gemma 3',
    'deepseek' : 'DeepSeek R1T2 Chimera',
    'nemotron' : 'Nemotron Nano 9B V2',
    'grok4fast' : 'Grok 4 fast',
    'gpt5mini' : 'GPT-5 mini',
}

def get_model_display_name(model_alias: str) -> str:
    return MODEL_DISPLAY_NAMES.get(model_alias)