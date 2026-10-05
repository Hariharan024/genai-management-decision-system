from pathlib import Path
import cv2

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def find_store_images(image_dir: str):
    directory = Path(image_dir)
    if not directory.exists():
        return []
    return sorted([p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS])


def classify_brightness(brightness: float):
    if brightness < 80: return "Dark"
    if brightness < 130: return "Moderately lit"
    if brightness < 200: return "Well lit"
    return "Very bright"


def classify_visual_detail(edge_density: float):
    if edge_density < 0.08: return "Low visual detail"
    if edge_density < 0.18: return "Moderate visual detail"
    return "High visual detail"


def analyze_image(image_path: Path):
    image = cv2.imread(str(image_path))
    if image is None:
        return {"file": image_path.name, "status": "Could not read image"}
    height, width = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = float(gray.mean())
    edges = cv2.Canny(gray, 100, 200)
    edge_density = float((edges > 0).mean())
    brightness_status = classify_brightness(brightness)
    detail_status = classify_visual_detail(edge_density)
    return {"file": image_path.name, "width": width, "height": height, "brightness": round(brightness,2), "brightness_status": brightness_status, "edge_density": round(edge_density,4), "visual_detail": detail_status, "observations": [f"Image is {brightness_status.lower()}.", f"Image contains {detail_status.lower()}."] , "status":"Analyzed"}


def analyze_store_images(image_dir: str):
    images = find_store_images(image_dir)
    results = [analyze_image(p) for p in images]
    return {"image_count": len(images), "images": results, "status": "OpenCV visual analysis completed." if images else "No store images found."}
