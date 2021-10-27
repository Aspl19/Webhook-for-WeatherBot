import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/webhook', methods = ['POST'])

def webhook():
  req = request.get_json(silent = True, force = True)
  print(json.dumps(req, indent = 4))

  res = makeResponse(req)
  res = json.dumps(res, indent = 4)
  r = make_response(res)
  r.headers['Content-Type'] = 'application/json'
  return r


def makeResponse(req):
  result = req.get("result")  #Based on the format of json from DialogFlow
  parameters = req.get("parameters")
  city = parameters.get("geo-city")
  date = parameters.get("date")

  r = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=40812ead86415b8f702757200cbbda8d")
  json_object = r.json()
  weather = json_object["list"]

  for i in range(0, 30):
    if date in weather[i]["dt_txt"]:
      condition = weather[i]["weather"][0]["description"]
      break

  """
  There're 3 fields that DialogFlow expects in the response.
  {
    "speech" : "",          # Response to the request
    "displayText" : "",     # Text displayed on user device screen
    "source" : ""           # Data Source
  }

  """

  speech = "The forecast for " + city + " for " + date + " is " + condition

  return {
    "speech" : speech,
    "displayText" : speech,
    "source" : "apiai-weather-webhook"
    }



if __name__ == "__main__":
  port = int(os.getenv('PORT', 5000))  # port defaults to 5000
  print("Starting app on port %d" %d port)
  app.run(debug = False, port = port, host = '0.0.0.0')  # Defaults to 127.0.0.1 (localhost) and '0.0.0.0' to have server externally