import torch
from torchvision import transforms
import numpy as np
from PIL import Image
import torchvision.transforms.functional as TF
import os
from django.conf import settings
from basicsr.archs.rrdbnet_arch import RRDBNet

# Define model and output paths dynamically
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'net_g_latest.pth')
INPUT_IMAGE_PATH = os.path.join(settings.INPUT_IMAGE_DIR, 'InputImage.png')
OUTPUT_IMAGE_PATH = os.path.join(settings.OUTPUT_IMAGE_DIR, 'OutputImage.png')

IMPROVEMENT = {
    "NoiseReduction": None,
    "ContrastImprovement": None,
}

# Defining the ESRGAN model architecture
def create_esrgan_model(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, scale=4):
    model = RRDBNet(
        num_in_ch=num_in_ch,
        num_out_ch=num_out_ch,
        num_feat=num_feat,
        num_block=num_block,
        scale=scale,
    )
    return model

def process_with_gan(input_image_path=INPUT_IMAGE_PATH, output_image_path=OUTPUT_IMAGE_PATH):
    """Processes an image using the ESRGAN model and saves the output."""
    
    # Load Model
    model = create_esrgan_model()
    state_dict = torch.load(MODEL_PATH, map_location=torch.device('cpu'))

    # Load the correct model weights
    if 'params_ema' in state_dict:
        model.load_state_dict(state_dict['params_ema'])
    elif 'params' in state_dict:
        model.load_state_dict(state_dict['params'])
    else:
        model.load_state_dict(state_dict)

    model.eval().cpu()

    # Load and preprocess image
    img = Image.open(input_image_path).convert('RGB')
    #file_extension = img.format.lower()
    input_size = img.size

    img = img.resize((256, 256), Image.LANCZOS)
    input_tensor = TF.to_tensor(img).unsqueeze(0)

    # Run GAN model
    with torch.no_grad():
        output = model(input_tensor)

    # Convert to image format
    output_img = output.squeeze().cpu().clamp_(0, 1).permute(1, 2, 0).numpy()
    output_img = (output_img * 255.0).astype(np.uint8)
    output_img = Image.fromarray(output_img)
    output_img = output_img.resize(input_size, Image.LANCZOS)

    # Save output image
    output_img.save(output_image_path)

    return output_image_path
