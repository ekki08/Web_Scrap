# core/parser.py

from bs4 import BeautifulSoup
import json
import re

class Parser:
    def __init__(self, parser_type="html.parser"):
        """
        :param parser_type: Parser type for BeautifulSoup ('html.parser', 'lxml', etc.)
        """
        self.parser_type = parser_type

    def parse_html(self, content):
        """
        Parse raw HTML using BeautifulSoup
        """
        return BeautifulSoup(content, self.parser_type)

    def extract_text(self, soup, selector, attr=None):
        """
        Extract text or attribute from HTML elements
        :param soup: BeautifulSoup object
        :param selector: CSS selector string
        :param attr: if provided, extract attribute instead of text
        """
        elements = soup.select(selector)
        if attr:
            return [el.get(attr) for el in elements if el.get(attr)]
        return [el.get_text(strip=True) for el in elements]

    def parse_json(self, content):
        """
        Parse JSON response into Python dictionary
        """
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return None

    def extract_regex(self, text, pattern):
        """
        Extract using regex pattern
        """
        return re.findall(pattern, text)
