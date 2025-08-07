import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Replicate API Configuration
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "your-replicate-api-token-here")
    
    # Model configurations
    MODELS = {

        "ipadapter": {
            "model_id": "lucataco/ip_adapter-sdxl-face:226c6bf67a75a129b0f978e518fed33e1fb13956e15761c1ac53c9d2f898c9af",
            "description": "Style-aware portrait generation with IP-Adapter SDXL Face"
        },
        "instantid": {
            "model_id": "tgohblio/instant-id-albedobase-xl:2a2afbff09996b53247b0714577d4ff82d2c9da8e8b00c5499b5b34510bb8b5e",
            "description": "Identity-preserving portrait generation with AlbedoBase XL"
        },
        "instantid2": {
            "model_id": "tgohblio/instant-id-multicontrolnet:35324a7df2397e6e57dfd8f4f9d2910425f5123109c8c3ed035e769aeff9ff3c",
            "description": "Advanced identity preservation with MultiControlNet"
        },
        "ipadapter2": {
            "model_id": "zsxkib/instant-id-ipadapter-plus-face:32402fb5c493d883aa6cf098ce3e4cc80f1fe6871f6ae7f632a8dbde01a3d161",
            "description": "Enhanced IP-Adapter with improved face preservation"
        }
    }
    
    # Default generation parameters
    DEFAULT_PARAMS = {

        "ipadapter": {
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "seed": 42
        },
        "instantid": {
            # "style_strength_ratio": 20,
            # "reference_strength": 0.8,
            # "num_steps": 30,
            # "guidance_scale": 5,
            # "seed": 42
        },
        "instantid2": {
            # Only takes face_image_path
            # No additional parameters needed
        },
        "ipadapter2": {
            # Only takes image
            # No additional parameters needed
        }
    }
    
    # Prompt templates
    PROMPT_TEMPLATES = {
        "realistic": "A high-quality portrait, professional photography, sharp focus, detailed facial features, natural lighting",
        "artistic": "An artistic portrait, creative composition, beautiful lighting, professional photography",
        "professional": "A professional headshot, business attire, clean background, corporate photography",
        "casual": "A casual portrait, natural expression, everyday setting, candid photography"
    }
    
    # Negative prompt templates
    NEGATIVE_PROMPT_TEMPLATES = {
        "default": "blurry, low quality, distorted, deformed, cartoon, anime, painting, drawing",
        "realistic": "blurry, low quality, distorted, deformed, cartoon, anime, painting, drawing, artificial",
        "professional": "blurry, low quality, distorted, deformed, cartoon, anime, casual, informal"
    } 