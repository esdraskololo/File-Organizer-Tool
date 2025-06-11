"""
Manages internationalization (i18n) for the application.

Loads language strings from JSON files, detects system language,
and provides a mechanism to retrieve translated strings.
"""
import json
import locale
import os
import sys

class LocaleManager:
    """
    Handles loading and retrieving translated strings for different locales.
    """
    def __init__(self, locales_dir="locales", default_lang="en"):
        """
        Initializes the LocaleManager.

        Args:
            locales_dir (str, optional): The directory containing locale JSON files.
                                         Defaults to "locales".
            default_lang (str, optional): The default language code to use if
                                          system language is not found or supported.
                                          Defaults to "en".
        """
        self.locales_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), locales_dir)
        self.default_lang = default_lang
        self.translations = {}
        self.current_lang = default_lang
        self.available_languages = self._load_available_languages()

        system_lang = self.get_system_language()
        if system_lang in self.available_languages:
            self.set_language(system_lang)
        else:
            self.set_language(self.default_lang)

    def _load_available_languages(self):
        """
        Scans the locales directory to find available language JSON files.
        Reads the '_lang_name_' from each file for display purposes.

        Returns:
            dict: A dictionary mapping language codes (e.g., "en") to their
                  native display names (e.g., "English").
        """
        langs = {}
        if not os.path.isdir(self.locales_dir):
            print(f"Warning: Locales directory not found: {self.locales_dir}", file=sys.stderr)
            return {self.default_lang: "English"} # Fallback
        try:
            for filename in os.listdir(self.locales_dir):
                if filename.endswith(".json"):
                    lang_code = filename[:-5]
                    try:
                        with open(os.path.join(self.locales_dir, filename), 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            lang_name = data.get("_lang_name_", lang_code) # Expecting a _lang_name_ key in json
                            langs[lang_code] = lang_name
                    except Exception as e:
                        print(f"Warning: Could not load language file {filename}: {e}", file=sys.stderr)
            if not langs: # If no languages loaded, ensure default is somewhat available
                 langs[self.default_lang] = "English"
        except Exception as e:
            print(f"Warning: Could not list locales directory {self.locales_dir}: {e}", file=sys.stderr)
            langs[self.default_lang] = "English"
        return langs

    def load_language(self, lang_code):
        """
        Loads the translation strings for the given language code.

        If the specified language file is not found or is invalid,
        it attempts to fall back to the default language.

        Args:
            lang_code (str): The language code (e.g., "en", "tr") to load.
        """
        filepath = os.path.join(self.locales_dir, f"{lang_code}.json")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Language file not found: {filepath}. Falling back to default.", file=sys.stderr)
            if lang_code != self.default_lang:
                self.load_language(self.default_lang) # Try to load default
            else: # If default also fails
                self.translations = {} 
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {filepath}.", file=sys.stderr)
            if lang_code != self.default_lang:
                self.load_language(self.default_lang)
            else:
                self.translations = {}
        except Exception as e:
            print(f"Error loading language {lang_code}: {e}", file=sys.stderr)
            self.translations = {}


    def set_language(self, lang_code):
        """
        Sets the current language for the application.

        Loads the translations for the specified language. If the language
        is not available, it falls back to the default language.

        Args:
            lang_code (str): The language code to set.
        """
        if lang_code in self.available_languages:
            self.current_lang = lang_code
            self.load_language(lang_code)
        elif self.default_lang in self.available_languages:
            print(f"Warning: Language '{lang_code}' not available. Setting to default '{self.default_lang}'.", file=sys.stderr)
            self.current_lang = self.default_lang
            self.load_language(self.default_lang)
        else: # Absolute fallback if even default isn't in available_languages (e.g. due to loading errors)
            print(f"Critical: Default language '{self.default_lang}' also not available. Using minimal fallback.", file=sys.stderr)
            self.current_lang = self.default_lang # Keep it as default_lang code
            self.translations = {} # No translations available


    def get_string(self, key, **kwargs):
        """
        Retrieves a translated string for the given key.

        If the key is not found in the current language's translations,
        the key itself is returned. Supports string formatting with kwargs.

        Args:
            key (str): The key for the string to retrieve.
            **kwargs: Keyword arguments for string formatting.

        Returns:
            str: The translated (and formatted, if applicable) string,
                 or the key if no translation is found.
        """
        val = self.translations.get(key, key) # Return key if not found
        try:
            return val.format(**kwargs)
        except KeyError as e: # Missing a format key
            # print(f"Warning: Missing format key '{e}' for string key '{key}' in language '{self.current_lang}'.", file=sys.stderr)
            return val # Return unformatted string
        except Exception as e:
            # print(f"Warning: Error formatting string key '{key}': {e}", file=sys.stderr)
            return val


    def get_system_language(self):
        """
        Attempts to detect the system's default language.

        Tries `locale.getdefaultlocale()` and the `LANG` environment variable.

        Returns:
            str: The detected two-letter language code (e.g., "en"),
                 or the default language if detection fails.
        """
        try:
            # Works for Windows, Linux, macOS in many cases
            lang_code, _ = locale.getdefaultlocale()
            if lang_code:
                return lang_code.split('_')[0].lower() # e.g., 'en_US' -> 'en'
            
            # Fallback for some systems (especially if LANG env var is more specific)
            env_lang = os.getenv('LANG')
            if env_lang:
                return env_lang.split('.')[0].split('_')[0].lower() # e.g., 'en_US.UTF-8' -> 'en'
        except Exception as e:
            print(f"Warning: Could not detect system language: {e}", file=sys.stderr)
        return self.default_lang # Fallback to default if detection fails

    def get_available_languages_display(self):
        """
        Returns a dictionary of available language codes mapped to their
        display names.

        Returns:
            dict: Language codes to display names.
        """
        return self.available_languages

    def get_current_language_code(self):
        """
        Returns the currently set language code.

        Returns:
            str: The current language code.
        """
        return self.current_lang

