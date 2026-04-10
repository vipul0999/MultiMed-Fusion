import logging
import os
from typing import List

from PIL import Image, ImageFilter, ImageOps

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover - optional dependency
    genai = None


def _prepare_variants(image: Image.Image) -> List[Image.Image]:
    grayscale = ImageOps.grayscale(image)
    autocontrast = ImageOps.autocontrast(grayscale)
    enlarged = autocontrast.resize(
        (max(1, autocontrast.width * 2), max(1, autocontrast.height * 2)),
        Image.Resampling.LANCZOS,
    )
    sharpened = enlarged.filter(ImageFilter.SHARPEN)
    thresholded = sharpened.point(lambda value: 255 if value > 165 else 0)
    return [image, autocontrast, sharpened, thresholded]


def _tesseract_ocr(variants: List[Image.Image]) -> str:
    try:
        import pytesseract
    except Exception:
        logger.warning("pytesseract is not available for local OCR.")
        return ""

    configs = [
        "--oem 3 --psm 6",
        "--oem 3 --psm 11",
        "--oem 1 --psm 4",
    ]
    candidates = []
    for variant in variants:
        for config in configs:
            try:
                text = pytesseract.image_to_string(variant, config=config)
            except Exception:
                continue
            cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip()).strip()
            if cleaned:
                candidates.append(cleaned)
    if not candidates:
        return ""
    return max(candidates, key=len)


def _gemini_vision_ocr(image: Image.Image) -> str:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key or genai is None:
        return ""

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            [
                (
                    "Extract all visible medical text from this image as faithfully as possible. "
                    "This may be a handwritten clinical note, prescription, report, or scan. "
                    "Return only the extracted text. If the image is partly unclear, preserve uncertain words as best you can."
                ),
                image,
            ],
            generation_config={"temperature": 0},
        )
        text = getattr(response, "text", "") or ""
        return "\n".join(line.strip() for line in text.splitlines() if line.strip()).strip()
    except Exception as exc:
        logger.warning("Gemini OCR fallback failed: %s", exc)
        return ""


def extract_text_from_image(path: str) -> str:
    """
    Extract text from images using a stronger hybrid OCR flow.

    1. Preprocess the image with contrast, resize, and threshold variants.
    2. Run multiple Tesseract OCR passes.
    3. Fall back to Gemini vision for difficult images such as handwriting.
    """
    try:
        with Image.open(path) as opened_image:
            image = opened_image.convert("RGB")
            variants = _prepare_variants(image)
            local_text = _tesseract_ocr(variants)
            if len(local_text) >= 40:
                return local_text

            gemini_text = _gemini_vision_ocr(variants[2])
            if len(gemini_text) > len(local_text):
                return gemini_text
            return local_text or gemini_text
    except Exception as exc:
        logger.warning("Error extracting text from image %s: %s", path, exc)
        return ""
