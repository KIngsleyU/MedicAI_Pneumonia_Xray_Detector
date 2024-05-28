import os
import random
import boto3
from PIL import Image, ImageEnhance

# Initialize S3 client
s3_client = boto3.client('s3')

# Define your local directory with images and the target S3 bucket
local_directory = '/path/to/your/images'
s3_bucket = 'your-s3-bucket-name'
s3_prefix = 'augmented-images/'

# Convert images to greyscale, apply augmentation, and upload them to S3
for filename in os.listdir(local_directory):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(local_directory, filename)
        with Image.open(image_path) as img:
            # Convert image to greyscale
            greyscale_img = img.convert('L')
            
            # Apply rotation (e.g., random rotation between -30 to 30 degrees)
            angle = random.uniform(-30, 30)
            rotated_img = greyscale_img.rotate(angle)
            
            # Apply random crop (e.g., cropping 10% of the border)
            width, height = rotated_img.size
            crop_percentage = 0.1
            left = int(width * crop_percentage)
            top = int(height * crop_percentage)
            right = int(width * (1 - crop_percentage))
            bottom = int(height * (1 - crop_percentage))
            cropped_img = rotated_img.crop((left, top, right, bottom))
            cropped_img = cropped_img.resize((width, height))
            
            # Apply random color transformation (brightness adjustment)
            enhancer = ImageEnhance.Brightness(cropped_img)
            factor = random.uniform(0.8, 1.2)  # Random brightness adjustment
            augmented_img = enhancer.enhance(factor)
            
            # Save the processed image temporarily
            processed_image_path = os.path.join(local_directory, 'processed_' + filename)
            augmented_img.save(processed_image_path)
            
            # Upload processed image to S3
            s3_key = s3_prefix + 'processed_' + filename
            s3_client.upload_file(processed_image_path, s3_bucket, s3_key)
            
            # Optionally, delete the temporary processed image file
            os.remove(processed_image_path)
