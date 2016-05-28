from flask import Flask, jsonify, Blueprint, current_app, request
import pygeoip, pycountry

## IP Blueprint ################################################################

ip = Blueprint('ip', __name__)

gic = pygeoip.GeoIP(r'./GeoLiteCity.dat')

@ip.route("/")
def get_ip():
    geo = gic.record_by_addr(request.remote_addr)
    return jsonify({'ip': request.remote_addr,
        'geo': geo}), 200
    #for proxy:
    # request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

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

    return jsonify(result)

@countries.route('/<country>')
def get_country_by_alpha2(country):
    try:
        c = pycountry.countries.get(alpha2=str(country).upper())
        result = {}
        result['name'] = c.name
        result['numeric'] = c.numeric
        result['alpha2'] = c.alpha2
        result['alpha3'] = c.alpha3
        try:
            result['official_name'] = c.official_name
        except:
            pass

        return jsonify(result)
    except:
        return jsonify({'error': 'country code could not be found'})

## app ########################################################################

app = Flask(__name__)
app.config["DEBUG"] = False
app.register_blueprint(ip, url_prefix="/ip")
app.register_blueprint(countries, url_prefix="/countries")


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
            <li><h4>Country codes</h4>
                <ul>
                    <li><a href="/countries"><b>/countries</b><br> get data about all countries</a></li>
                    <li><a href="/countries/de"><b>/countries/de</b><br> get data about specified country by its alpha2 code(2 letter)</a></li>
                </ul>
            </li>
            </ul>
            Contact: sergey.malych [at] gmail [dot] com'''

###############################################################################

if __name__ == "__main__":
    port = process.env.PORT || int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port, use_debugger=False, use_reloader=True, threaded=True)