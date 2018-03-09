#!/usr/bin/python3

from external.pywebview import webview
import threading
import time
import json

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

class Api:
    def __init__(self):
        pass

    def onComplete(self, result):
        time.sleep(0.1)  # sleep to prevent from the ui thread from freezing for a moment
        # TODO send result to server!
        print(result)


def load_html(json="{}"):
    webview.load_html(WEB_PAGE.replace("###REPLACE_JSON###", json))

if __name__ == '__main__':
    json = """
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

    t = threading.Thread(target=load_html, kwargs=dict(json=json))
    t.start()

    # Create a non-resizable webview window with 800x600 dimensions
    api = Api()
    webview.create_window("Alfa GYBS Anketi", js_api=api)
