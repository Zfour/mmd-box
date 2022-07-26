from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')

name_space = '/dcenter'
video_path = r".\static\video"  # 文件夹目录
video_list=[] #路径列表

#读取当前video播放id，默认存储上一次的值
with open("config.json","r") as f:
    row_data=json.load(f)
current_video_id=int(row_data['current_video_ID'])
print(current_video_id)

for root,dirs,files in os.walk(video_path):
    for file in files:
        print(os.path.join(root,file))
        video_list.append(os.path.join(root,file).replace("\\","/"))
print(video_list)

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
@app.route('/')
def index():
    now_play_video_src=video_list[current_video_id]
    return render_template('box_view/index.html',now_play_video_src=now_play_video_src)
#播放下一段视频
@app.route('/nextvideo')
def push_once():
    video_list = []
    with open("config.json", "r") as load_f:
        row_data = json.load(load_f)
    for root, dirs, files in os.walk(video_path):
        for file in files:
            video_list.append(os.path.join(root, file).replace("\\", "/"))
    current_video_id = (int(row_data['current_video_ID']) + 1)%len(video_list)
    row_data['current_video_ID']=current_video_id
    with open("config.json", "w") as dunp_f:
        json.dump(row_data, dunp_f)
    event_name = 'dcenter'
    broadcasted_data = {'data': "next video!","video_src":video_list[row_data['current_video_ID']]}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    return '成功执行操作！已切换至下一个视频！'

if __name__ == '__main__':

    socketio.run(app, host='0.0.0.0', port=5050, debug=True)