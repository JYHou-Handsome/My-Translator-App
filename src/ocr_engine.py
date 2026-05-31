import pytesseract
from PIL import Image, ImageGrab
import tempfile
import os


class OCREngine:
    def __init__(self, tesseract_cmd: str = ""):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self._tesseract_cmd = tesseract_cmd

    def set_tesseract_path(self, path: str):
        self._tesseract_cmd = path
        pytesseract.pytesseract.tesseract_cmd = path

    def recognize_from_image(self, image: Image.Image, lang: str = "chi_sim+eng") -> str:
        try:
            return pytesseract.image_to_string(image, lang=lang).strip()
        except pytesseract.TesseractError as e:
            return f"[OCR 识别失败] {e}"
        except Exception as e:
            return f"[OCR 错误] {e}"

    def recognize_from_file(self, filepath: str, lang: str = "chi_sim+eng") -> str:
        try:
            image = Image.open(filepath)
            return self.recognize_from_image(image, lang)
        except Exception as e:
            return f"[图片读取失败] {e}"
