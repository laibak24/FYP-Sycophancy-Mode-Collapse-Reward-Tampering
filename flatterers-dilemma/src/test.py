import google.generativeai as genai

genai.configure(api_key="AIzaSyAScWV662yQAvZBLi9VrO7GbTb-KfvjWHE")

for m in genai.list_models():
    print(m.name)
