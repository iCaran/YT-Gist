import openai
import os

openai.api_key = "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"

# Set the model, prompt, and parameters
model_engine = "text-davinci-002"
prompt = "Please summarize the following text:\n\n"
text_to_summarize = """
This is a very long text that you want to summarize using OpenAI's API. The text could be anything: a news article, a scientific paper, a legal document, or anything else. The goal is to generate a brief summary of the text that captures its most important points.

To do this, you can use OpenAI's GPT-3 language model, which is trained on a large corpus of diverse text and can generate high-quality summaries. You can pass the text to be summarized as input to the model, along with some additional parameters to control the length and quality of the summary.

In this example, we will use the "text-davinci-002" engine, which is one of the most powerful and versatile language models available on the OpenAI API. We will also set the "max_tokens" parameter to 100 to limit the length of the generated summary.

Once you have the summary, you can use it to quickly understand the main points of the original text and decide whether it is worth reading in full.
"""
max_tokens = 100

# Call the API to generate the summary
response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt + text_to_summarize,
    max_tokens=max_tokens
)

# Extract the summary from the API response
summary = response.choices[0].text.strip()

# Print the summary
print(summary)
