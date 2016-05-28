from flask import Flask, jsonify, Blueprint, current_app, request
import pygeoip, pycountry

## IP Blueprint ################################################################

ip = Blueprint('ip', __name__)

gic = pygeoip.GeoIP(r'./GeoLiteCity.dat')

@ip.route("/")
def get_ip():
    try:
        try:
            geo = gic.record_by_addr(request.access_route)
            if not geo:
                raise
        except:
            geo = 'geolocation could not be found'
        return jsonify({'ip': request.access_route,
            'geo': geo}), 200
        #for proxy:
        # request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    except:
        return jsonify({'error': 'ip could not be found'})

@ip.route("/<address>")
def get_ip_by_parameter(address):
    try:
        try:
            geo = gic.record_by_addr(address)
            name = 'ip'
        except:
            geo = gic.record_by_name(address)
            name = 'address'
        return jsonify({name: address,
            'geo': geo}), 200
        #for proxy:
        # request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    except:
        return jsonify({'error': 'address could not be found'})


## countries Blueprint ########################################################

countries = Blueprint('countries', __name__)

@countries.route('/')
def get_countries():
    result = {}
    for country in pycountry.countries:
        country_dict_temp = {}
        country_dict_temp['name'] = country.name
        country_dict_temp['numeric'] = country.numeric
        country_dict_temp['alpha2'] = country.alpha2
        country_dict_temp['alpha3'] = country.alpha3
        try:
            country_dict_temp['official_name'] = country.official_name
        except:
            pass

        result[country.name] = country_dict_temp

    return jsonify(result), 200

@countries.route('/<country>')
def get_country(country):
    try:
        try:
            c = pycountry.countries.get(alpha2=str(country).upper())
        except:
            try:
                c = pycountry.countries.get(alpha3=str(country).upper())
            except:
                try:
                    c = pycountry.countries.get(numeric=str(country).upper())
                except:
                    c = pycountry.countries.get(name=str(country).upper())
                    
        result = {}
        result['name'] = c.name
        result['numeric'] = c.numeric
        result['alpha2'] = c.alpha2
        result['alpha3'] = c.alpha3
        try:
            result['official_name'] = c.official_name
        except:
            pass

        return jsonify(result), 200
    except:
        return jsonify({'error': 'country code could not be found'})

## currencies Blueprint ########################################################

currencies = Blueprint('currencies', __name__)

@currencies.route('/')
def get_currencies():
    result = {}
    for currency in pycountry.currencies:
        currency_dict_temp = {}
        currency_dict_temp['name'] = currency.name
        currency_dict_temp['letter'] = currency.letter
        try:
            currency_dict_temp['numeric'] = currency.numeric
        except:
            pass

        result[currency.name] = currency_dict_temp

    return jsonify(result), 200

@currencies.route('/<letter>')
def get_currency(letter):
    try:
        try:
            c = pycountry.currencies.get(letter=str(letter).upper())
        except:
            try:
                c = pycountry.currencies.get(numeric=str(letter).upper())
            except:
                c = pycountry.currencies.get(name=str(letter).upper())

        result = {}
        result['name'] = c.name
        result['numeric'] = c.numeric
        result['letter'] = c.letter

        return jsonify(result), 200
    except:
        return jsonify({'error': 'currency could not be found'})



## languages Blueprint ########################################################

languages = Blueprint('languages', __name__)

@languages.route('/')
def get_languages():
    result = {}
    for language in pycountry.languages:
        language_dict_temp = {}

        try:
            language_dict_temp['name'] = language.name
        except:
            pass
        try:
            language_dict_temp['inverted_name'] = language.inverted_name
        except:
            pass
        try:
            language_dict_temp['common_name'] = language.common_name
        except:
            pass
        try:
            language_dict_temp['iso639_1_code'] = language.iso639_1_code
        except:
            pass
        try:
            language_dict_temp['iso639_2T_code'] = language.iso639_2T_code
        except:
            pass
        try:
            language_dict_temp['iso639_3_code'] = language.iso639_3_code
        except:
            pass


        result[language.name] = language_dict_temp

    return jsonify(result), 200

@languages.route('/<code>')
def get_language(code):
    try:
        try:
            language = pycountry.languages.get(iso639_1_code=str(code).lower())
        except:
            try:
                language = pycountry.languages.get(iso639_2T_code=str(code).lower())
            except:
                language = pycountry.languages.get(iso639_3_code=str(code).lower())


        result = {}

        try:
            result['name'] = language.name
        except:
            pass
        try:
            result['common_name'] = language.common_name
        except:
            pass
        try:
            result['iso639_1_code'] = language.iso639_1_code
        except:
            pass
        try:
            result['iso639_2T_code'] = language.iso639_2T_code
        except:
            pass
        try:
            result['iso639_3_code'] = language.iso639_3_code
        except:
            pass

        return jsonify(result), 200
    except:
        return jsonify({'error': 'language could not be found'})



## app ########################################################################

app = Flask(__name__)
app.config["DEBUG"] = True
app.register_blueprint(ip, url_prefix="/ip")
app.register_blueprint(countries, url_prefix="/countries")
app.register_blueprint(currencies, url_prefix="/currencies")
app.register_blueprint(languages, url_prefix="/languages")


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
            <li><h4>Country codes (ISO 3166)</h4>
                <ul>
                    <li><a href="/countries"><b>/countries</b><br>get data about all countries</a></li>
                    <li><a href="/countries/de"><b>/countries/de</b><br>get data about specified country</a></li>
                </ul>
            </li>
            <li><h4>Currencies (ISO 4217)</h4>
                <ul>
                    <li><a href="/currencies"><b>/currencies</b><br>get data about all currencies</a></li>
                    <li><a href="/currencies/eur"><b>/currencies/eur</b><br>get data about specified currency by identifyer</a></li>
                </ul>
            </li>
            <li><h4>Languages (ISO 639)</h4>
                <ul>
                    <li><a href="/languages"><b>/languages</b><br>get data about all languages</a></li>
                    <li><a href="/languages/heb"><b>/languages/heb</b><br>get data about specified language by identifyer</a></li>
                </ul>
            </li>
            </ul>
            Contact: sergey.malych [at] gmail [dot] com'''


###############################################################################

if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=True, threaded=True)