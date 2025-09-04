from flask import Flask, json, jsonify
from bs4 import BeautifulSoup
import requests
import re

TAX_URL = "https://www.ato.gov.au/tax-rates-and-codes/tax-rates-australian-residents"
DEFAULT_RATES = [
    {
        "year": "2025–26",
        "rates": [
            {
                "threshold": 18200,
                "rate": 0.0
            },
            {
                "threshold": 45000,
                "rate": 16.0
            },
            {
                "threshold": 135000,
                "rate": 30.0
            },
            {
                "threshold": 190000,
                "rate": 37.0
            },
            {
                "threshold": -1,
                "rate": 45.0
            }
        ]
    },
    {
        "year": "2024–25",
        "rates": [
            {
                "threshold": 18200,
                "rate": 0.0
            },
            {
                "threshold": 45000,
                "rate": 16.0
            },
            {
                "threshold": 135000,
                "rate": 30.0
            },
            {
                "threshold": 190000,
                "rate": 37.0
            },
            {
                "threshold": -1,
                "rate": 45.0
            }
        ]
    },
    {
        "year": "2023–24",
        "rates": [
            {
                "threshold": 18200,
                "rate": 0.0
            },
            {
                "threshold": 45000,
                "rate": 19.0
            },
            {
                "threshold": 120000,
                "rate": 32.5
            },
            {
                "threshold": 180000,
                "rate": 37.0
            },
            {
                "threshold": -1,
                "rate": 45.0
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
                cashreg = cashreg[1] if len(cashreg) > 1 else "-1"
                cashcap = int(re.sub(r"\,", "", cashreg))
                centreg = re.findall(r"\d+(?:\.\d+)?c", ps[1].text.strip())
                centreg = centreg[0][:-1] if len(centreg) > 0 else "0"
                cents = float(centreg)
                fetched_thresholds.append({"threshold": cashcap, "rate": cents})
            fetched_rates.append({"year": caption, "rates": fetched_thresholds})

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