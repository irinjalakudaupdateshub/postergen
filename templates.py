"""
Prompt templates for Gemini 3 Image Generation
Each template contains placeholders in square brackets [placeholder_name]
"""

import re
from typing import Dict, List

# Template definitions
TEMPLATES = {
    "Male Candidate - Regular Photo": """Create a 4:5 poster in 4K resolution for a Kerala Local Body Election Campaign, using the uploaded candidate photo.

Candidate Instructions

Recreate the same person from the uploaded reference photo with 100% accurate facial identity. Show the candidate standing, wearing a light blue shirt (full sleeves folded to half) and a Kerala mundu. Expression: pleasant, clean, well-groomed, matching the face in the reference. Main pose: candidate waving his hand.

Style: youthful, trendy, modern Kerala election design.

Poster Layout & Design

Follow Malayalam political-poster aesthetics.

Use clear Malayalam typography.

Do NOT show any labels.

All text must be in Malayalam.

Add the following Malayalam text exactly as specified order:

1. Subheading (Regular font, lesser size than title):

[Panchayath/Constituency Name] 

2. Title (Bold, with breathing space above and below):

[Candidate Name]

3. Floating Headline 2 (Condensed sans-serif, lesser size than title ):

നമ്മുടെ [Party Name Initials] സ്ഥാനാർത്ഥിയെ [Symbol Name] അടയാളത്തിൽ വോട്ട് ചെയ്ത് വിജയിപ്പിക്കുക.

4. side Floating tagline in stylish manner with calligraphic decorations, font size less than title, Italic, handwritten style:

[Campaign Tagline]

5. Bottom Footer Section

Left side, Display Party Name: [Full Party Name]

Right side Display Symbol line, in outlined rounded corner box:

നമ്മുടെ ചിഹ്നം place one [Symbol Description] icon next to this text only

Design Instructions:
Malayalam text must be beautifully typeset. Maintain a clean, real-world election poster look with minimal background. Gentle shadows. Add delicate shapes, soft gradients, and a calm, balanced trendy composition.""",

    "Female Candidate - Regular Photo": """Create a 4:5 poster in 4K resolution for a Kerala Local Body Election Campaign, using the uploaded candidate photo.

Candidate Instructions

Recreate the same person from the uploaded reference photo with 100% accurate facial identity. Show the candidate standing and wearing a plain blue Indian saree typically used in election campaigning. The expression should be pleasant, confident, clean, and well-groomed, matching the look of the reference. The main pose should show the candidate waving her hand. Keep ornaments minimal—small earrings, a thin neck chain, one or two simple bangles, and a wristwatch.

Poster Layout & Design

Follow Malayalam political-poster aesthetics.

Use clear Malayalam typography.

Do NOT show any labels.

All text must be in Malayalam.

Add the following Malayalam text exactly as specified order:

1. Subheading (Regular font, lesser size than title):

[Panchayath/Constituency Name] ഗ്രാമ പഞ്ചായത്ത് ഒന്നാം വാർഡ് സ്ഥാനാർത്ഥി

2. Title (Bold, with breathing space above and below):

[Candidate Name]

3. Floating Headline 2 (Condensed sans-serif, lesser size than title ):

നമ്മുടെ [Party Name Initials] സ്ഥാനാർത്ഥിയെ [Symbol Name] അടയാളത്തിൽ വോട്ട് ചെയ്ത് വിജയിപ്പിക്കുക.

4. side Floating tagline in stylish manner with calligraphic decorations, font size less than title, Italic, handwritten style:

[Campaign Tagline]

5. Bottom Footer Section

Left side, Display Party Name: [Full Party Name]

Right side Display Symbol line, in outlined rounded corner box:

നമ്മുടെ ചിഹ്നം place one [Symbol Description] icon next to this text only

Design Instructions:
Malayalam text must be beautifully typeset. Maintain a clean, real-world election poster look with minimal background. Gentle shadows. Add delicate shapes, soft gradients, and a calm, balanced trendy composition.""",

    "Male Candidate - Caricature Style": """Create a 4:5 poster in 4K resolution for a Kerala Local Body Election Campaign, using the uploaded candidate photo.

Candidate Instructions

Recreate the same person from the uploaded reference photo with 100% accurate facial identity. Show the candidate standing, wearing a light blue shirt (full sleeves folded to half) and a Kerala mundu. Expression: pleasant, clean, well-groomed, matching the face in the reference. Main pose: candidate waving his hand.

Style: youthful, trendy, modern Kerala election design.

Poster Layout & Design

Follow Malayalam political-poster aesthetics.

Use clear Malayalam typography.

Do NOT show any labels.

All text must be in Malayalam.

Add the following Malayalam text exactly as specified order:

1. Subheading (Regular font, lesser size than title):

[Panchayath/Constituency Name] സ്ഥാനാർത്ഥി

2. Title (Bold, with breathing space above and below):

[Candidate Name]

3. Floating Headline 2 (Condensed sans-serif, lesser size than title ):

നമ്മുടെ [Party Name Initials] സ്ഥാനാർത്ഥിയെ [Symbol Name] അടയാളത്തിൽ വോട്ട് ചെയ്ത് വിജയിപ്പിക്കുക.

4. side Floating tagline in stylish manner with calligraphic decorations, font size less than title, Italic, handwritten style:

[Campaign Tagline]

5. Bottom Footer Section

Left side, Display Party Name: [Full Party Name]

Right side Display Symbol line, in outlined rounded corner box:

നമ്മുടെ ചിഹ്നം place one [Symbol Description] icon next to this text only

Design Instructions

Caricature-style election poster with a clean, polished, cartoonish illustration of the candidate. Use a minimal real-world election poster aesthetic with smooth lighting and gentle, natural shadows. All Malayalam text must be beautifully typeset, with modern political-poster typography. Use a calm, balanced layout with soft gradients, delicate abstract shapes, and thoughtfully used negative space. Maintain a youthful, trendy composition without clutter.""",

    "Female Candidate - Caricature Style": """Create a 4:5 poster in 4K resolution for a Kerala Local Body Election Campaign, using the uploaded candidate photo.

Candidate Instructions

Recreate the same person from the uploaded reference photo with 100% accurate facial identity. Show the candidate standing and wearing a plain blue Indian saree typically used in election campaigning. The expression should be pleasant, confident, clean, and well-groomed, matching the look of the reference. The main pose should show the candidate waving her hand. Keep ornaments minimal—small earrings, a thin neck chain, one or two simple bangles, and a wristwatch.

Poster Layout & Design

Follow Malayalam political-poster aesthetics.

Use clear Malayalam typography.

Do NOT show any labels.

All text must be in Malayalam.

Add the following Malayalam text exactly as specified order:

1. Subheading (Regular font, lesser size than title):

[Panchayath/Constituency Name] ഗ്രാമ പഞ്ചായത്ത് ഒന്നാം വാർഡ് സ്ഥാനാർത്ഥി

2. Title (Bold, with breathing space above and below):

[Candidate Name]

3. Floating Headline 2 (Condensed sans-serif, lesser size than title ):

നമ്മുടെ [Party Name Initials] സ്ഥാനാർത്ഥിയെ [Symbol Name] അടയാളത്തിൽ വോട്ട് ചെയ്ത് വിജയിപ്പിക്കുക.

4. side Floating tagline in stylish manner with calligraphic decorations, font size less than title, Italic, handwritten style:

[Campaign Tagline]

5. Bottom Footer Section

Left side, Display Party Name: [Full Party Name]

Right side Display Symbol line, in outlined rounded corner box:

നമ്മുടെ ചിഹ്നം place one [Symbol Description] icon next to this text only

Design Instructions

Caricature-style election poster with a clean, polished, cartoonish illustration of the candidate. Use a minimal real-world election poster aesthetic with smooth lighting and gentle, natural shadows. All Malayalam text must be beautifully typeset, with modern political-poster typography. Use a calm, balanced layout with soft gradients, delicate abstract shapes, and thoughtfully used negative space. Maintain a youthful, trendy composition without clutter."""
}


def extract_placeholders(template: str) -> List[str]:
    """
    Extract all placeholders from a template.
    Placeholders are in the format [placeholder_name]
    
    Args:
        template: The template string
        
    Returns:
        List of unique placeholder names
    """
    pattern = r'\[([^\]]+)\]'
    placeholders = re.findall(pattern, template)
    # Return unique placeholders while preserving order
    seen = set()
    unique_placeholders = []
    for p in placeholders:
        if p not in seen:
            seen.add(p)
            unique_placeholders.append(p)
    return unique_placeholders


def replace_placeholders(template: str, values: Dict[str, str]) -> str:
    """
    Replace placeholders in template with provided values.
    
    Args:
        template: The template string with placeholders
        values: Dictionary mapping placeholder names to their values
        
    Returns:
        Template with placeholders replaced
    """
    result = template
    for placeholder, value in values.items():
        result = result.replace(f'[{placeholder}]', value)
    return result


def get_template_names() -> List[str]:
    """Get list of all template names"""
    return list(TEMPLATES.keys())


def get_template(name: str) -> str:
    """Get template by name"""
    return TEMPLATES.get(name, "")
