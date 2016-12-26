from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import json
import ocr


class OCRServerRequestHandler(BaseHTTPRequestHandler):
    ocr_ann_obj = ocr.OCRHandle()

    def do_POST(self):
        response_content = ""
        response_code = 200
        content_length = int(self.headers.get("Content-Length"))
        payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        train_array = payload["trainArray"]
        is_train = payload["train"]

        if is_train:
            self.ocr_ann_obj.artificial_neural_network_train(train_array, True)
            response_content = {
                "type": "train",
                "result": "OK"
            }
        else:
            predict_digit = self.ocr_ann_obj.artificial_neural_network_train(train_array, False)
            response_content = {
                "type": "predict",
                "result": predict_digit
            }

        self.send_response(response_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if response_content:
            self.wfile.write(json.dumps(response_content).encode("utf-8"))
        return

if __name__ == "__main__":
    server_ip_address = ("127.0.0.1", 4567)
    httpd = HTTPServer(server_ip_address, OCRServerRequestHandler)
    httpd.serve_forever()
