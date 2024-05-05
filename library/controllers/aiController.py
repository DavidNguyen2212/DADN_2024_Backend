import joblib, random
from sklearn.exceptions import InconsistentVersionWarning
import warnings
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
from library import app
from flask import jsonify, request, make_response
from library.services.format import handleRegex, get_Goldprice
from library.connectIOserver import client

def load_model(file_name):
    model = joblib.load(file_name, mmap_mode='r')
    return model

commandSet = load_model("library/AI_modules/commandVoice/commandset.pkl")
weather_predictor, scaler = load_model("library/AI_modules/predictWeather/weatherPredictor.pkl")

poems = ["Mặt trời mới mọc ở đằng tây... Thiên hạ ngạc nhiên chuyện lạ này. Ngơ ngác nhìn nhau và tự hỏi. Thức dậy hay là... ngủ nữa đây.",
         "Trong tù không rượu cũng không hoa, Cảnh đẹp đêm nay, khó hững hờ! Người ngắm trăng soi ngoài cửa sổ... Trăng nhòm khe cửa ngắm nhà thơ.",
         "Ai bán cho tôi một mảnh tình. Để tôi thay vải, may áo xinh. Để tôi khỏi lạnh khi đông đến. Để tôi được thấy nắng lung linh."]


@app.route("/voice", methods=['POST'])
def processText():
    text = request.json.get("usertext")
    # Tách riêng số và mệnh lệnh 
    temp, noNumberText = handleRegex(text)

    command = commandSet.predict([noNumberText])[0]
    if command == 'bật điều hòa':
        if temp is not None and 0 <= temp <= 30:
            # client.publish
            client.publish("control-fan", 'ON')
            client.publish("ac", int(temp * 100 / 40))
            response = make_response(jsonify({"Reply": "Tui đã bật điều hòa cho bạn ở nhiệt độ {} rồi đó".format(temp)}))
            return response, 200
        else:
            client.publish("control-fan", 'ON')
            response = make_response(jsonify({"Reply": "Tui đã bật điều hòa cho bạn rồi đó!"}))
            return response, 200
    elif command == 'tắt điều hòa':
        client.publish("control-fan", 'OFF')
        response = make_response(jsonify({"Reply": "Tui đã tắt điều hòa cho bạn rồi đó!"}))
        return response, 200
    elif command == 'tắt đèn chùm':
        client.publish("chandeliers", 'OFF')
        response = make_response(jsonify({"Reply": "Tui đã tắt đèn chùm cho bạn rồi đó!"}))
        return response, 200
    elif command == 'bật đèn chùm':
        client.publish("chandeliers", 'ON')
        response = make_response(jsonify({"Reply": "Tui đã bật đèn chùm cho bạn rồi đó!"}))
        return response, 200
    elif command == 'giá vàng':
        response = make_response(jsonify({"Reply": get_Goldprice()}))
        return response, 200
    elif command == 'làm thơ':
        response = make_response(jsonify({"Reply": "Tôi làm thơ nhé. " + random.choice(poems)}))
        return response, 200
    elif command == 'chửi thề':
        response = make_response(jsonify({"Reply": "Chửi bậy, nói tục là không ngoan, không phải cháu ngoan Bác Hồ bạn ei!"}))
        return response, 200
    elif command == 'undefined':
        response = make_response(jsonify({"Reply": "Xin lỗi tôi không thể giúp bạn! Vui lòng nhắc lại hoặc đưa ra mệnh lệnh khác"}))
        return response, 200
    
    response = make_response(jsonify({"Reply": "Error while processing text!"}))
    return response, 402

@app.route("/weather_predict", methods=['GET'])
def predict_weather():
    temp = float(request.args.get("temp"))
    humi = float(request.args.get("humi"))
    # Example usage
    input_data = [humi, temp]
    scaled_data = scaler.transform([input_data])
    prediction = weather_predictor.predict(scaled_data)
    weather = None
    if prediction[0] == 0:
        weather = 'CLEAR'
    elif prediction[0] == 1:
        weather = 'CLOUDY'
    elif prediction[0] == 2:
        weather = 'RAINY'
    else:
        weather = 'SUNNY'

    return jsonify({"Reply": weather}), 200