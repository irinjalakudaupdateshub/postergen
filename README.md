# Gemini 3 Image Generator

A Streamlit application for generating custom Kerala election posters using Gemini 3 Pro Image Preview model.

## Features

- 🎨 **Multiple Templates**: Choose from 4 pre-built election poster templates
  - Male Candidate - Regular Photo
  - Female Candidate - Regular Photo
  - Male Candidate - Caricature Style
  - Female Candidate - Caricature Style

- 📸 **Multi-Image Upload**: Upload 1-5 reference images for the candidate
- ✏️ **Custom Placeholders**: Fill in template-specific details like:
  - Candidate name
  - Panchayath/Constituency name
  - Party name and initials
  - Election symbol
  - Campaign tagline

- ⚙️ **Customizable Settings**:
  - Aspect ratio selection (1:1, 4:5, 16:9, etc.)
  - Resolution options (1K, 2K, 4K)

- 💾 **Download Generated Images**: Save your generated posters as PNG files

## Installation

1. Clone this repository or navigate to the project directory:
```bash
cd /Users/edwinjose/Documents/imagen/imagegen
```

2. Install dependencies using `uv` (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

3. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

1. Run the Streamlit app:

Using the convenience script:
```bash
./run.sh
```

Or using `uv` directly:
```bash
uv run streamlit run app.py
```

Or using streamlit directly:
```bash
streamlit run app.py
```

2. Enter your Gemini API key in the sidebar

3. Select a template from the dropdown

4. Upload 1-5 reference images of the candidate

5. Fill in all the placeholder fields with appropriate Malayalam text

6. Adjust aspect ratio and resolution if needed

7. Click "Generate Image" and wait for the result

8. Download your generated poster using the download button

## Template Placeholders

Each template requires the following information:

- **Panchayath/Constituency Name**: Name in Malayalam
- **Candidate Name**: Full name in Malayalam
- **Party Name Initials**: e.g., LDF, UDF, NDA
- **Symbol Name**: Election symbol name in Malayalam
- **Campaign Tagline**: A catchy slogan in Malayalam
- **Full Party Name**: Complete party name
- **Symbol Description**: Description of the election symbol

## Tips for Best Results

- Use clear, high-quality reference images
- Ensure all Malayalam text is properly formatted
- Fill in all placeholders for complete posters
- Use the 4:5 aspect ratio and 4K resolution for poster printing
- Keep taglines short and impactful

## Requirements

- Python 3.9+
- Streamlit 1.28.0+
- google-genai 0.3.0+
- Pillow 10.0.0+
- uv (recommended for dependency management)

## License

This project is for educational and demonstration purposes.
