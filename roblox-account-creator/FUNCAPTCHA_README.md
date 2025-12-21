# FunCaptcha Solver

An automatic Python-based solver for FunCaptcha (Arkose Labs) challenges. This solver provides automated solving capabilities for various FunCaptcha challenge types commonly encountered on websites.

## Features

- ✅ **Automatic Challenge Detection** - Identifies different FunCaptcha challenge types
- ✅ **Rotation Challenge Solver** - Solves image rotation challenges
- ✅ **Selection Challenge Solver** - Handles object selection challenges
- ✅ **Image Processing Utilities** - Advanced image analysis and feature extraction
- ✅ **Proxy Support** - Works with HTTP/HTTPS proxies
- ✅ **Session Management** - Handles FunCaptcha session tokens and API communication
- ✅ **Modular Design** - Easy to extend and customize

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `requests` - HTTP library for API communication
- `pillow` - Image processing
- `numpy` - Numerical operations
- `opencv-python` - Computer vision operations

## Quick Start

### Basic Usage

```python
from funcaptcha_solver import FunCaptchaSolver

# Initialize the solver
solver = FunCaptchaSolver(
    public_key="YOUR_PUBLIC_KEY",
    service_url="https://client-api.arkoselabs.com",
    page_url="https://example.com"
)

# Solve the challenge
solution_token = solver.solve()
print(f"Solution: {solution_token}")
```

### Using a Proxy

```python
solver = FunCaptchaSolver(
    public_key="YOUR_PUBLIC_KEY",
    service_url="https://client-api.arkoselabs.com",
    page_url="https://example.com",
    proxy="http://proxy.example.com:8080"
)

solution_token = solver.solve()
```

### Step-by-Step Process

```python
# Initialize solver
solver = FunCaptchaSolver(public_key, service_url, page_url)

# Get session token
session_token = solver.get_session_token()

# Get challenge data
challenge = solver.get_challenge()

# Solve automatically
solution = solver.solve()
```

## Examples

Run the example script to see different usage patterns:

```bash
# Basic usage
python example.py 1

# Usage with proxy
python example.py 2

# Step-by-step example
python example.py 3

# Show help
python example.py help
```

## How It Works

### Challenge Detection

The solver automatically detects the type of FunCaptcha challenge:
- **Type 1**: Rotation challenges (rotate image to correct orientation)
- **Type 3**: Selection challenges (select images matching criteria)
- Other types are handled with fallback methods

### Image Processing

The `funcaptcha_utils.py` module provides various image processing capabilities:

- Edge detection using Canny algorithm
- Rotation angle calculation using Hough transform
- Object detection using contour analysis
- Color analysis and feature extraction
- Image similarity comparison

### Solving Process

1. **Session Initialization**: Request a session token from FunCaptcha API
2. **Challenge Retrieval**: Fetch the current challenge data
3. **Image Analysis**: Process challenge images using computer vision
4. **Answer Generation**: Generate answers based on image analysis
5. **Submission**: Submit answers and retrieve solution token
6. **Verification**: Return the solution token for use on the website

## API Reference

### FunCaptchaSolver Class

#### `__init__(public_key, service_url, page_url, proxy=None)`

Initialize the solver with configuration parameters.

**Parameters:**
- `public_key` (str): FunCaptcha public key from the target website
- `service_url` (str): FunCaptcha API endpoint
- `page_url` (str): URL of the page containing the captcha
- `proxy` (str, optional): Proxy server URL

#### `get_session_token() -> str`

Request a session token from FunCaptcha API.

**Returns:** Session token string

#### `get_challenge() -> dict`

Fetch the current challenge data.

**Returns:** Dictionary containing challenge information

#### `solve() -> str`

Main method to solve the FunCaptcha challenge.

**Returns:** Solution token string

#### `download_image(image_url) -> Image`

Download an image from a URL.

**Parameters:**
- `image_url` (str): URL of the image

**Returns:** PIL Image object

#### `solve_rotation_challenge(image) -> int`

Solve a rotation challenge.

**Parameters:**
- `image` (Image): Challenge image

**Returns:** Rotation angle in degrees

#### `solve_selection_challenge(images, instruction) -> List[int]`

Solve a selection challenge.

**Parameters:**
- `images` (List[Image]): List of images to analyze
- `instruction` (str): Challenge instruction

**Returns:** List of selected image indices

### ImageProcessor Class

Utility class for image processing operations.

#### `preprocess_image(image) -> ndarray`

Preprocess an image for analysis.

#### `detect_edges(image) -> ndarray`

Detect edges using Canny edge detection.

#### `calculate_rotation_angle(image) -> int`

Calculate required rotation angle.

#### `calculate_similarity(image1, image2) -> float`

Calculate similarity between two images.

#### `extract_dominant_colors(image, num_colors=5) -> List[Tuple]`

Extract dominant colors from an image.

#### `calculate_image_features(image) -> dict`

Calculate various image features for classification.

## Configuration

### Finding Your Public Key

The FunCaptcha public key is typically found in the website's HTML or JavaScript. Look for:
- `data-pkey` attribute in HTML
- `publicKey` variable in JavaScript
- Network requests to `arkoselabs.com`

### Service URL

The default FunCaptcha service URL is:
```
https://client-api.arkoselabs.com
```

Some websites may use custom endpoints. Check network traffic to confirm.

## Limitations

- **Accuracy**: The solver uses heuristic methods and may not achieve 100% accuracy
- **Challenge Types**: Currently supports rotation and selection challenges
- **Rate Limiting**: Subject to FunCaptcha's rate limiting policies
- **Updates**: FunCaptcha may update their system, requiring solver updates

## Advanced Usage

### Custom Challenge Handlers

You can extend the solver to handle additional challenge types:

```python
class CustomSolver(FunCaptchaSolver):
    def solve_custom_challenge(self, challenge_data):
        # Your custom solving logic
        pass
```

### Image Analysis Customization

Customize the image processing pipeline:

```python
from funcaptcha_utils import ImageProcessor

processor = ImageProcessor()
features = processor.calculate_image_features(image)
# Use features for custom classification
```

## Troubleshooting

### Common Issues

**1. Session Token Errors**
- Verify the public key is correct
- Check that the page_url matches the target website
- Ensure network connectivity

**2. Challenge Solving Failures**
- Some challenges may be difficult to solve automatically
- Try running multiple times
- Check image processing quality

**3. Rate Limiting**
- Wait between solve attempts
- Use proxy rotation if needed
- Respect website rate limits

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Ethics and Legal Considerations

This tool is provided for educational and research purposes only. Users are responsible for:

- Complying with website Terms of Service
- Respecting rate limits and server resources
- Using the tool ethically and legally
- Understanding that automated captcha solving may violate some websites' policies

## Contributing

Contributions are welcome! Areas for improvement:

- Support for additional challenge types
- Machine learning integration for better accuracy
- Performance optimizations
- Additional language support

## License

This project is provided under the GPL-3.0 license. See the repository LICENSE file for details.

## Disclaimer

This solver is for educational purposes only. The authors are not responsible for misuse or any damages caused by this software. Always respect website terms of service and applicable laws.

## Support

For issues and questions:
- Check the examples in `example.py`
- Review this documentation
- Test with the basic configuration first

## Changelog

### Version 1.0.0
- Initial release
- Support for rotation challenges
- Support for selection challenges
- Image processing utilities
- Proxy support
- Example scripts and documentation
