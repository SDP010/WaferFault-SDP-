import os
import shutil
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
import json
from flask_cors import cross_origin
from Prediction_Validation import pred_validation
from Prediction_Pipeline import model_prediction
from Train_Validation import train_validation
from Training_Pipeline import model_train
from Logger import Applogger
from wsgiref import simple_server

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route('/',methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
@cross_origin()

def prediction_route():
    logger = Applogger()

    if os.path.isdir('Logs/'):
        pass
    else:
        os.makedirs('Logs/')

    try:

        # TRAINING PROCESS
        if os.path.isdir('Logs/Training_Logs/'):
            shutil.rmtree('Logs/Training_Logs/')

        os.makedirs('Logs/Training_Logs/')

        file = open('Logs/Training_Logs/training_log.txt', 'a+')

        pred_path = request.form['prediction_file']
        train_path = request.form['prediction_file']

        logger.log(file, 'Training Started!!')

        train_val = train_validation(train_path)
        logger.log(file, 'object for train_validation() initialized')

        logger.log(file, 'Training data validation Started!!')
        train_val.train_validation()
        logger.log(file, 'Training data validation completed!!')

        train_obj = model_train()
        logger.log(file,'object for model_train() initialized!!')
        print('22')
        train_obj.training_model()
        logger.log(file, 'Training completed!!')

        file.close()

        # PREDICTION PROCESS
        if os.path.isdir('Logs/Prediction_Logs/'):
            shutil.rmtree('Logs/Prediction_Logs/')

        os.makedirs('Logs/Prediction_Logs/')

        file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')

        logger.log(file, 'Prediction Started!!')
        pred_val = pred_validation(pred_path)
        logger.log(file, 'object for pred_validation() initialized!!')


        logger.log(file, 'Validation Started!!')
        pred_val.prediction_validation()
        logger.log(file, 'prediction validation done!!')


        prediction = model_prediction(pred_path)
        logger.log(file, 'object for model_prediction() initialized!!')

        result_path, json_prediction = prediction.prediction_from_model()
        logger.log(file, 'prediction done!!')

        logger.log(file, 'Result returned')
        file.close()
        return render_template('results.html', file_path=str(result_path), predictions=str(json.loads(json_prediction)))

    except Exception as e:
        file = open('Logs/MainFile_log.txt', 'a+')
        logger.log(file, f'Error Occured : {e} ')
        file.close()
        return e



# port = int(os.getenv("PORT",5000))
# if __name__=='__main__':
#     host = '0.0.0.0'
#     httpd = simple_server.make_server(host, port, app)
#     httpd.serve_forever()
    # app.run()
    
if __name__=='__main__':
    app.run(debug=True,port=os.environ["PORT"])
    
    
# if __name__=='__main__':
#     app.run(debug=True)
