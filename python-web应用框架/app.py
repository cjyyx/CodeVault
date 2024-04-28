from flask import Flask,request
import json

app=Flask(__name__)

@app.route('/')
def index():
    with open('index.html','r',encoding='utf-8')as f:
        html=f.read()
    return html
@app.route('/js/<name>')
def js_file(name=''):
    try:
        with open('js/'+name,'r',encoding='utf-8')as f:
            content=f.read()
        return content
    except:
        return 'Not Found!'


@app.route('/topy',methods=['POST'])
def topy():
    data=request.get_data()
    function_name,parameters=json.loads(data)

    # 格式：
    # function_name string
    # parameters list
    # TODO 在这写接口
    if function_name=='print':
        print(parameters)

    return json.dumps({
        'state':'ok'
    })



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)