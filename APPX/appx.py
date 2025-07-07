from flask import Flask, render_template, request, redirect, url_for
import json, requests

app = Flask(__name__)

@app.route('/')
def masukkeindeks():
    alamatserver_ms1_dba = "http://localhost:5051/cars"
    datas_dba = requests.get(alamatserver_ms1_dba)
    rows_dba = json.loads(datas_dba.text)

    alamatserver_ms3_dbb = "http://localhost:5053/cars"
    datas_dbb = requests.get(alamatserver_ms3_dbb)
    rows_dbb = json.loads(datas_dbb.text)

    return render_template('index.html', rows_dba=rows_dba,  rows_dbb=rows_dbb)

@app.route('/ms1')
def ms1():
    servermana='MS1'
    alamatserver = "http://localhost:5051/cars"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render_template('indexms.html', rows=rows,  servermana=servermana, DB='DB-A')

@app.route('/ms2')
def ms2():
    servermana='MS2'
    alamatserver = "http://localhost:5052/cars"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render_template('indexms.html', rows=rows,  servermana=servermana, DB='DB-A')

@app.route('/ms3')
def ms3():
    servermana='MS3'
    alamatserver = "http://localhost:5053/cars"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render_template('indexms.html',  rows=rows,servermana=servermana, DB='DB-B')

@app.route('/createcar/<ms>')
def createcar(ms):
    try:
        return render_template('createcar.html', servermana=ms)
    except:
        ms = 'MS1'
        return render_template('createcar.html', servermana=ms)

@app.route('/createcarsave_ms1', methods=['GET','POST'])
def createcarsave_ms1():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']
    fdesc = "input from appx to MS1"

    datacar = {
        "carname" : fName,
        "carbrand" : fBrand, 
        "carmodel" : fModel,
        "carprice" : fPrice,
        "description":fdesc
    }
    
    datacar_json = json.dumps(datacar)

    alamatserver = "http://localhost:5051/cars/"
    
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('ms1'))

@app.route('/createcarsave_ms2', methods=['GET','POST'])
def createcarsave_ms2():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']
    fdesc = "input from appx to MS2"

    datacar = {
        "carname" : fName,
        "carbrand" : fBrand, 
        "carmodel" : fModel,
        "carprice" : fPrice,
        "description":fdesc
    }
    
    datacar_json = json.dumps(datacar)

    alamatserver = "http://localhost:5052/cars/"
    
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('ms2'))

@app.route('/createcarsave_ms3', methods=['GET','POST'])
def createcarsave_ms3():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']
    fdesc = "input from appx to MS3"

    datacar = {
        "carname" : fName,
        "carbrand" : fBrand, 
        "carmodel" : fModel,
        "carprice" : fPrice,
        "description":fdesc
    }
    
    datacar_json = json.dumps(datacar)

    alamatserver = "http://localhost:5053/cars/"
    
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('ms3'))

@app.route('/readcar/<ms>')
def readcar(ms):
    ms = ms.upper()
    if ms in ['MS1','MS2']:
        alamatserver = "http://localhost:5051/cars"
        datas = requests.get(alamatserver)
        rows = json.loads(datas.text)

        return render_template('readcar.html', rows=rows, servermana=ms, DB='DB-A')

    elif ms in ['MS3']:
        alamatserver = "http://localhost:5053/cars"
        datas = requests.get(alamatserver)
        rows = json.loads(datas.text)
        return render_template('readcar.html', rows=rows, servermana=ms, DB='DB-B')

@app.route('/updatecar/<ms>', methods=['GET', 'POST'])
def updatecar(ms):
    ms = ms.upper()
    if request.method == 'POST':
        car_id = request.form['carId']

        datacar = {
            "carname": request.form['carName'],
            "carbrand": request.form['carBrand'],
            "carmodel": request.form['carModel'],
            "carprice": request.form['carPrice'],
            "description": f"updated from {ms}"
        }

        datacar_json = json.dumps(datacar)

        if ms == 'MS1':
            alamatserver = f"http://localhost:5051/cars/{car_id}"
        elif ms == 'MS2':
            alamatserver = f"http://localhost:5052/cars/{car_id}"
        elif ms == 'MS3':
            alamatserver = f"http://localhost:5053/cars/{car_id}"
        else:
            return "Server tidak valid"

        headers = {'Content-Type': 'application/json'}
        res = requests.put(alamatserver, data=datacar_json, headers=headers)

        return redirect(url_for('readcar', ms=ms))

    return render_template('updatecar.html', servermana=ms)

@app.route('/deletecar/<ms>', methods=['GET', 'POST'])
def deletecar(ms):
    ms = ms.upper()
    if request.method == 'POST':
        car_id = request.form['carId']

        if ms == 'MS1':
            alamatserver = f"http://localhost:5051/cars/{car_id}"
        elif ms == 'MS2':
            alamatserver = f"http://localhost:5052/cars/{car_id}"
        elif ms == 'MS3':
            alamatserver = f"http://localhost:5053/cars/{car_id}"
        else:
            return "Server tidak valid"

        res = requests.delete(alamatserver)
        return redirect(url_for('readcar', ms=ms))

    return render_template('deletecar.html', servermana=ms)

@app.route('/searchcar/<ms>', methods=['GET', 'POST'])
def searchcar(ms):
    hasil = []
    ms = ms.upper()
    if request.method == 'POST':
        keyword = request.form['keyword'].lower()

        if ms == 'MS1':
            alamatserver = "http://localhost:5051/cars"
        elif ms == 'MS2':
            alamatserver = "http://localhost:5052/cars"
        elif ms == 'MS3':
            alamatserver = "http://localhost:5053/cars"
        else:
            return "Server tidak valid"

        res = requests.get(alamatserver)
        semua_data = res.json()

        hasil = [row for row in semua_data if keyword in row['carname'].lower()]

    return render_template('searchcar.html', hasil=hasil, servermana=ms)

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        debug = True
    )
