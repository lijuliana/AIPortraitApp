import replicate
import os
import uuid
import aiofiles
from typing import Dict, Any, Optional
from config import Config
from PIL import Image
import io
import zipfile
import tempfile
import asyncio
import signal
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import gc

class PortraitGenerationService:
    def __init__(self):
        self.config = Config()
        os.environ["REPLICATE_API_TOKEN"] = self.config.REPLICATE_API_TOKEN
    
    async def save_uploaded_image(self, image_content: bytes) -> str:
        """Save uploaded image and return the file path"""
        image_id = str(uuid.uuid4())
        temp_path = f"temp_{image_id}.jpg"
        
        async with aiofiles.open(temp_path, 'wb') as f:
            await f.write(image_content)
        
        return temp_path
    

    
    def get_prompt(self, style: str, custom_prompt: Optional[str] = None) -> str:
        """Get appropriate prompt based on style"""
        base_prompt = self.config.PROMPT_TEMPLATES.get(style, self.config.PROMPT_TEMPLATES["realistic"])
        if custom_prompt:
            # Concatenate template with custom prompt, separated by comma
            return f"{base_prompt}, {custom_prompt}"
        
        return base_prompt
    
    def get_negative_prompt(self, style: str, custom_negative: Optional[str] = None) -> str:
        """Get appropriate negative prompt based on style"""
        base_negative = self.config.NEGATIVE_PROMPT_TEMPLATES.get(style, self.config.NEGATIVE_PROMPT_TEMPLATES["default"])
        if custom_negative:
            # Concatenate template with custom negative prompt, separated by comma
            return f"{base_negative}, {custom_negative}"
        
        return base_negative
    
    async def generate_with_instantid(self, image_path: str, prompt: str, negative_prompt: str) -> Dict[str, Any]:
        """Generate portrait using InstantID model"""
        try:
            params = self.config.DEFAULT_PARAMS["instantid"].copy()
            print("[InstantID] About to call replicate.run() with params:", params)
            
            # Run replicate in a thread with timeout
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                def run_replicate():
                    with open(image_path, "rb") as img_file:
                        return replicate.run(
                            self.config.MODELS["instantid"]["model_id"],
                            input={
                                "image": img_file,
                                "width": 640,
                                "height": 640,
                                "prompt": prompt,
                                "negative_prompt": negative_prompt
                            }
                        )
                
                future = loop.run_in_executor(executor, run_replicate)
                output = await asyncio.wait_for(future, timeout=300)  # 5 minute timeout
            
            print("[InstantID] replicate.run() output:", output)
            print("[InstantID] Output type:", type(output))
            
            # Handle different output formats
            if hasattr(output, 'url'):
                # If it's a Replicate output object with .url() method
                image_url = output.url()
            elif isinstance(output, list) and len(output) > 0:
                image_url = str(output[0]).strip()
            elif isinstance(output, str):
                image_url = output.strip()
            else:
                # If it's a generator or other format, try to get the first item
                try:
                    image_url = list(output)[0] if hasattr(output, '__iter__') else str(output)
                except:
                    image_url = str(output)
            
            print("[InstantID] Final Image URL:", image_url)
            print("[InstantID] Image URL type:", type(image_url))
            print("[InstantID] Image URL length:", len(image_url))
            
            return {
                "image_url": image_url,
                "model_used": "InstantID",
                "model_description": self.config.MODELS["instantid"]["description"],
                "generation_id": str(uuid.uuid4())
            }
        except asyncio.TimeoutError:
            print("[InstantID] Timeout after 5 minutes!")
            raise Exception("InstantID generation timed out after 5 minutes")
        except Exception as e:
            print(f"[InstantID] Exception: {e}")
            raise Exception(f"InstantID generation failed: {str(e)}")
    

    
    async def generate_with_ipadapter(self, image_path: str, prompt: str, negative_prompt: str) -> Dict[str, Any]:
        """Generate portrait using IP-Adapter SDXL Face model"""
        try:
            params = self.config.DEFAULT_PARAMS["ipadapter"].copy()
            print("[IP-Adapter] About to call replicate.run() with params:", params)
            
            # Run replicate in a thread with timeout
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                def run_replicate():
                    with open(image_path, "rb") as img_file:
                        return replicate.run(
                            self.config.MODELS["ipadapter"]["model_id"],
                            input={
                                "image": img_file,
                                "prompt": prompt,
                                "negative_prompt": negative_prompt,
                                **params
                            }
                        )
                
                future = loop.run_in_executor(executor, run_replicate)
                output = await asyncio.wait_for(future, timeout=300)  # 5 minute timeout
            
            print("[IP-Adapter] replicate.run() output:", output)
            return {
                "image_url": output[0],
                "model_used": "IP-Adapter SDXL Face",
                "model_description": self.config.MODELS["ipadapter"]["description"],
                "generation_id": str(uuid.uuid4())
            }
        except asyncio.TimeoutError:
            print("[IP-Adapter] Timeout after 5 minutes!")
            raise Exception("IP-Adapter generation timed out after 5 minutes")
        except Exception as e:
            print(f"[IP-Adapter] Exception: {e}")
            raise Exception(f"IP-Adapter generation failed: {str(e)}")
    

    
    async def generate_with_instantid2(self, image_path: str, prompt: str, negative_prompt: str) -> Dict[str, Any]:
        """Generate portrait using InstantID MultiControlNet model"""
        try:
            params = self.config.DEFAULT_PARAMS["instantid2"].copy()
            print("[InstantID2] About to call replicate.run() with params:", params)
            
            # Run replicate in a thread with timeout
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                def run_replicate():
                    with open(image_path, "rb") as img_file:
                        return replicate.run(
                            self.config.MODELS["instantid2"]["model_id"],
                            input={
                                "face_image_path": img_file,
                                "width": 640,
                                "height": 640,
                                "prompt": prompt,
                                "negative_prompt": negative_prompt
                            }
                        )
                
                future = loop.run_in_executor(executor, run_replicate)
                output = await asyncio.wait_for(future, timeout=300)  # 5 minute timeout
            
            print("[InstantID2] replicate.run() output:", output)
            print("[InstantID2] Output type:", type(output))
            
            # Handle different output formats
            if hasattr(output, 'url'):
                # If it's a Replicate output object with .url() method
                image_url = output.url()
            elif isinstance(output, list) and len(output) > 0:
                image_url = str(output[0]).strip()
            elif isinstance(output, str):
                image_url = output.strip()
            else:
                # If it's a generator or other format, try to get the first item
                try:
                    image_url = list(output)[0] if hasattr(output, '__iter__') else str(output)
                except:
                    image_url = str(output)
            
            print("[InstantID2] Final Image URL:", image_url)
            print("[InstantID2] Image URL type:", type(image_url))
            print("[InstantID2] Image URL length:", len(image_url))
            
            if not image_url.startswith('http'):
                print("[InstantID2] Warning: URL doesn't start with http:", image_url)
            
            return {
                "image_url": image_url,
                "model_used": "InstantID MultiControlNet",
                "model_description": self.config.MODELS["instantid2"]["description"],
                "generation_id": str(uuid.uuid4())
            }
        except asyncio.TimeoutError:
            print("[InstantID2] Timeout after 5 minutes!")
            raise Exception("InstantID2 generation timed out after 5 minutes")
        except Exception as e:
            print(f"[InstantID2] Exception: {e}")
            print(f"[InstantID2] Exception type: {type(e).__name__}")
            print(f"[InstantID2] Full error details: {str(e)}")
            
            # Check if it's a network-related error
            if "nodename nor servname provided" in str(e) or "network" in str(e).lower():
                raise Exception(f"InstantID2 network error: This model requires additional network access that may not be available. Error: {str(e)}")
            else:
                raise Exception(f"InstantID2 generation failed: {str(e)}")
    
    async def generate_with_ipadapter2(self, image_path: str, prompt: str = "", negative_prompt: str = "") -> Dict[str, Any]:
        """Generate portrait using IP-Adapter Plus Face model"""
        try:
            params = self.config.DEFAULT_PARAMS["ipadapter2"].copy()
            print("[IP-Adapter2] About to call replicate.run() with params:", params)
            
            # Run replicate in a thread with timeout
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                def run_replicate():
                    with open(image_path, "rb") as img_file:
                        return replicate.run(
                            self.config.MODELS["ipadapter2"]["model_id"],
                            input={
                                "image": img_file,
                                "output_format": "png"
                            }
                        )
                
                future = loop.run_in_executor(executor, run_replicate)
                output = await asyncio.wait_for(future, timeout=300)  # 5 minute timeout
            
            print("[IP-Adapter2] replicate.run() output:", output)
            
            # Handle different output formats
            if isinstance(output, list) and len(output) > 0:
                image_url = output[0]
            elif isinstance(output, str):
                image_url = output
            else:
                # If it's a generator or other format, try to get the first item
                try:
                    image_url = list(output)[0] if hasattr(output, '__iter__') else str(output)
                except:
                    image_url = str(output)
            
            return {
                "image_url": image_url,
                "model_used": "IP-Adapter Plus Face",
                "model_description": self.config.MODELS["ipadapter2"]["description"],
                "generation_id": str(uuid.uuid4())
            }
        except asyncio.TimeoutError:
            print("[IP-Adapter2] Timeout after 5 minutes!")
            raise Exception("IP-Adapter2 generation timed out after 5 minutes")
        except Exception as e:
            print(f"[IP-Adapter2] Exception: {e}")
            raise Exception(f"IP-Adapter2 generation failed: {str(e)}")
    
    async def generate_portrait_runall(self, image_path: str, style: str = "realistic",
                                     custom_prompt: Optional[str] = None,
                                     custom_negative: Optional[str] = None) -> Dict[str, Any]:
        """Generate portraits using all models and select the best result"""
        try:
            # Get unified prompts for all models
            unified_prompt = self.get_prompt(style, custom_prompt)
            unified_negative_prompt = self.get_negative_prompt(style, custom_negative)
            
            print(f"[Run All] Using unified prompt: {unified_prompt}")
            print(f"[Run All] Using unified negative prompt: {unified_negative_prompt}")
            
            results = {}
            successful_models = 0
            total_models = 4  # We now have 4 models total
            
            # Generate with InstantID
            try:
                results["instantid"] = await self.generate_with_instantid(
                    image_path, unified_prompt, unified_negative_prompt
                )
                successful_models += 1
                print(f"[Run All] InstantID completed successfully ({successful_models}/{total_models})")
            except Exception as e:
                results["instantid"] = {"error": str(e)}
                print(f"[Run All] InstantID failed: {str(e)}")
            
            # Generate with IP-Adapter
            try:
                results["ipadapter"] = await self.generate_with_ipadapter(
                    image_path, unified_prompt, unified_negative_prompt
                )
                successful_models += 1
                print(f"[Run All] IP-Adapter completed successfully ({successful_models}/{total_models})")
            except Exception as e:
                results["ipadapter"] = {"error": str(e)}
                print(f"[Run All] IP-Adapter failed: {str(e)}")
            
            # Generate with InstantID2
            try:
                results["instantid2"] = await self.generate_with_instantid2(
                    image_path, unified_prompt, unified_negative_prompt
                )
                successful_models += 1
                print(f"[Run All] InstantID2 completed successfully ({successful_models}/{total_models})")
            except Exception as e:
                error_msg = str(e)
                if "network" in error_msg.lower() or "nodename" in error_msg.lower():
                    results["instantid2"] = {"error": "InstantID2 requires additional network access that is not available. Try using InstantID instead."}
                else:
                    results["instantid2"] = {"error": error_msg}
                print(f"[Run All] InstantID2 failed: {error_msg}")
            
            # Generate with IP-Adapter2
            try:
                results["ipadapter2"] = await self.generate_with_ipadapter2(
                    image_path, unified_prompt, unified_negative_prompt
                )
                successful_models += 1
                print(f"[Run All] IP-Adapter2 completed successfully ({successful_models}/{total_models})")
            except Exception as e:
                results["ipadapter2"] = {"error": str(e)}
                print(f"[Run All] IP-Adapter2 failed: {str(e)}")
            
            print(f"[Run All] Generation complete: {successful_models}/{total_models} models succeeded")
            
            # Check if we have at least one successful generation
            if successful_models == 0:
                raise Exception("All models failed to generate portraits. Please try again or check your input image.")
            
            # Select the best result
            best_result = self.select_best_result(results)
            if best_result:
                results["best"] = best_result
                print(f"[Run All] Selected best result: {best_result['model_used']}")
            
            return {
                "runall_results": results,
                "generation_id": str(uuid.uuid4()),
                "successful_models": successful_models,
                "total_models": total_models
            }
        except Exception as e:
            raise Exception(f"Run All generation failed: {str(e)}")
    
    def select_best_result(self, results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select the best result from all successful generations"""
        successful_results = []
        
        # Collect all successful results
        for model_name, result in results.items():
            if "error" not in result:
                successful_results.append((model_name, result))
        
        if not successful_results:
            return None
        
        # Simple selection algorithm - prioritize certain models
        # You can enhance this with image quality analysis later
        priority_order = ["instantid2", "instantid", "ipadapter", "ipadapter2"]
        
        # Try to find the highest priority successful model
        for priority_model in priority_order:
            for model_name, result in successful_results:
                if model_name == priority_model:
                    print(f"[Run All] Selected {model_name} as best result (priority-based selection)")
                    return result
        
        # If no priority model found, return the first successful result
        first_result = successful_results[0][1]
        print(f"[Run All] Selected {successful_results[0][0]} as best result (fallback selection)")
        return first_result
    
    def cleanup_temp_file(self, file_path: str):
        """Clean up temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass 