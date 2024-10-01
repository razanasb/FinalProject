# 🌱 Plant Identification and Care App

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Expected Outputs](#-expected-outputs)
- [Model Choices and Pipeline Explanations](#-model-choices-and-pipeline-explanations)
- [Special Measures for Arabic Language Support](#-special-measures-for-arabic-language-support)
- [Tech Stack and Dependencies](#-tech-stack-and-dependencies)
- [Usage Instructions](#-usage-instructions)
- [Plant Dictionaries](#-plant-dictionaries)
- [Hugging Face Integration](#-hugging-face-integration)
- [Video Walkthrough](#-video-walkthrough)
- [Future Enhancements](#-future-enhancements)

---

## 🚀 Project Overview

This project is a web app built using Gradio that helps users identify plants from an image input. After identifying the plant, it provides care instructions and interesting facts. Users can also listen to plant facts in English or Arabic. The app uses Hugging Face models for plant classification, translation, and text-to-speech services for audio playback.

This app is designed for both English and Arabic-speaking users and provides a simple, user-friendly experience.

---

## 🌟 Key Features

- **Plant Identification from Images**: Upload an image to identify the plant.
- **Bilingual Support**: Choose between English and Arabic for care instructions and plant facts.
- **Text-to-Speech Audio**: Listen to plant facts in your chosen language.

---

## 📊 Expected Outputs

1. **Plant Name**: The identified plant’s name (from image or text input).
2. **Care Instructions**: Tips on how to care for the plant.
3. **Interesting Fact**: A fun fact about the plant.
4. **Audio Output**: An audio file with the plant fact in English or Arabic.

---

## 🛠 Model Choices and Pipeline Explanations

### 1. Image Classification
- **Model**: `umutbozdag/plant-identity`
- **Purpose**: To identify plants from an uploaded image.
- **Pipeline**: The model processes the uploaded image and provides a prediction of the plant’s name.

### 2. Translation Models
- **Models**:
  - `Helsinki-NLP/opus-mt-ar-en` (Arabic to English translation)
  - `Helsinki-NLP/opus-mt-en-ar` (English to Arabic translation)
- **Purpose**: To translate plant care instructions between English and Arabic.
- **Pipeline**: Once a plant is identified, the care instructions are translated depending on the user’s language preference.

### 3. Text-to-Speech (TTS)
- **Library**: `gTTS`
- **Purpose**: To convert plant facts into audio in English or Arabic.
- **Pipeline**: The plant fact is turned into an audio file, which can be played back in the selected language.

---

## 🌍 Special Measures for Arabic Language Support

1. **Translation**: Plant care instructions and facts are automatically translated into Arabic using Hugging Face models.
2. **Arabic Audio**: The `gTTS` library generates audio in Arabic for plant facts, providing a more interactive experience for Arabic-speaking users.

---

## 💻 Tech Stack and Dependencies

### Tech Stack:
- **Programming Language**: Python
- **Interface**: Gradio
- **Model Hosting**: Hugging Face for image classification and translation models

### Dependencies:
Install the required libraries:
```bash
pip install transformers gradio gtts
```
### 📖 Usage Instructions
Running the App:

Image Input:
Upload an image of a plant.

Select your preferred language (English or Arabic).

The app will display the plant’s name, care instructions, and an audio fact.

Example Workflow:
Upload an image of a plant.
Choose English or Arabic as your language.
View the care instructions and interesting facts.
Listen to the audio fact in your selected language.

### 🌿 Plant Dictionaries
The app has built-in dictionaries with plant care instructions and facts. If a plant is unrecognized, the app will provide default messages.

Example: Aloe Vera Image

Care: "Aloe Vera prefers bright, indirect sunlight. Water deeply but infrequently."

Fact: "Aloe Vera is known for its soothing properties and is often used in skincare."

You can add more plants by expanding the plant_care_dict and plant_facts_dict.

### 🤖 Hugging Face Integration
The app uses the following Hugging Face models:

Image Classification: umutbozdag/plant-identity

Translation:
Helsinki-NLP/opus-mt-ar-en (Arabic to English)
Helsinki-NLP/opus-mt-en-ar (English to Arabic)

Make sure the app is connected to the internet to access these models during use.

### 🎥 Video Walkthrough
For a detailed video on how to set up and use the app, watch the Video Walkthrough. 

### 🚧 Future Enhancements
- Expand Plant Database: Add more plants with care instructions and facts.
- Improve UI: Make the user interface more engaging and responsive.
- Additional Language Support: Add more language options beyond English and Arabic.
- Plant Disease Detection: Add a feature to detect plant diseases using images.
