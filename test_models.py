#!/usr/bin/env python3
"""
Test script to verify AI models are working
"""

import os
import replicate
from dotenv import load_dotenv
import requests

load_dotenv()

# Model slugs
IPADAPTER_SLUG = "lucataco/ip_adapter-sdxl-face:226c6bf67a75a129b0f978e518fed33e1fb13956e15761c1ac53c9d2f898c9af"
INSTANTID_SLUG = "tgohblio/instant-id-albedobase-xl:2a2afbff09996b53247b0714577d4ff82d2c9da8e8b00c5499b5b34510bb8b5e"
INSTANTID2_SLUG = "tgohblio/instant-id-multicontrolnet:35324a7df2397e6e57dfd8f4f9d2910425f5123109c8c3ed035e769aeff9ff3c"
IPADAPTER2_SLUG = "zsxkib/instant-id-ipadapter-plus-face:32402fb5c493d883aa6cf098ce3e4cc80f1fe6871f6ae7f632a8dbde01a3d161"



def test_instantid():
    print("\nTesting InstantID model...")
    try:
        from PIL import Image
        import io
        
        # Create a larger, more realistic test image
        img = Image.new('RGB', (512, 512), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=95)
        img_bytes.seek(0)
        
        print("[InstantID] About to call replicate.run()...")
        print(f"[InstantID] Model slug: {INSTANTID_SLUG}")
        
        # Try with minimal parameters first
        output = replicate.run(
            INSTANTID_SLUG,
            input={
                "image": img_bytes,
                "prompt": "portrait",
                "negative_prompt": "blurry"
            }
        )
        print("[InstantID] replicate.run() output:", output)
        print("✅ InstantID test passed!")
        print(f"Generated image: {output[0]}")
        return True

    except Exception as e:
        print(f"❌ InstantID test failed: {e}")
        print(f"[InstantID] Error details: {type(e).__name__}: {str(e)}")
        return False



def test_ipadapter():
    print("\nTesting IP-Adapter model...")
    try:
        from PIL import Image
        import io
        img = Image.new('RGB', (100, 100), color='green')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        print("[IP-Adapter] About to call replicate.run()...")
        output = replicate.run(
            IPADAPTER_SLUG,
            input={
                "image": img_bytes,
                "prompt": "A professional portrait photograph",
                "negative_prompt": "blurry, low quality",
                "num_inference_steps": 20,
                "guidance_scale": 7.5,
                "seed": 42
            }
        )
        print("[IP-Adapter] replicate.run() output:", output)
        print("✅ IP-Adapter test passed!")
        print(f"Generated image: {output[0]}")
        return True

    except Exception as e:
        print(f"❌ IP-Adapter test failed: {e}")
        return False

def test_instantid2():
    print("\nTesting InstantID2 model...")
    try:
        from PIL import Image
        import io
        
        # Create a larger, more realistic test image
        img = Image.new('RGB', (512, 512), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=95)
        img_bytes.seek(0)
        
        print("[InstantID2] About to call replicate.run()...")
        print(f"[InstantID2] Model slug: {INSTANTID2_SLUG}")
        
        # Try with minimal parameters first
        output = replicate.run(
            INSTANTID2_SLUG,
            input={
                "face_image_path": img_bytes,
                "prompt": "portrait",
                "negative_prompt": "blurry"
            }
        )
        print("[InstantID2] replicate.run() output:", output)
        print("✅ InstantID2 test passed!")
        print(f"Generated image: {output[0]}")
        return True

    except Exception as e:
        print(f"❌ InstantID2 test failed: {e}")
        print(f"[InstantID2] Error details: {type(e).__name__}: {str(e)}")
        return False

def test_ipadapter2():
    print("\nTesting IP-Adapter2 model...")
    try:
        from PIL import Image
        import io
        img = Image.new('RGB', (100, 100), color='orange')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        print("[IP-Adapter2] About to call replicate.run()...")
        output = replicate.run(
            IPADAPTER2_SLUG,
            input={
                "image": img_bytes,
                "output_format": "png"
            }
        )
        print("[IP-Adapter2] replicate.run() output:", output)
        print("✅ IP-Adapter2 test passed!")
        print(f"Generated image: {output[0]}")
        return True

    except Exception as e:
        print(f"❌ IP-Adapter2 test failed: {e}")
        return False

def main():
    print("🧪 Testing AI Models")
    print("=" * 40)
    token = os.getenv("REPLICATE_API_TOKEN")
    if not token or token == "your-replicate-api-token-here":
        print("❌ Please set your REPLICATE_API_TOKEN in the .env file")
        return
    results = []
    results.append(test_instantid())
    results.append(test_ipadapter())
    results.append(test_instantid2())
    results.append(test_ipadapter2())
    print("\n" + "=" * 40)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} models working")
    if passed == total:
        print("🎉 All models are working correctly!")
    elif passed > 0:
        print("⚠️  Some models are working. The app will use fallbacks.")
    else:
        print("❌ No models are working. Please check your API token and internet connection.")

if __name__ == "__main__":
    main() 