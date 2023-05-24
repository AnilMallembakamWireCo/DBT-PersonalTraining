{% macro deepl_translate(text, target_lang) %}
{% set api_key = '9c25b173-6916-4bd4-7a47-1b386d7cdc52:fx' %}
{% set endpoint = "https://api.deepl.com/v2/translate" %}
{% set headers = {'Content-Type': 'application/x-www-form-urlencoded'} %}

{% set params = {
  'auth_key': api_key,
  'text': text,
  'target_lang': target_lang
} %}

{% set response = requests.post(endpoint, headers=headers, data=params) %}

{% set data = response.json() %}

{% if 'translations' in data %}
{{ data.translations[0].text }}
{% else %}
Error: {{ data.error.message }}
{% endif %}

{% endmacro %}
