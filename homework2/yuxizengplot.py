import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from gtts import gTTS
import random

def generate_artistic_text(text):
    width, height = 500, 200
    image = Image.new('RGB', (width, height), color=(random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)))
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((width - text_width) / 2, (height - text_height) / 2)
    
    shadow_color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    draw.text((position[0]+2, position[1]+2), text, font=font, fill=shadow_color)
    
    text_color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
    draw.text(position, text, font=font, fill=text_color)
    
    for _ in range(20):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(5, 20)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.ellipse([x, y, x+size, y+size], fill=color)
    
    return image

def generate_audio(text):
    tts = gTTS(text=text, lang='en')  # Changed to English
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    return audio_io

st.title("Artistic Text and Audio Generator")
user_input = st.text_input("Please enter some text:")

if st.button("Generate"):
    if user_input:
        with st.spinner("Generating artistic text image..."):
            try:
                image = generate_artistic_text(user_input)
                st.image(image, caption='Generated Artistic Text', use_column_width=True)
            except Exception as e:
                st.error(f"Error generating image: {str(e)}")

        with st.spinner("Generating audio..."):
            audio_io = generate_audio(user_input)
            st.audio(audio_io, format='audio/mp3')
    else:
        st.warning("Please enter some text before generating.")