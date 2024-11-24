import os
import google.generativeai as genai

def llm(prompt,context,schema=None):
  genai.configure(api_key="AIzaSyDVzN38pImW354xd70Q9kbu9xysj8RTC9I")

  # Create the model
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_schema": schema,
    "response_mime_type": "application/json"
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
  )

  chat_session = model.start_chat(
    history=[
    ]
  )

  response = chat_session.send_message(f"{prompt} and context is {context}")

  print(response.text)
  return response.text



# prompt = "extract and save this given data into structured json"
# context = """See the examples to explore the capabilities of these model variations.

# [*] A token is equivalent to about 4 characters for Gemini models. 100 tokens are about 60-80 English words.

# [**] RPM: Requests per minute
# TPM: Tokens per minute
# RPD: Requests per day
# TPD: Tokens per day

# Due to capacity limitations, specified maximum rate limits are not guaranteed.

# Model version name patterns
# Gemini models are available in either preview or stable versions. In your code, you can use one of the following model name formats to specify which model and version you want to use.

# Latest: Points to the cutting-edge version of the model for a specified generation and variation. The underlying model is updated regularly and might be a preview version. Only exploratory testing apps and prototypes should use this alias.

# To specify the latest version, use the following pattern: <model>-<generation>-<variation>-latest. For example, gemini-1.0-pro-latest.

# Latest stable: Points to the most recent stable version released for the specified model generation and variation.

# To specify the latest stable version, use the following pattern: <model>-<generation>-<variation>. For example, gemini-1.0-pro.

# Stable: Points to a specific stable model. Stable models don't change. Most production apps should use a specific stable model.

# To specify a stable version, use the following pattern: <model>-<generation>-<variation>-<version>. For example, gemini-1.0-pro-001.

# Experimental: Points to an experimental model available in Preview, as defined in the Terms, meaning it is not for production use. We release experimental models to gather feedback, get our latest updates into the hands of developers quickly, and highlight the pace of innovation happening at Google. What we learn from experimental launches informs how we release models more widely. An experimental model can be swapped for another without prior notice. We don't guarantee that an experimental model will become a stable model in the future.

# To specify an experimental version, use the following pattern: <model>-<generation>-<variation>-<version>. For example, gemini-1.5-pro-exp-0827.

# Available languages
# Gemini models are trained to work with the following languages:

# Arabic (ar)
# Bengali (bn)
# Bulgarian (bg)
# Chinese simplified and traditional (zh)
# Croatian (hr)
# Czech (cs)
# Danish (da)
# Dutch (nl)
# English (en)
# Estonian (et)
# Finnish (fi)
# French (fr)
# German (de)
# Greek (el)
# Hebrew (iw)
# Hindi (hi)
# Hungarian (hu)
# Indonesian (id)
# Italian (it)
# Japanese (ja)
# Korean (ko)
# Latvian (lv)
# Lithuanian (lt)"""
# print(llm(prompt,context))