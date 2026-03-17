# agent.py
from openai import OpenAI
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)

def process_examples(word, examples):
    prompt = f"""
    Clean and organize these examples for the word '{word}':
    {examples}. Reply in a structured manner, filter the ones you consider examples and
    return directly the list of each one with its translation in spanish in one line enumerated
    """
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text

def get_definition(word, language="fr") :
    second_def = 'english' if language == 'fr' else 'french'
    prompt = f"""
    Can you define two definitions of this word '{word}' in this language '{language}'

    1. short definition in spanish
    2. short definition in {second_def}

    Return JUST JSON with this format:
    DO NOT use markdown.
    DO NOT use ```json
    {{
      "definition_spanish": "...",
      "definition_other": "..."
    }}
    
    """
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    text = response.output_text
    return json.loads(text)

def get_grammar_specification(word) :
    prompt = f"""
    Can you precise if there is a particular rule of this word '{word}', for example how it is used, 
    if it is necessary to use subjunctive, prepositions, conditional, etc.

    1. Particular rule for its translation in english
    2. Particular rule for its translation in french

    Return JUST JSON with this format:
    DO NOT use markdown.
    DO NOT use ```json

    {{
      "spec_eng": "...",
      "spec_fr": "..."
    }}
    """
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    text = response.output_text
    return json.loads(text)

def analyze_tone(example_text):
    prompt = f"""
    Analyze the next phrase and just reply "formal" or "informal":
    "{example_text}"
    """
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text.strip()