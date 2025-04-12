import openai
import os
from openai.error import RateLimitError

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_style_recommendation(descriptions):
    prompt = f"""
    You are a fashion stylist. Given the following clothing items: {descriptions},
    give a brief opinion on the style and 3 suggestions for improvement.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.7,
            messages=[
                {"role": "system", "content": "You are a helpful fashion advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']

    except RateLimitError:
        # Return a friendly message if rate limit is exceeded
        return "Oops, you've reached your limit. Please try again later."

    except Exception as e:
        # Handle other potential errors
        return f"An error occurred: {str(e)}"
