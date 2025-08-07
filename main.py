import os
import replicate
import requests
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import aiofiles
import uuid
from PIL import Image
import io
import json
import os
from portrait_service import PortraitGenerationService
from config import Config

app = FastAPI(title="AI Portrait Generator", description="Generate realistic portraits using SOTA AI models")

# Initialize services
portrait_service = PortraitGenerationService()
config = Config()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

class PortraitRequest(BaseModel):
    style: str = "realistic"
    prompt: Optional[str] = None
    negative_prompt: Optional[str] = None

class PortraitResponse(BaseModel):
    image_url: str
    model_used: str
    generation_id: str

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main frontend page"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
            <head><title>AI Portrait Generator</title></head>
            <body>
                <h1>AI Portrait Generator API</h1>
                <p>Frontend not found. Please ensure static/index.html exists.</p>
                <p>API endpoints are available at:</p>
                <ul>
                    <li><a href="/docs">/docs</a> - API Documentation</li>
                    <li><a href="/models">/models</a> - Available Models</li>
                </ul>
            </body>
        </html>
        """)

@app.post("/generate-portrait-instantid", response_model=PortraitResponse)
async def generate_portrait_instantid(
    reference_image: UploadFile = File(...),
    style: str = Form("realistic"),
    prompt: Optional[str] = Form(None),
    negative_prompt: Optional[str] = Form(None)
):
    """Generate a realistic portrait using the uploaded reference image with InstantID"""
    
    temp_path = None
    try:
        # Save uploaded image
        content = await reference_image.read()
        temp_path = await portrait_service.save_uploaded_image(content)
        
        # Generate portrait using InstantID
        unified_prompt = portrait_service.get_prompt(style, prompt)
        unified_negative_prompt = portrait_service.get_negative_prompt(style, negative_prompt)
        
        result = await portrait_service.generate_with_instantid(
            temp_path, 
            unified_prompt, 
            unified_negative_prompt
        )
        
        return PortraitResponse(
            image_url=result["image_url"],
            model_used=result["model_used"],
            generation_id=result["generation_id"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
    finally:
        if temp_path:
            portrait_service.cleanup_temp_file(temp_path)



@app.post("/generate-portrait-runall")
async def generate_portrait_runall(
    reference_image: UploadFile = File(...),
    style: str = Form("realistic"),
    prompt: Optional[str] = Form(None),
    negative_prompt: Optional[str] = Form(None)
):
    """Generate portraits using all models and select the best result"""
    
    temp_path = None
    try:
        # Save uploaded image
        content = await reference_image.read()
        temp_path = await portrait_service.save_uploaded_image(content)
        
        # Generate portraits using all models and select best
        result = await portrait_service.generate_portrait_runall(
            temp_path, 
            style, 
            prompt, 
            negative_prompt
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Run All generation failed: {str(e)}")
    finally:
        if temp_path:
            portrait_service.cleanup_temp_file(temp_path)

@app.post("/generate-portrait-ipadapter", response_model=PortraitResponse)
async def generate_portrait_ipadapter(
    reference_image: UploadFile = File(...),
    style: str = Form("realistic"),
    prompt: Optional[str] = Form(None),
    negative_prompt: Optional[str] = Form(None)
):
    """Generate portrait using IP-Adapter FaceID model"""
    temp_path = None
    try:
        # Save uploaded image
        content = await reference_image.read()
        temp_path = await portrait_service.save_uploaded_image(content)
        # Generate portrait using IP-Adapter
        unified_prompt = portrait_service.get_prompt(style, prompt)
        unified_negative_prompt = portrait_service.get_negative_prompt(style, negative_prompt)
        
        result = await portrait_service.generate_with_ipadapter(
            temp_path,
            unified_prompt,
            unified_negative_prompt
        )
        return PortraitResponse(
            image_url=result["image_url"],
            model_used=result["model_used"],
            generation_id=result["generation_id"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
    finally:
        if temp_path:
            portrait_service.cleanup_temp_file(temp_path)

@app.post("/generate-portrait-instantid2", response_model=PortraitResponse)
async def generate_portrait_instantid2(
    reference_image: UploadFile = File(...),
    style: str = Form("realistic"),
    prompt: Optional[str] = Form(None),
    negative_prompt: Optional[str] = Form(None)
):
    """Generate portrait using InstantID MultiControlNet model"""
    temp_path = None
    try:
        # Save uploaded image
        content = await reference_image.read()
        temp_path = await portrait_service.save_uploaded_image(content)
        # Generate portrait using InstantID2
        unified_prompt = portrait_service.get_prompt(style, prompt)
        unified_negative_prompt = portrait_service.get_negative_prompt(style, negative_prompt)
        
        result = await portrait_service.generate_with_instantid2(
            temp_path,
            unified_prompt,
            unified_negative_prompt
        )
        
        print(f"[API] InstantID2 result:")
        print(f"[API] Image URL: {result['image_url']}")
        print(f"[API] Model Used: {result['model_used']}")
        print(f"[API] Generation ID: {result['generation_id']}")
        
        return PortraitResponse(
            image_url=result["image_url"],
            model_used=result["model_used"],
            generation_id=result["generation_id"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
    finally:
        if temp_path:
            portrait_service.cleanup_temp_file(temp_path)

@app.post("/generate-portrait-ipadapter2", response_model=PortraitResponse)
async def generate_portrait_ipadapter2(
    reference_image: UploadFile = File(...),
    style: str = Form("realistic"),
    prompt: Optional[str] = Form(None),
    negative_prompt: Optional[str] = Form(None)
):
    """Generate portrait using IP-Adapter Plus Face model"""
    temp_path = None
    try:
        # Save uploaded image
        content = await reference_image.read()
        temp_path = await portrait_service.save_uploaded_image(content)
        # Generate portrait using IP-Adapter2
        unified_prompt = portrait_service.get_prompt(style, prompt)
        unified_negative_prompt = portrait_service.get_negative_prompt(style, negative_prompt)
        
        result = await portrait_service.generate_with_ipadapter2(
            temp_path,
            unified_prompt,
            unified_negative_prompt
        )
        return PortraitResponse(
            image_url=result["image_url"],
            model_used=result["model_used"],
            generation_id=result["generation_id"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
    finally:
        if temp_path:
            portrait_service.cleanup_temp_file(temp_path)

@app.get("/models")
async def get_available_models():
    """Get information about available models"""
    return {
        "models": config.MODELS,
        "styles": list(config.PROMPT_TEMPLATES.keys()),
        "default_params": config.DEFAULT_PARAMS
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)