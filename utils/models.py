MODELS = {
    'grok4fast' : 'Grok 4 fast',
    'gpt5mini' : 'GPT-5 mini',
    'deepseekv32' : 'DeepSeek V3.2',
    'gemini3flashprev' : 'Gemini 3 Flash Preview',
}

OpenAI_API_Models = [
    'Grok 4 fast',
    'GPT-5 mini',
    'DeepSeek V3.2',
    'Gemini 3 Flash Preview',
]

MODEL_DISPLAY_NAMES = {
    'grok4fast' : 'Grok 4 fast',
    'gpt5mini' : 'GPT-5 mini',
    'deepseekv32' : 'DeepSeek V3.2',
    'gemini3flashprev' : 'Gemini 3 Flash Preview',
}

def get_model_display_name(model_alias: str) -> str:
    return MODEL_DISPLAY_NAMES.get(model_alias)