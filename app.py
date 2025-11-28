"""
Streamlit App for Gemini 3 Image Generation
Supports multiple image uploads, prompt templates, and customizable placeholders
"""

import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import os
import uuid
from templates import (
    get_template_names,
    get_template,
    extract_placeholders,
    replace_placeholders
)

# Page configuration
st.set_page_config(
    page_title="Gemini 3 Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Default password (you can change this)
DEFAULT_PASSWORD = "imagegen2024"

# Initialize session state
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []
if 'api_key' not in st.session_state:
    # Try to load API key from Streamlit secrets first, then environment variable
    try:
        st.session_state.api_key = st.secrets.get("GEMINI_API_KEY", "")
    except (FileNotFoundError, KeyError):
        # Fall back to environment variable if secrets not configured
        st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Login function
def check_password():
    """Returns True if the user entered the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == DEFAULT_PASSWORD:
            st.session_state.authenticated = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        # Show login form
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h1 style="color: #667eea; font-size: 3rem;">🎨</h1>
            <h2 style="color: #333;">Gemini 3 Image Generator</h2>
            <p style="color: #666; font-size: 1.1rem;">Please enter the password to access the app</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.text_input(
                "Password",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="Enter password"
            )
            
            if st.session_state.get("authenticated") == False and "password" not in st.session_state:
                st.error("😕 Incorrect password. Please try again.")
        
        return False
    else:
        return True

# Check authentication before showing main app
if not check_password():
    st.stop()

# Custom CSS for better aesthetics
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Section styling */
    .section-header {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* Card styling */
    .info-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced title and description
st.markdown("""
<div class="main-header">
    <h1>🎨 Gemini 3 Image Generator</h1>
    <p>Create stunning Kerala election posters with AI-powered image generation</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for API key and settings
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # API Key input with info
    st.markdown("#### 🔑 API Key")
    
    # Check if API key is from secrets or environment
    api_key_from_external = False
    api_key_source = ""
    
    try:
        if st.secrets.get("GEMINI_API_KEY"):
            api_key_from_external = True
            api_key_source = "Streamlit secrets"
    except (FileNotFoundError, KeyError):
        if os.getenv("GEMINI_API_KEY"):
            api_key_from_external = True
            api_key_source = "environment variable"
    
    # Only show input field if API key is NOT from external source
    if api_key_from_external:
        st.success(f"✅ Configured via {api_key_source}")
    else:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state.api_key,
            help="Enter your Gemini API key",
            label_visibility="collapsed"
        )
        st.session_state.api_key = api_key
        
        if not api_key:
            st.info("💡 Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)")
            st.caption("Set in `.streamlit/secrets.toml` or as environment variable")
    
    st.divider()
    
    # Image settings
    st.markdown("#### 🖼️ Image Settings")
    
    aspect_ratio = st.selectbox(
        "📐 Aspect Ratio",
        options=["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
        index=5,  # Default to 4:5
        help="Choose the aspect ratio for your poster"
    )
    
    resolution = st.selectbox(
        "🎯 Resolution",
        options=["1K", "2K", "4K"],
        index=2,  # Default to 4K
        help="Higher resolution = better quality but slower generation"
    )
    
    st.divider()
    
    # Instructions
    st.markdown("#### 📖 How to Use")
    st.markdown("""
    <div class="info-card">
        <ol style="margin: 0; padding-left: 1.2rem;">
            <li>Enter your API key above</li>
            <li>Select a poster template</li>
            <li>Upload candidate photos</li>
            <li>Fill in campaign details</li>
            <li>Review & edit the prompt</li>
            <li>Generate your poster! 🎨</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="section-header">📝 Input Configuration</div>', unsafe_allow_html=True)
    
    # Template selection
    st.markdown("#### 🎭 Select Template")
    template_names = get_template_names()
    selected_template = st.selectbox(
        "Choose your poster style",
        options=template_names,
        help="Choose a poster template",
        label_visibility="collapsed"
    )
    
    # Get the selected template
    template = get_template(selected_template)
    
    # Image upload in an expander for better organization
    with st.expander("📸 **Upload Reference Images**", expanded=False):
        # Load default images from default_pics folder
        default_pics_dir = "default_pics"
        default_images = []
        
        if os.path.exists(default_pics_dir):
            for filename in os.listdir(default_pics_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    default_images.append(os.path.join(default_pics_dir, filename))
        
        # Show info about default images
        if default_images and not st.session_state.get('uploaded_files_used', False):
            st.info(f"📁 {len(default_images)} default image(s) loaded from `{default_pics_dir}/`")
        
        uploaded_files = st.file_uploader(
            "Upload candidate photos (1-5 images)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            help="Upload reference images for the candidate (will override default images)",
            label_visibility="collapsed"
        )
        
        # Use uploaded files if provided, otherwise use default images
        if uploaded_files:
            st.session_state.uploaded_files_used = True
            images_to_use = uploaded_files
            st.success(f"✅ {len(uploaded_files)} image(s) uploaded")
        else:
            st.session_state.uploaded_files_used = False
            images_to_use = default_images
        
        # Display images (uploaded or default)
        if images_to_use:
            cols = st.columns(min(len(images_to_use), 3))
            for idx, file in enumerate(list(images_to_use)[:3]):  # Show max 3 thumbnails
                with cols[idx]:
                    if isinstance(file, str):  # Default image path
                        image = Image.open(file)
                        st.image(image, caption=os.path.basename(file), use_container_width=True)
                    else:  # Uploaded file
                        image = Image.open(file)
                        st.image(image, caption=file.name, use_container_width=True)
            if len(images_to_use) > 3:
                st.info(f"➕ {len(images_to_use) - 3} more image(s)")
    
    # Extract placeholders from template
    placeholders = extract_placeholders(template)
    
    # Placeholder inputs in an expander
    with st.expander("✏️ **Fill in Campaign Details**", expanded=False):
        placeholder_values = {}
        
        # Group placeholders in columns for better layout
        for idx, placeholder in enumerate(placeholders):
            # Create a more user-friendly label
            label = placeholder.replace("_", " ").title()
            
            # Add emoji based on field type (check symbol before name!)
            if "panchayath" in placeholder.lower() or "constituency" in placeholder.lower():
                icon = "📍"
            elif "party" in placeholder.lower():
                icon = "🏛️"
            elif "symbol" in placeholder.lower():
                icon = "🎯"
            elif "tagline" in placeholder.lower():
                icon = "💬"
            elif "name" in placeholder.lower():
                icon = "👤"
            else:
                icon = "📝"
            
            # Provide helpful defaults based on exact placeholder names
            placeholder_lower = placeholder.lower()
            
            if placeholder == "Panchayath/Constituency Name":
                help_text = "Enter the panchayath/constituency name in Malayalam"
                default_value = "തൃശ്ശൂർ ജില്ലാ പഞ്ചായത്ത് മുരിയാട് ഡിവിഷൻ"
            elif placeholder == "Candidate Name":
                help_text = "Enter the candidate's name in Malayalam"
                default_value = "ജോസ് ജെ. ചിറ്റിലപ്പിള്ളി"
            elif placeholder == "Symbol Name":
                help_text = "Enter the election symbol name in Malayalam"
                default_value = "അരിവാൾ ചുറ്റിക നക്ഷത്രം"
            elif placeholder == "Symbol Description":
                help_text = "Describe the symbol (e.g., hammer and sickle with star)"
                default_value = "അരിവാൾ ചുറ്റിക നക്ഷത്രം"
            elif placeholder == "Campaign Tagline":
                help_text = "Enter a catchy campaign tagline in Malayalam"
                default_value = "വികസനത്തിനായി ജോസ് മാഷ്"
            elif placeholder == "Party Name Initials":
                help_text = "Enter party initials (e.g., LDF, UDF, NDA)"
                default_value = "LDF"
            elif placeholder == "Full Party Name":
                help_text = "Enter the full party name"
                default_value = "LDF"
            else:
                help_text = f"Enter value for {label}"
                default_value = ""
            
            value = st.text_input(
                f"{icon} {label}",
                value=default_value,
                key=f"placeholder_{placeholder}",
                help=help_text
            )
            placeholder_values[placeholder] = value
    
    
    # Show final prompt with placeholders replaced in an expander
    with st.expander("📝 **Final Prompt Preview**", expanded=False):
        st.caption("✨ Review and edit the prompt before generating")
        
        # Replace placeholders to show preview
        preview_prompt = replace_placeholders(template, placeholder_values)
        
        # Editable text area for the final prompt
        # Use template name in key so it resets when template changes
        final_prompt_edited = st.text_area(
            "Edit Prompt (optional)",
            value=preview_prompt,
            height=300,
            key=f"final_prompt_editor_{selected_template}",
            help="You can edit the prompt here before generating the image",
            label_visibility="collapsed"
        )


with col2:
    st.markdown('<div class="section-header">🎨 Generated Output</div>', unsafe_allow_html=True)
    
    # Generate button with better styling
    st.markdown("<br>", unsafe_allow_html=True)
    generate_button = st.button("✨ Generate Image", type="primary", use_container_width=True)
    
    if generate_button:
        # Validation
        if not st.session_state.api_key:
            st.error("❌ Please enter your Gemini API key in the sidebar")
        elif not images_to_use:
            st.error("❌ Please upload at least one reference image or ensure default images exist")
        elif not all(placeholder_values.values()):
            st.warning("⚠️ Some placeholders are empty. Please fill in all fields for best results.")
        else:
            try:
                with st.spinner("Generating image... This may take a moment."):
                    # Use the edited prompt from the text area
                    final_prompt = final_prompt_edited
                    
                    # Initialize Gemini client
                    client = genai.Client(api_key=st.session_state.api_key)
                    
                    # Prepare content list
                    content = [final_prompt]
                    
                    # Add images (uploaded or default)
                    for img_file in images_to_use:
                        if isinstance(img_file, str):  # Default image path
                            image = Image.open(img_file)
                        else:  # Uploaded file
                            # Reset file pointer
                            img_file.seek(0)
                            image = Image.open(img_file)
                        
                        # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                        content.append(image)
                    
                    # Generate image
                    response = client.models.generate_content(
                        model="gemini-3-pro-image-preview",
                        contents=content,
                        config=types.GenerateContentConfig(
                            response_modalities=['TEXT', 'IMAGE'],
                            image_config=types.ImageConfig(
                                aspect_ratio=aspect_ratio,
                                image_size=resolution
                            ),
                        )
                    )
                    
                    # Debug: Print response structure
                    print("=" * 50)
                    print("GEMINI API RESPONSE DEBUG")
                    print("=" * 50)
                    print(f"Response type: {type(response)}")
                    print(f"Response parts count: {len(response.parts)}")
                    
                    # Process response
                    st.session_state.generated_images = []
                    text_response = []
                    
                    for idx, part in enumerate(response.parts):
                        print(f"\n--- Part {idx} ---")
                        print(f"Part type: {type(part)}")
                        print(f"Has text: {part.text is not None}")
                        
                        if part.text is not None:
                            print(f"Text content: {part.text[:100]}...")
                            text_response.append(part.text)
                        else:
                            print("Attempting to get image...")
                            gemini_image = part.as_image()
                            if gemini_image:
                                print(f"Gemini Image type: {type(gemini_image)}")
                                
                                try:
                                    # Convert google.genai.types.Image to PIL Image
                                    # The Gemini Image object has image_bytes attribute
                                    if hasattr(gemini_image, 'image_bytes') and gemini_image.image_bytes:
                                        pil_image = Image.open(io.BytesIO(gemini_image.image_bytes))
                                        print(f"Converted to PIL Image: {type(pil_image)}")
                                        print(f"PIL Image mode: {pil_image.mode}, size: {pil_image.size}")
                                        st.session_state.generated_images.append(pil_image)
                                    else:
                                        print("ERROR: No image_bytes found in Gemini Image object")
                                except Exception as e:
                                    print(f"ERROR converting Gemini Image to PIL: {e}")
                                    import traceback
                                    traceback.print_exc()

                    
                    print("=" * 50)

                    
                    # Display results
                    if st.session_state.generated_images:
                        st.success("✅ Image generated successfully!")
                        
                        for idx, img in enumerate(st.session_state.generated_images):
                            try:
                                st.image(img, caption=f"Generated Poster {idx + 1}", width="stretch")
                                
                                # Save to disk with UUID filename (failsafe)
                                try:
                                    image_uuid = str(uuid.uuid4())
                                    filename = f"{image_uuid}.png"
                                    img.save(filename)
                                    print(f"✓ Saved image to: {filename}")
                                    
                                    # Read the saved file for download button
                                    with open(filename, 'rb') as f:
                                        byte_im = f.read()
                                    
                                    st.download_button(
                                        label=f"⬇️ Download Image {idx + 1}",
                                        data=byte_im,
                                        file_name=f"generated_poster_{idx + 1}.png",
                                        mime="image/png",
                                        use_container_width=True
                                    )
                                except Exception as save_error:
                                    print(f"ERROR saving image {idx + 1}: {save_error}")
                                    st.error(f"Could not create download for image {idx + 1}: {save_error}")
                                    
                            except Exception as display_error:
                                print(f"ERROR displaying image {idx + 1}: {display_error}")
                                st.error(f"Could not display image {idx + 1}: {display_error}")

                    
                    if text_response:
                        with st.expander("📝 AI Response Text"):
                            st.write("\n\n".join(text_response))
                    
                    if not st.session_state.generated_images and not text_response:
                        st.warning("⚠️ No image or text was generated. Please try again.")
                        
            except Exception as e:
                st.error(f"❌ Error generating image: {str(e)}")
                st.info("Please check your API key and try again.")
    
    # Display previously generated images
    elif st.session_state.generated_images:
        st.info("Previous generation:")
        for idx, img in enumerate(st.session_state.generated_images):
            try:
                st.image(img, caption=f"Generated Poster {idx + 1}", width="stretch")
                
                # Save to disk with UUID filename (failsafe)
                try:
                    image_uuid = str(uuid.uuid4())
                    filename = f"{image_uuid}.png"
                    img.save(filename)
                    
                    # Read the saved file for download button
                    with open(filename, 'rb') as f:
                        byte_im = f.read()
                    
                    st.download_button(
                        label=f"⬇️ Download Image {idx + 1}",
                        data=byte_im,
                        file_name=f"generated_poster_{idx + 1}.png",
                        mime="image/png",
                        use_container_width=True,
                        key=f"download_{idx}"
                    )
                except Exception as save_error:
                    print(f"ERROR saving previous image {idx + 1}: {save_error}")
                    st.error(f"Could not create download for image {idx + 1}: {save_error}")
                    
            except Exception as display_error:
                print(f"ERROR displaying previous image {idx + 1}: {display_error}")
                st.error(f"Could not display image {idx + 1}: {display_error}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Powered by Gemini 3 Pro Image Preview Beta| Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
