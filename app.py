# Import required libraries
import requests
from PIL import Image
from io import BytesIO
from transformers import pipeline
import gradio as gr
import torch
from gtts import gTTS
import IPython.display as ipd
device = "cuda" if torch.cuda.is_available() else "cpu"
translator_ar_to_en = pipeline("translation_ar_to_en", model="Helsinki-NLP/opus-mt-ar-en", device=0 if device == "cuda" else -1)
translator_en_to_ar = pipeline("translation_en_to_arabic", model="Helsinki-NLP/opus-mt-en-ar", device=0 if device == "cuda" else -1)
# Load the plant identification pipeline from Hugging Face
pipe = pipeline("image-classification", model="umutbozdag/plant-identity")
plant_care_dict = {
    "Aloe Vera": "Water every 2-3 weeks, allowing the soil to dry out between waterings. Place in bright, indirect sunlight.",
    "Bamboo": "Keep the soil moist but not soggy. Place in indirect sunlight, and avoid direct exposure to sunlight.",
    "Basil": "Water regularly to keep the soil moist. Place in full sun for at least 6 hours a day.",
    "Boston fern": "Water regularly to maintain humidity. Mist the leaves often and keep in indirect sunlight.",
    "English ivy": "Water when the top inch of soil is dry. Place in moderate sunlight and maintain humidity.",
    "Ficus": "Water when the top inch of soil is dry. Place in bright, indirect light, and rotate the plant occasionally.",
    "Fiddle leaf fig": "Water when the top inch of soil is dry. Place in bright, indirect light, and avoid drafts.",
    "Lavender": "Water when the soil is dry to the touch. Place in full sun and ensure good drainage.",
    "Mint": "Water regularly to keep the soil moist. Place in partial shade, and pinch back to encourage bushiness.",
    "Monstera deliciosa": "Water when the top inch of soil is dry. Place in indirect sunlight and provide support for climbing.",
    "Orchids": "Water every 1-2 weeks. Provide humidity and place in indirect light.",
    "Peace Lily": "Water when the top inch of soil is dry. Place in low light and keep out of direct sunlight.",
    "Philodendron": "Water when the top inch of soil is dry. Place in indirect sunlight, and prune as needed.",
    "Pothos": "Water when the top inch of soil is dry. Tolerates low light but grows best in bright, indirect light.",
    "Rosemary": "Water when the top inch of soil is dry. Place in full sun and ensure good drainage.",
    "Rubber plant": "Water when the top inch of soil is dry. Place in bright, indirect light, and dust leaves regularly.",
    "Snake plant": "Water every 2-6 weeks, depending on light conditions. Place in low to bright indirect light.",
    "Spider plant": "Water when the top inch of soil is dry. Place in bright, indirect light, and avoid soggy soil.",
    "Succulents": "Water every 1-3 weeks, allowing the soil to dry completely between waterings. Place in bright sunlight.",
    "ZZ plant": "Water when the soil is completely dry, usually every 2-3 weeks. Tolerates low light conditions.",
    "Jasmine": "Water when the top inch of soil is dry. Place in full sun and prune regularly to encourage growth.",
    "Rose": "Water regularly, keeping the soil moist but not soggy. Place in full sun and fertilize during the growing season.",
    "Chamomile": "Water when the top inch of soil is dry. Place in full sun, and harvest flowers regularly.",
    "Marigold": "Water regularly, especially in dry conditions. Place in full sun and deadhead flowers to promote blooming.",
    "Daffodil": "Water when the soil is dry to the touch. Place in full sun and avoid overwatering.",
    "Geranium": "Water when the top inch of soil is dry. Place in full sun and pinch back to promote bushiness.",
    "Thyme": "Water when the soil is dry. Place in full sun and ensure good drainage.",
    "Coriander": "Water regularly to keep the soil moist. Place in full sun and harvest leaves often.",
    "Lemon Balm": "Water when the soil is dry. Place in full sun and prune regularly to encourage growth.",
    "Sage": "Water when the soil is dry. Place in full sun and provide well-drained soil.",
    "Peppermint": "Water regularly to keep the soil moist. Place in partial shade and pinch back to promote bushiness.",
    "Bougainvillea": "Water when the soil is dry. Place in full sun and prune regularly to encourage flowering.",
    "Desert Rose": "Water when the soil is dry. Place in full sun and ensure good drainage.",
    "Palm Tree": "Water when the top inch of soil is dry. Place in bright sunlight and provide adequate space for growth.",
    "Oleander": "Water when the top inch of soil is dry. Place in full sun and fertilize regularly.",
    "Cactus": "Water every few weeks, allowing the soil to dry completely between waterings. Place in bright sunlight."
}
# Plant facts dictionary
plant_facts_dict = {
    "Aloe Vera": "Aloe Vera is known for its soothing properties and is commonly used in skincare products. It thrives in bright, indirect sunlight.",
    "Bamboo": "Bamboo is one of the fastest-growing plants in the world. It prefers moist soil and indirect sunlight.",
    "Basil": "Basil is a fragrant herb that is often used in cooking. It needs plenty of sunlight and regular watering to thrive.",
    "Boston fern": "Boston ferns are popular houseplants known for their lush, green fronds. They prefer high humidity and indirect sunlight.",
    "English ivy": "English ivy is a climbing plant that can adapt to various conditions. It likes well-drained soil and moderate sunlight.",
    "Ficus": "Ficus plants are versatile and can be grown indoors or outdoors. They prefer bright, indirect light and moderate watering.",
    "Fiddle leaf fig": "Fiddle leaf figs are known for their large, glossy leaves. They thrive in bright, indirect light and require regular watering.",
    "Lavender": "Lavender is a fragrant herb often used in aromatherapy. It prefers full sun and well-drained soil.",
    "Mint": "Mint is a fast-growing herb that can easily spread. It prefers partial shade and moist soil.",
    "Monstera deliciosa": "Monstera is known for its unique leaf holes. It thrives in indirect sunlight and requires regular watering.",
    "Orchids": "Orchids are exotic flowers that require special care. They prefer indirect light and humidity.",
    "Peace Lily": "Peace Lilies are known for their elegant white flowers. They thrive in low light and require regular watering.",
    "Philodendron": "Philodendrons are popular houseplants with heart-shaped leaves. They prefer indirect sunlight and moderate watering.",
    "Pothos": "Pothos are resilient plants that can survive in low light. They prefer to dry out between waterings.",
    "Rosemary": "Rosemary is an aromatic herb that is commonly used in cooking. It prefers full sun and well-drained soil.",
    "Rubber plant": "Rubber plants are known for their large, glossy leaves. They thrive in bright, indirect light and moderate watering.",
    "Snake plant": "Snake plants are hardy and can tolerate low light. They require infrequent watering.",
    "Spider plant": "Spider plants are known for their air-purifying properties. They prefer bright, indirect light and regular watering.",
    "Succulents": "Succulents are drought-tolerant plants that store water in their leaves. They prefer bright sunlight and well-drained soil.",
    "ZZ plant": "ZZ plants are known for their glossy leaves and resilience. They thrive in low light and require infrequent watering.",
    "Jasmine": "Jasmine is a fragrant flower often used in perfumes. It prefers full sun and well-drained soil.",
    "Rose": "Roses are popular garden plants known for their beautiful flowers. They prefer full sun and regular watering.",
    "Chamomile": "Chamomile is an aromatic herb used in teas. It prefers full sun and well-drained soil.",
    "Marigold": "Marigolds are bright flowers that repel pests. They thrive in full sun and require regular watering.",
    "Daffodil": "Daffodils are spring flowers known for their trumpet shape. They prefer well-drained soil and full sun.",
    "Geranium": "Geraniums are popular bedding plants. They prefer full sun and regular watering.",
    "Thyme": "Thyme is an aromatic herb commonly used in cooking. It prefers full sun and well-drained soil.",
    "Coriander": "Coriander is an herb known for its distinct flavor. It prefers full sun and well-drained soil.",
    "Lemon Balm": "Lemon balm is a fragrant herb often used in teas. It prefers full sun and regular watering.",
    "Sage": "Sage is a hardy herb commonly used in cooking. It prefers full sun and well-drained soil.",
    "Peppermint": "Peppermint is a popular herb known for its refreshing flavor. It prefers partial shade and moist soil.",
    "Bougainvillea": "Bougainvillea is a colorful flowering plant. It prefers full sun and well-drained soil.",
    "Desert Rose": "Desert roses are succulent plants known for their beautiful flowers. They prefer full sun and well-drained soil.",
    "Palm Tree": "Palm trees are iconic tropical plants. They prefer bright sunlight and well-drained soil.",
    "Oleander": "Oleander is a hardy shrub known for its flowers. It prefers full sun and well-drained soil.",
    "Cactus": "Cacti are drought-resistant plants that thrive in dry conditions. They prefer bright sunlight and minimal watering."
}
plant_name_translations = {
    "Aloe Vera": "Aloe Vera - صبار الألوفيرا",
    "Bamboo": "Bamboo - الخيزران",
    "Basil": "Basil - الريحان",
    "Boston fern": "Boston Fern - سرخس بوسطن",
    "English ivy": "English Ivy - اللبلاب الإنجليزي",
    "Ficus": "Ficus - نبات الفيكس",
    "Fiddle leaf fig": "Fiddle Leaf Fig - التين ورقي الكمان",
    "Lavender": "Lavender - الخزامى",
    "Mint": "Mint - النعناع",
    "Monstera deliciosa": "Monstera Deliciosa - مونستيرا دليسيوسا",
    "Orchids": "Orchids - الأوركيد",
    "Peace Lily": "Peace Lily - زنبق السلام",
    "Philodendron": "Philodendron - الفيلوديندرون",
    "Pothos": "Pothos - البوتس",
    "Rosemary": "Rosemary - إكليل الجبل",
    "Rubber plant": "Rubber Plant - نبات المطاط",
    "Snake plant": "Snake Plant - نبات الثعبان",
    "Spider plant": "Spider Plant - نبات العنكبوت",
    "Succulents": "Succulents - النباتات العصارية",
    "ZZ plant": "ZZ Plant - نبات زيزي",
    "Jasmine": "Jasmine - الياسمين",
    "Rose": "Rose - الورد",
    "Chamomile": "Chamomile - البابونج",
    "Marigold": "Marigold - القطيفة",
    "Daffodil": "Daffodil - النرجس",
    "Geranium": "Geranium - إبرة الراعي",
    "Thyme": "Thyme - الزعتر",
    "Coriander": "Coriander - الكزبرة",
    "Lemon Balm": "Lemon Balm - بلسم الليمون",
    "Sage": "Sage - الميرمية",
    "Peppermint": "Peppermint - النعناع الفلفلي",
    "Bougainvillea": "Bougainvillea - الجهنمية",
    "Desert Rose": "Desert Rose - وردة الصحراء",
    "Palm Tree": "Palm Tree - النخيل",
    "Oleander": "Oleander - دفلى",
    "Cactus": "Cactus - الصبار"}
def classify_plant_image(image):
    image.save('temp_image.jpg')  # Save the image locally for pipeline processing
    predictions = pipe('temp_image.jpg')
    top_prediction = predictions[0]  # Get the top prediction
    return top_prediction['label']
def text_to_speech(instructions, language='en'):
    tts = gTTS(text=instructions, lang=language)
    tts.save('temp_audio.mp3')  # Save the audio file
    return 'temp_audio.mp3'
def process_image_input(image=None, language='english'):
    plant_name = classify_plant_image(image)  # Identify plant from image

    # Debugging: Log the identified plant name
    print(f"Identified Plant Name: {plant_name}")

    # Get care instructions in English
    care_instructions = plant_care_dict.get(plant_name, f"Care instructions are not available for '{plant_name}'.")
    plant_fact = plant_facts_dict.get(plant_name, f"Facts are not available for '{plant_name}'.")

    # Translate care instructions and facts to Arabic
    if language == 'arabic':
        care_instructions = translator_en_to_ar(care_instructions)[0]['translation_text']
        plant_fact = translator_en_to_ar(plant_fact)[0]['translation_text']
        plant_name = plant_name_translations.get(plant_name, plant_name)  # Translate plant name to Arabic

    # Generate audio for the facts
    audio_file = text_to_speech(plant_fact, language='ar' if language == 'arabic' else 'en')

    return plant_name, care_instructions, audio_file

# Main processing function for text input
def process_text_input(plant_name=None, language='english'):
    if plant_name:
        # Debugging: Log the requested plant name
        print(f"Requested Plant Name: {plant_name}")

        # Get care instructions in English
        care_instructions = plant_care_dict.get(plant_name, f"Care instructions are not available for '{plant_name}'.")
        plant_fact = plant_facts_dict.get(plant_name, f"Facts are not available for '{plant_name}'.")

        # Translate care instructions and facts to Arabic
        if language == 'arabic':
            care_instructions = translator_en_to_ar(care_instructions)[0]['translation_text']
            plant_fact = translator_en_to_ar(plant_fact)[0]['translation_text']
            plant_name = plant_name_translations.get(plant_name, plant_name)  # Translate plant name to Arabic

        # Generate audio for the facts
        audio_file = text_to_speech(plant_fact, language='ar' if language == 'arabic' else 'en')

        return plant_name, care_instructions, audio_file
# Creating Gradio app with tabs
with gr.Blocks() as demo:
    gr.Markdown("## Plant Identification and Care Instructions")

    with gr.Tab("Image Input"):
        gr.Interface(
            fn=process_image_input,
            inputs=[
                gr.Image(type="pil", label="Upload a Plant Image"),  # Image input
                gr.Dropdown(choices=["english", "arabic"], label="Select Language", value="english")  # Language selection
            ],
            outputs=[
                gr.Textbox(label="Identified Plant"),
                gr.Textbox(label="Care Instructions"),
                gr.Audio(label="Audio Fact")  # Output audio file
            ],
            title="Identify Plant from Image",
            description="Upload an image of a plant to identify it and receive care instructions in your chosen language."
        )

    with gr.Tab("Text Input"):
        gr.Interface(
            fn=process_text_input,
            inputs=[
                gr.Textbox(label="Enter Plant Name"),  # Text input
                gr.Dropdown(choices=["english", "arabic"], label="Select Language", value="english")  # Language selection
            ],
            outputs=[
                gr.Textbox(label="Identified Plant"),
                gr.Textbox(label="Care Instructions"),
                gr.Audio(label="Audio Fact")  # Output audio file
            ],
            title="Identify Plant by Name",
            description="Enter the name of a plant to receive care instructions in your chosen language."
        )

# Launch the Gradio app with Tabs
demo.launch()
