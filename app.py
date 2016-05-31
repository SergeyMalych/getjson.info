#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from blueprints import ip, random, countries, currencies, languages, hash

## app ########################################################################

app = Flask(__name__)
app.config["DEBUG"] = False
app.register_blueprint(ip.ip, url_prefix="/ip")
app.register_blueprint(countries.countries, url_prefix="/countries")
app.register_blueprint(currencies.currencies, url_prefix="/currencies")
app.register_blueprint(languages.languages, url_prefix="/languages")
app.register_blueprint(random.rand, url_prefix="/random")
app.register_blueprint(hash.hash, url_prefix="/hash")


@app.route("/")
def index():
    return '''<p><h1>JSON API for common data</h1>get JSON data of those stuff:</p>
            <ul>
            <li><h4>IP address and geolocation</h4>
                <ul>
                    <li><a href="/ip"><b>/ip</b><br>get data about your IP address</a></li>
                    <li><a href="/ip/64.233.161.99"><b>/ip/64.233.161.99</b><br>get geodata about specified IP address</a></li>
                    <li><a href="/ip/google.com"><b>/ip/google.com</b><br>get geodata about specified URI</a></li>
                </ul>
            </li>
            <li><h4>Random</h4>
                <ul>
                    <li><a href="/random"><b>/random</b><br>get random stuff</a></li>
                </ul>
            </li>
            <li><h4>Hash</h4>
                <ul>
                    <li><a href="/hash/stringtohash"><b>/hash/stringtohash</b><br>get hash for specified input</a></li>
                </ul>
            </li>
            <li><h4>Country codes (ISO 3166)</h4>
                <ul>
                    <li><a href="/countries"><b>/countries</b><br>get data about all countries</a></li>
                    <li><a href="/countries/de"><b>/countries/de</b><br>get data about specified country</a></li>
                </ul>
            </li>
            <li><h4>Currencies (ISO 4217)</h4>
                <ul>
                    <li><a href="/currencies"><b>/currencies</b><br>get data about all currencies</a></li>
                    <li><a href="/currencies/eur"><b>/currencies/eur</b><br>get data about specified currency by identifier</a></li>
                </ul>
            </li>
            <li><h4>Languages (ISO 639)</h4>
                <ul>
                    <li><a href="/languages"><b>/languages</b><br>get data about all languages</a></li>
                    <li><a href="/languages/heb"><b>/languages/heb</b><br>get data about specified language by identifier</a></li>
                </ul>
            </li>
            </ul>
            Contact: sergey.malych [at] gmail [dot] com'''


###############################################################################

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, threaded=True)