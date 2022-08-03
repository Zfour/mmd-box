from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')

name_space = '/dcenter'


#python端更新json
def update_json(dir,name,content):
    with open(dir, "r") as load_f:
        row_data = json.load(load_f)
    row_data[name]=content
    with open(dir, "w") as dunp_f:
        json.dump(row_data, dunp_f)

#读取当前video播放dir，默认为存储上一次的值
with open("static/config.json", "r") as f:
    row_data=json.load(f)
current_video_src=row_data['current_video_src']
current_show_mode_id=int(row_data['current_show_mode'])

def get_video_list(video_path):
# 文件夹目录
 video_list=[] #路径列表
 for root,dirs,files in os.walk(video_path):
     for file in files:
         #print(os.path.join(root,file))
         video_list.append(os.path.join(root,file).replace("\\","/"))
 #print(video_list)
 return video_list

@socketio.on('connect', namespace=name_space)
def connected_msg():
    print('client connected.')

@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    print('client disconnected.')

@socketio.on('my_event', namespace=name_space)
def mtest_message(message):
    print(message)
    emit('my_response',
         {'data': message['data'], 'count': 1})

# mmd-box相关规则
#
#
#

@app.route('/')
def index():
    return render_template('box_view/index.html')

#播放下一段视频
@app.route('/nextvideo')
def push_once():
    video_path = "./static/video"
    video_list = get_video_list(video_path)
    with open("static/config.json", "r") as load_f:
        row_data = json.load(load_f)
    print(video_list)
    print(row_data['current_video_src'])
    #获取当前播放视频的文件夹index&异常处理
    if row_data['current_video_src'] in video_list:
        current_video_src = (int(video_list.index(row_data['current_video_src'].replace("\\", "/"))) + 1) % len(
            video_list)
        row_data['current_video_src'] = video_list[current_video_src]

    else:
        row_data['current_video_src'] = video_list[0]

    with open("static/config.json", "w") as dunp_f:
        json.dump(row_data, dunp_f)
    event_name = 'dcenter'
    video_src= row_data['current_video_src']
    broadcasted_data = {'data': "next video!","video_src":video_src}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    return '成功执行操作！已切换至下一个视频！'

#播放下一段视频
@app.route('/lastvideo')
def push_once_last():
    video_path = "./static/video"
    video_list = get_video_list(video_path)
    with open("static/config.json", "r") as load_f:
        row_data = json.load(load_f)
    print(video_list)
    print(row_data['current_video_src'])
    #获取当前播放视频的文件夹index&异常处理
    if row_data['current_video_src'] in video_list:
        current_video_src = (int(video_list.index(row_data['current_video_src'].replace("\\", "/"))) - 1) % len(
            video_list)
        row_data['current_video_src'] = video_list[current_video_src]

    else:
        row_data['current_video_src'] = video_list[0]

    with open("static/config.json", "w") as dunp_f:
        json.dump(row_data, dunp_f)
    event_name = 'dcenter'
    video_src= row_data['current_video_src']
    broadcasted_data = {'data': "last video!","video_src":video_src}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    return '成功执行操作！已切换至上一个视频！'

#切换UI显示模式
@app.route('/show_mode_1')
def show_mode_1():
    event_name = 'dcenter'
    broadcasted_data = {'data': "show_mode_1!"}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    update_json("static/config.json", 'current_show_mode', 1)
    return '切换为正常显示模式！'

@app.route('/show_mode_2')
def show_mode_2():
    event_name = 'dcenter'
    broadcasted_data = {'data': "show_mode_2!"}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    update_json("static/config.json", 'current_show_mode',2)
    return '切换为隐藏UI模式！'

#循环模式
#单个循环/列表循环
@app.route('/play_mode_1')
def play_mode_1():
    event_name = 'dcenter'
    broadcasted_data = {'data': "play_mode_1!"}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    update_json("static/config.json", 'play_mode',1)
    return '切换为单个循环模式！'
@app.route('/play_mode_2')
def play_mode_2():
    event_name = 'dcenter'
    broadcasted_data = {'data': "play_mode_2!"}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    update_json("static/config.json", 'play_mode',2)
    return '切换为列表循环模式！'

# 提供前端查询的json列表
@app.route('/show_config')
def show_config():
    with open("static/config.json", "r") as load_f:
        row_data = json.load(load_f)
    if row_data['current_show_mode']==1:
        row_data['current_show_mode']='UI显示'
    elif row_data['current_show_mode']==2:
        row_data['current_show_mode'] = 'UI隐藏'
    if row_data['play_mode'] == 1:
        row_data['play_mode'] = '单个循环'
    elif row_data['play_mode'] == 2:
        row_data['play_mode'] = '列表循环'
    row_data['current_video_src']=row_data['current_video_src'].replace('./static/video/','')
    return row_data



def start():
    socketio.run(app, host='0.0.0.0', port=5050, debug=False,use_reloader=False)


