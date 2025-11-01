MODELS = {
    'gemma' : 'google/gemma-3-27b-it:free',
    'deepseek' : 'tngtech/deepseek-r1t2-chimera:free',
}

MODEL_DISPLAY_NAMES = {
    'gemma' : 'Gemma 3',
    'deepseek' : 'DeepSeek R1T2 Chimera',
}

def get_model_display_name(model_alias: str) -> str:
    return MODEL_DISPLAY_NAMES.get(model_alias)