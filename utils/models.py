MODELS = {
    'gemma' : 'google/gemma-3-27b-it:free',
    'deepseek' : 'tngtech/deepseek-r1t2-chimera:free',
    'minimax' : 'minimax/minimax-m2:free',
    'nemotron' : 'nvidia/nemotron-nano-9b-v2:free',
}

MODEL_DISPLAY_NAMES = {
    'gemma' : 'Gemma 3',
    'deepseek' : 'DeepSeek R1T2 Chimera',
    'minimax' : 'MiniMax M2',
    'nemotron' : 'Nemotron Nano 9B V2',
}

def get_model_display_name(model_alias: str) -> str:
    return MODEL_DISPLAY_NAMES.get(model_alias)