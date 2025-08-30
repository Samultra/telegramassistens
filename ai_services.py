import openai
import requests
from PIL import Image
import io
import base64
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from diffusers import StableDiffusionPipeline
import torch
from config import OPENAI_API_KEY, HUGGINGFACE_TOKEN, GPT_MODEL, DALLE_MODEL, IMAGE_MODEL

class AIServices:
    def __init__(self):
        # Инициализация OpenAI
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
        
        # Инициализация Hugging Face моделей
        self.text_generator = None
        self.image_generator = None
        self._init_huggingface_models()
    
    def _init_huggingface_models(self):
        """Инициализация моделей Hugging Face"""
        try:
            # Текстовая модель для генерации кода и решения задач
            self.text_generator = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",
                token=HUGGINGFACE_TOKEN
            )
            
            # Модель для генерации изображений
            if torch.cuda.is_available():
                self.image_generator = StableDiffusionPipeline.from_pretrained(
                    IMAGE_MODEL,
                    torch_dtype=torch.float16,
                    use_auth_token=HUGGINGFACE_TOKEN
                ).to("cuda")
            else:
                self.image_generator = StableDiffusionPipeline.from_pretrained(
                    IMAGE_MODEL,
                    use_auth_token=HUGGINGFACE_TOKEN
                )
        except Exception as e:
            print(f"Ошибка инициализации Hugging Face моделей: {e}")
    
    async def generate_text_response(self, prompt, max_length=500):
        """Генерация текстового ответа"""
        try:
            if OPENAI_API_KEY:
                # Используем OpenAI GPT
                response = openai.ChatCompletion.create(
                    model=GPT_MODEL,
                    messages=[
                        {"role": "system", "content": "Ты полезный ИИ ассистент. Отвечай кратко и по делу."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_length,
                    temperature=0.7
                )
                return response.choices[0].message.content
            elif self.text_generator:
                # Используем Hugging Face модель
                response = self.text_generator(
                    prompt,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7
                )
                return response[0]['generated_text']
            else:
                return "Извините, сервис генерации текста временно недоступен."
        except Exception as e:
            return f"Ошибка генерации ответа: {str(e)}"
    
    async def generate_code(self, description):
        """Генерация кода по описанию"""
        prompt = f"Напиши код на Python для следующей задачи: {description}. Код должен быть рабочим и содержать комментарии."
        return await self.generate_text_response(prompt, max_length=1000)
    
    async def solve_problem(self, problem):
        """Решение задач"""
        prompt = f"Реши следующую задачу: {problem}. Объясни решение пошагово."
        return await self.generate_text_response(prompt, max_length=800)
    
    async def search_information(self, query):
        """Поиск информации"""
        prompt = f"Найди информацию по запросу: {query}. Предоставь краткий, но информативный ответ."
        return await self.generate_text_response(prompt, max_length=600)
    
    async def generate_image(self, prompt):
        """Генерация изображения по текстовому описанию"""
        try:
            if OPENAI_API_KEY:
                # Используем OpenAI DALL-E
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )
                image_url = response['data'][0]['url']
                
                # Скачиваем изображение
                img_response = requests.get(image_url)
                img_response.raise_for_status()
                return img_response.content
                
            elif self.image_generator:
                # Используем Hugging Face Stable Diffusion
                image = self.image_generator(prompt).images[0]
                
                # Конвертируем в байты
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                return img_byte_arr
            else:
                return None
        except Exception as e:
            print(f"Ошибка генерации изображения: {e}")
            return None
    
    async def chat_response(self, message, conversation_history=None):
        """Обработка общего чата"""
        if conversation_history:
            # Добавляем контекст предыдущих сообщений
            context = "\n".join([f"Пользователь: {msg}" for msg in conversation_history[-3:]])
            prompt = f"{context}\nПользователь: {message}\nАссистент:"
        else:
            prompt = f"Пользователь: {message}\nАссистент:"
        
        return await self.generate_text_response(prompt, max_length=500)
