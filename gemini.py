import os
import time
import textwrap
import hashlib
from pathlib import Path
from IPython.display import Markdown
from dotenv import find_dotenv,load_dotenv
from requests.exceptions import HTTPError
import google.generativeai as genai

os.environ['HTTPS_PROXY'] = 'http://10.2.49.49:7897'
timeout_seconds = 300

env = load_dotenv(find_dotenv())

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

genai.configure(api_key=GOOGLE_API_KEY)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

# models/gemini-1.0-pro
# models/gemini-1.0-pro-001
# models/gemini-1.0-pro-latest
# models/gemini-1.0-pro-vision-latest
# models/gemini-1.5-pro-latest
# models/gemini-pro
# models/gemini-pro-vision
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
uploaded_files = []
def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file.uri]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1].uri]

def run_generate_content_with_retry(model, text, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = model.generate_content(text)
            return response
        except HTTPError as e:
            print(e.response.status_code)
            if e.response.status_code == 500:
                print(f"Internal server error occurred. Retrying ({retries + 1}/{max_retries})...")
                retries += 1
                time.sleep(2 ** retries)  # Exponential backoff: 2^retries seconds
            else:
                # Handle other types of errors here
                print(f"Error occurred: {e}")
                return None
    return None  # Reached max retries without success

def write_to_file(content, output_file_path):
    # md_result = to_markdown(content)
    with open(output_file_path, 'w',encoding='utf-8') as output_file:
        output_file.write(f"{content}")        

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def run():
  with open('./pharmacy-web.txt', 'r', encoding='utf-8') as file:
    code_text = file.read()
    # response = run_generate_content_with_retry(model,code_text)
    response = model.generate_content("以下为仓库代码文件源码，请根据目录树和对应代码，输出项目文件结构，主要方法,以markdown形式输出：" + code_text)
    if response is None:
      print("Failed to get a valid response after retries.")
    else:
      write_to_file(response.text, './result.md')




run()



# models/gemini-1.0-pro
# models/gemini-1.0-pro-001
# models/gemini-1.0-pro-latest
# models/gemini-1.0-pro-vision-latest
# models/gemini-1.5-pro-latest
# models/gemini-pro
# models/gemini-pro-vision

