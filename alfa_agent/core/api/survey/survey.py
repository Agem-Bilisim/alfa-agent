#!/usr/bin/python3

import webview
from core.base.messaging.message_sender import MessageSender
from core.api.util.util import Util
import threading
import time
import json

WEB_PAGE = """
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Alfa Anket</title>
                    <script src="https://unpkg.com/jquery"></script>
                    <script src="https://surveyjs.azureedge.net/1.0.24/survey.jquery.js"></script>
                    <link href="https://unpkg.com/bootstrap@3.3.7/dist/css/bootstrap.min.css" rel="stylesheet"/>
                    <style>
                        .btn-green {
                            background-color: #1ab394;
                            color: #fff;
                            border-radius: 3px;
                        }
                        .btn-green:focus,
                        .btn-green:hover {
                            background-color: #18a689;
                            color: #fff;
                        }
                        .panel-footer {
                            padding: 0 15px;
                            border: none;
                            text-align: right;
                            background-color: #fff;
                        }
                    </style>
                </head>
                <body>
                    <div id="surveyElement"></div>
                    <div id="surveyResult"></div>
                    <script type="text/javascript">
                        Survey.Survey.cssType = "bootstrap";
                        Survey.defaultBootstrapCss.navigationButton = "btn btn-green";
                        var json = ###REPLACE_JSON### ;
                        window.survey = new Survey.Model(json);
                        survey.locale = "tr";
                        survey
                            .onComplete
                            .add(function (result) {
                                var result = JSON.stringify(result.data);
                                pywebview.api.onComplete(result);
                            });
                        $("#surveyElement").Survey({model: survey});
                    </script
                </body>
            </html>
            """

class Survey:
    def __init__(self, _json, survey_id):
        self.json = json.dumps(_json) if type(_json) is dict else str(_json)
        self.api = self.Api(survey_id)
        t = threading.Thread(target=self.get_loader(), kwargs=dict(json=self.json))
        t.start()

    def show(self):
        # Create a non-resizable webview window with 800x600 dimensions
        try:
            webview.create_window("Alfa GYBS Anketi", js_api=self.api)
        except Exception as e:
            print(e)

    def get_loader(self):
        def load_html(json="{}"):
            webview.load_html(WEB_PAGE.replace("###REPLACE_JSON###", json))
        return load_html

    class Api:
        def __init__(self, survey_id):
            self.survey_id = survey_id

        def onComplete(self, result):
            time.sleep(0.1)  # sleep to prevent from the ui thread from freezing for a moment
            print(result)
            res = dict()
            res["result"] = result
            res["survey_id"] = self.survey_id
            ms = MessageSender(Util.get_str_prop("CONNECTION", "server_url") + "survey-result")
            ms.send(res)


if __name__ == '__main__':
    test_json = """
        {
            questions: [
                {
                    type: "checkbox",
                    name: "car",
                    title: "What car are you driving?",
                    isRequired: true,
                    colCount: 4,
                    choices: [
                        "None",
                        "Ford",
                        "Vauxhall",
                        "Volkswagen",
                        "Nissan",
                        "Audi",
                        "Mercedes-Benz",
                        "BMW",
                        "Peugeot",
                        "Toyota",
                        "Citroen"
                    ]
                }
            ]
        }
    """

    s = Survey(test_json, 0)
    s.show()
