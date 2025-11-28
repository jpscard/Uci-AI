from pathlib import Path
import sys

# Get the absolute path of the current file
FILE = Path(__file__).resolve()
# Get the parent directory of the current file
ROOT = FILE.parent
# Add the root path to the sys.path list if it is not already there
if ROOT not in sys.path:
    sys.path.append(str(ROOT))
# Get the relative path of the root directory with respect to the current working directory
ROOT = ROOT.relative_to(Path.cwd())

# --- Fontes ---
IMAGE = 'Imagem'
VIDEO = 'Vídeo'
WEBCAM = 'Webcam'
YOUTUBE = 'YouTube'
SOURCES_LIST = [IMAGE, VIDEO, WEBCAM, YOUTUBE]

# --- Diretórios de Ativos (Assets) ---
ASSETS_DIR = ROOT / 'assets'
IMG_DIR = ASSETS_DIR / 'img'
VIDEO_DIR = ASSETS_DIR / 'videos'
TRAINING_RESULTS_DIR = ASSETS_DIR / 'training_results'

# --- Diretório de Saída (Output) ---
OUTPUT_DIR = ROOT / 'output'

# --- Diretório do Modelo ---
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'best.pt'

# --- Dicionário de Vídeos ---
VIDEOS_DICT = {
    'video_1': VIDEO_DIR / 'abacate.mp4',
    'video_2': VIDEO_DIR / 'banana.mp4',
    'video_3': VIDEO_DIR / 'caqui.mp4',
    'video_4': VIDEO_DIR / 'mamao.mp4',
    'video_5': VIDEO_DIR / 'melancia.mp4',
    'video_6': VIDEO_DIR / 'morango.mp4',
    'video_7': VIDEO_DIR / 'pera.mp4',
    'video_8': VIDEO_DIR / 'pimentao.mp4',
    'video_9': VIDEO_DIR / 'tomate.mp4',
}

# --- Webcam ---
WEBCAM_PATH = 0
