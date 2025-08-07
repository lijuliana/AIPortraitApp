# AI Portrait Generator Backend

A powerful FastAPI backend that generates realistic portraits using state-of-the-art AI models from Replicate.com. This application leverages multiple SOTA models including InstantID, IP-Adapter, InstantID2, and IP-Adapter2 for high-quality portrait generation.

## Features

- **Multiple SOTA Models**: Support for InstantID, IP-Adapter, InstantID2, IP-Adapter2, and more
- **Style Control**: Pre-defined styles (realistic, artistic, professional, casual)
- **Custom Prompts**: Full control over generation prompts and negative prompts
- **Ensemble Generation**: Compare results from multiple models simultaneously
- **Beautiful Frontend**: Modern, responsive web interface with drag-and-drop upload
- **RESTful API**: Clean FastAPI endpoints with automatic documentation
- **Error Handling**: Robust error handling and temporary file cleanup

## Models Used

### 1. InstantID
- **Model**: `tencentarc/instantid`
- **Best for**: High-quality portrait generation with identity preservation
- **Use case**: When you have a reference image and want to maintain facial identity

### 2. IP-Adapter
- **Model**: `lucataco/ip_adapter-sdxl-face`
- **Best for**: Style-aware portrait generation with face preservation
- **Use case**: When you want to maintain facial features while applying different styles

### 3. InstantID2 (MultiControlNet)
- **Model**: `tgohblio/instant-id-multicontrolnet`
- **Best for**: Advanced identity preservation with MultiControlNet
- **Use case**: When you need enhanced identity preservation capabilities

### 5. IP-Adapter2 (Plus Face)
- **Model**: `zsxkib/instant-id-ipadapter-plus-face`
- **Best for**: Enhanced IP-Adapter with improved face preservation
- **Use case**: When you want better face preservation with style transfer

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
REPLICATE_API_TOKEN=your-replicate-api-token-here
```

Get your Replicate API token from [replicate.com](https://replicate.com).

### 3. Run the Application

#### Option 1: Using the launcher (Recommended)
```bash
python run.py
```

#### Option 2: Direct execution
```bash
python main.py
```

#### Option 3: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at:
- **Frontend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Endpoints**: http://localhost:8000/models

## API Endpoints

### 1. Generate Portrait with InstantID
```http
POST /generate-portrait-instantid
```
Upload a reference image to generate a portrait using InstantID model.

### 2. Generate Portrait with IP-Adapter
```http
POST /generate-portrait-ipadapter
```
Upload a reference image to generate a style-aware portrait with face preservation.

### 3. Generate Portrait with InstantID2
```http
POST /generate-portrait-instantid2
```
Upload a reference image to generate a portrait using InstantID MultiControlNet.

### 5. Generate Portrait with IP-Adapter2
```http
POST /generate-portrait-ipadapter2
```
Upload a reference image to generate a portrait using IP-Adapter Plus Face.

### 5. Generate Portrait with All Models
```http
POST /generate-portrait-runall
```
Generate portraits using all models and select the best result.

### 5. Get Available Models
```http
GET /models
```
Get information about available models and styles.

## Usage Examples

### Using cURL

#### Generate Portrait with InstantID
```bash
curl -X POST "http://localhost:8000/generate-portrait" \
  -H "Content-Type: multipart/form-data" \
  -F "reference_image=@path/to/your/image.jpg" \
  -F 'request={"style": "realistic", "prompt": "A professional portrait"}'
```

#### Generate Portrait with SDXL
```bash
curl -X POST "http://localhost:8000/generate-portrait-sdxl" \
  -H "Content-Type: application/json" \
  -d '{"style": "professional", "prompt": "A stunning business portrait"}'
```

### Using Python

```python
import requests

# Generate portrait with InstantID
with open('reference_image.jpg', 'rb') as f:
    files = {'reference_image': f}
    data = {
        'request': '{"style": "realistic", "prompt": "A professional portrait"}'
    }
    response = requests.post('http://localhost:8000/generate-portrait', 
                           files=files, data=data)
    result = response.json()
    print(f"Generated image: {result['image_url']}")
```

## Available Styles

- **realistic**: High-quality portrait with natural lighting
- **artistic**: Creative composition with beautiful lighting
- **professional**: Business headshot with clean background
- **casual**: Natural expression in everyday setting

## Response Format

All generation endpoints return a response in this format:

```json
{
  "image_url": "https://replicate.delivery/pbxt/...",
  "model_used": "InstantID",
  "generation_id": "uuid-string"
}
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input parameters
- **500 Internal Server Error**: Generation failed or model error
- **422 Unprocessable Entity**: Validation errors

## Development

### Project Structure

```
├── main.py                 # FastAPI application
├── portrait_service.py     # Portrait generation service
├── config.py              # Configuration and model settings
├── static/
│   └── index.html         # Frontend web interface
├── requirements.txt       # Python dependencies
├── run.py                # Application launcher
├── setup.py              # Setup script
├── test_api.py           # API testing script
└── README.md             # This file
```

### Adding New Models

To add a new model:

1. Add model configuration to `config.py`
2. Add generation method to `PortraitGenerationService`
3. Add endpoint to `main.py`

### Environment Variables

- `REPLICATE_API_TOKEN`: Your Replicate API token (required)

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Check the [Replicate documentation](https://replicate.com/docs)
- Open an issue in this repository
- Contact the maintainers 