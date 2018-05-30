#!/usr/bin/python3

import webview
from core.base.messaging.message_sender import MessageSender
from core.api.util.util import Util
import threading
import time

WEB_PAGE = """
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Alfa Anket</title>
                    <script src="https://unpkg.com/jquery"></script>
                    <script src="https://surveyjs.azureedge.net/1.0.13/survey.jquery.js"></script>
                    <link href="https://surveyjs.azureedge.net/1.0.13/survey.css" type="text/css" rel="stylesheet"/>
                </head>
                <body>
                    <div id="surveyElement"></div>
                    <div id="surveyResult"></div>
                    <script type="text/javascript">
                        Survey
                            .StylesManager
                            .applyTheme("default");
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
    def __init__(self, json):
        self.json = json
        self.api = self.Api()
        t = threading.Thread(target=self.get_loader(), kwargs=dict(json=json))
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
        def onComplete(self, result):
            time.sleep(0.1)  # sleep to prevent from the ui thread from freezing for a moment
            print(result)
            ms = MessageSender(Util.server_url() + "survey-result")
            ms.send(result)


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

    s = Survey(test_json)
    s.show()
