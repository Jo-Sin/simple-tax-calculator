from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import re

TAX_URL = "https://www.ato.gov.au/tax-rates-and-codes/tax-rates-australian-residents"
DEFAULT_RATES = [
    {
        "year": "2025–26",
        "brackets": [
            {
                "min": 0,
                "max": 18200,
                "rate": 0.0,
                "base": 0.0
            },
            {
                "min": 18201,
                "max": 45000,
                "rate": 16.0,
                "base": 0.0
            },
            {
                "min": 45001,
                "max": 135000,
                "rate": 30.0,
                "base": 4288.0
            },
            {
                "min": 135001,
                "max": 190000,
                "rate": 37.0,
                "base": 31288.0
            },
            {
                "min": 190001,
                "max": -1,
                "rate": 45.0,
                "base": 51638.0
            }
        ]
    },
    {
        "year": "2024–25",
        "brackets": [
            {
                "min": 0,
                "max": 18200,
                "rate": 0.0,
                "base": 0.0
            },
            {
                "min": 18201,
                "max": 45000,
                "rate": 16.0,
                "base": 0.0
            },
            {
                "min": 45001,
                "max": 135000,
                "rate": 30.0,
                "base": 4288.0
            },
            {
                "min": 135001,
                "max": 190000,
                "rate": 37.0,
                "base": 31288.0
            },
            {
                "min": 190001,
                "max": -1,
                "rate": 45.0,
                "base": 51638.0
            }
        ]
    },
    {
        "year": "2023–24",
        "rates": [
            {
                "min": 0,
                "max": 18200,
                "rate": 0.0,
                "base": 0.0
            },
            {
                "min": 18201,
                "max": 45000,
                "rate": 19.0,
                "base": 0.0
            },
            {
                "min": 45001,
                "max": 120000,
                "rate": 32.5,
                "base": 5092.0
            },
            {
                "min": 120001,
                "max": 180000,
                "rate": 37.0,
                "base": 29467.0
            },
            {
                "min": 180001,
                "max": -1,
                "rate": 45.0,
                "base": 51667.0
            }
        ]
    }
]

api = Flask(__name__)

@api.route('/api/rates', methods=['GET'])
def get_rates():
    try:
        fetched_rates = []
        page = requests.get(TAX_URL)
        soup = BeautifulSoup(page.content, "html.parser")
        tables = soup.find_all("table")
        for table in tables:
            fetched_thresholds = []
            caption = table.find("caption").text.strip().split()[-1]
            trs = table.find_all("tr")[1:]
            for tr in trs:
                ps = tr.find_all("p")
                cashreg = re.findall(r"\d+(?:\,\d+)?(?:\.\d+)?", ps[0].text.strip())
                if len(cashreg) < 2:
                    cashreg.append("-1")
                min_cash, max_cash = map(lambda x: int(re.sub(r"\,", "", x)), cashreg)

                ps1_text = ps[1].text.strip()
                base_regex = re.findall(r"^\$\d+(?:\,\d+)?(?:\.\d+)?", ps1_text)
                base_tax = float(re.sub(r"\,", "", base_regex[0][1:])) if len(base_regex) > 0 else 0.0
                print('base:', base_regex, base_tax)
                centreg = re.findall(r"\d+(?:\.\d+)?c", ps1_text)
                centreg = centreg[0][:-1] if len(centreg) > 0 else "0"
                cents = float(centreg)
                fetched_thresholds.append({"min": min_cash, "max": max_cash, "rate": cents, "base": base_tax})
            fetched_rates.append({"year": caption, "brackets": fetched_thresholds})

        response = jsonify(fetched_rates)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(e)
        response = jsonify(DEFAULT_RATES)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

if __name__ == '__main__':
    api.run(host='0.0.0.0')