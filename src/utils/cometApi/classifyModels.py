from enum import Enum
from collections import defaultdict

class ModelsClasses(Enum):
    TEXTS = "textModels"
    IMAGES = "imagesModels"
    VIDEO = "videoModels",
    AUDIO = "audioModels",
    EDITIND = "editingModels",
    EMBENDS = "embendModels",
    OTHER = "otherModels",


def classify_model(model_id: str, owned_by: str) -> str:
    model_id_lower = model_id.lower()

    
    if any(kw in model_id_lower for kw in [
        "flux", "sdxl", "stable-diffusion", "dall-e", "ideogram", "recraft", "text_to_image",
        "text-to-image", "image-to-video", "t2i", "imagegen", "gpt-image", "mj_", "stability"
    ]):
        return ModelsClasses.IMAGES.value

    
    if any(kw in model_id_lower for kw in [
        "video", "sora", "runway", "kling", "luma", "veo", "seedance", "i2v", "t2v"
    ]):
        return ModelsClasses.VIDEO.value

    
    if any(kw in model_id_lower for kw in [
        "tts", "whisper", "audio", "music", "suno", "transcribe", "speech"
    ]):
        return  ModelsClasses.AUDIO.value

    
    if any(kw in model_id_lower for kw in [
        "edit", "erase", "enhance", "expand", "replace_background", "inpaint", "upscale"
    ]):
        return ModelsClasses.EDITIND.value

    
    if any(kw in model_id_lower for kw in [
        "embedding", "text-embedding", "bria_text_to_vector", "vector"
    ]):
        return ModelsClasses.EMBENDS.value

    
    if any(kw in model_id_lower for kw in [
        "chat", "gpt", "claude", "qwen", "gemini", "llama", "mistral", "mixtral", "deepseek",
        "glm", "o1", "o3", "o4", "grok", "minimax", "doubao", "kimi", "hunyuan", "spark", "moonshot"
    ]):
        return ModelsClasses.TEXTS.value

    
    return ModelsClasses.OTHER.value

def getClassifyModels(models: list[str]):
    grouped = defaultdict(lambda: defaultdict(list))

    for model in models:
        model_id = model["id"]
        owner = model.get("owned_by", "unknown")
        category = classify_model(model_id, owner)
        grouped[category][owner].append(model_id)

    return grouped
