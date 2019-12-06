from flask import Flask, jsonify, request, redirect, url_for, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory
from sqlalchemy import and_
from flask_api import status
import csv
import json
from sqlalchemy import func
import datetime
import os
import math
from dateutil.relativedelta import relativedelta
from sqlalchemy import or_
from ReadData import *
from flask import abort
import uuid
from functools import wraps
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import re
import hashlib

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
basedir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
print(os.path.join(basedir, 'database.db'))
app.config['SQLALCHEMY_ECHO'] = True  # 显示错误信息
app.config['SQLALCHEMY_RECORD_QUERIES'] = True  # 启用查询记录
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 追踪数据库修改

app.config.from_object(__name__)
app.config['CORS_ORIGIN_ALLOW_ALL'] = True
app.config['CORS_ALLOW_CREDENTIALS'] = True
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)


# models_committed信号

class Record(db.Model):
    __tablename__ = 'records_curr'

    REC_ID = db.Column(db.Integer, primary_key=True)
    REPORT_NUM = db.Column(db.Integer)
    CREATE_TIME = db.Column(db.DateTime)
    DISTRICT_NAME = db.Column(db.String(255))
    DISTRICT_ID = db.Column(db.Integer)
    STREET_NAME = db.Column(db.String(255))
    STREET_ID = db.Column(db.Integer)
    COMMUNITY_NAME = db.Column(db.String(255))
    COMMUNITY_ID = db.Column(db.Integer)
    EVENT_TYPE_NAME = db.Column(db.String(255))
    EVENT_TYPE_ID = db.Column(db.Integer)
    MAIN_TYPE_NAME = db.Column(db.String(255))
    MAIN_TYPE_ID = db.Column(db.Integer)
    SUB_TYPE_NAME = db.Column(db.String(255))
    SUB_TYPE_ID = db.Column(db.Integer)
    DISPOSE_UNIT_NAME = db.Column(db.String(255))
    DISPOSE_UNIT_ID = db.Column(db.Integer)
    EVENT_SRC_NAME = db.Column(db.String(255))
    EVENT_SRC_ID = db.Column(db.Integer)
    OPERATE_NUM = db.Column(db.Integer)
    OVERTIME_ARCHIVE_NUM = db.Column(db.Integer)
    INTIME_TO_ARCHIVE_NUM = db.Column(db.Integer)
    INTIME_ARCHIVE_NUM = db.Column(db.Integer)
    EVENT_PROPERTY_ID = db.Column(db.Integer)
    EVENT_PROPERTY_NAME = db.Column(db.String(255))
    OCCUR_PLACE = db.Column(db.String(255))

    def __repr__(self):
        return '<Rec_id %r>' % self.REC_ID
    def __init__(self, **entries):
        self.__dict__.update(entries)




def data2JSON(data):
    dict_list = []
    for entry in data:
        item = entry.__dict__
        item.pop('_sa_instance_state')
        dict_list.append(item)
    return jsonify(dict_list)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/allitems')
def query_all():
    qData = Record.query.all()
    return data2JSON(qData)


# TODO: 加入分页
default_keys = [
    'REC_ID',
    'REPORT_NUM',
    'CREATE_TIME',
    'DISTRICT_NAME',
    'DISTRICT_ID',
    'STREET_NAME',
    'STREET_ID',
    'COMMUNITY_NAME',
    'COMMUNITY_ID',
    'EVENT_TYPE_NAME',
    'EVENT_TYPE_ID',
    'MAIN_TYPE_NAME',
    'MAIN_TYPE_ID',
    'SUB_TYPE_NAME',
    'SUB_TYPE_ID',
    'DISPOSE_UNIT_NAME',
    'DISPOSE_UNIT_ID',
    'EVENT_SRC_NAME',
    'EVENT_SRC_ID',
    'OPERATE_NUM',
    'OVERTIME_ARCHIVE_NUM',
    'INTIME_TO_ARCHIVE_NUM',
    'INTIME_ARCHIVE_NUM',
    'EVENT_PROPERTY_ID',
    'EVENT_PROPERTY_NAME',
    'OCCUR_PLACE'
]
object_name = 'Record'

str_keys = [
    'CREATE_TIME',
    'DISTRICT_NAME',
    'STREET_NAME',
    'COMMUNITY_NAME',
    'EVENT_TYPE_NAME',
    'MAIN_TYPE_NAME',
    'SUB_TYPE_NAME',
    'DISPOSE_UNIT_NAME',
    'EVENT_SRC_NAME',
    'EVENT_PROPERTY_NAME',
    'OCCUR_PLACE'
]


class EmptyQuery(Exception):
    status_code = 204

    def __init__(self, message, status_code=204):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


@app.errorhandler(EmptyQuery)
def invalid_usage(error):
    response = make_response(error.message)
    response.status_code = error.status_code
    return response


@app.route('/exception')
def exception():
    raise EmptyQuery('No privilege to access the resource', status_code=204)



# 传入字典，查找某一对象，条件可变，提供的条件如上
@app.route('/reco', methods=['GET', 'POST'])
def query_single():
    conditions = []
    params = {'CREATE_TIME': '2018-02-08 15:34:40'}
    for key in default_keys:
        if params.get(key):
            if key in str_keys:
                cond_expr_str = object_name + '.' + key + '==' + '\'' + params[key] + '\''
            else:
                cond_expr_str = object_name + '.' + key + '==' + str(params[key])
            conditions.append(eval(cond_expr_str))
    qData = Record.query.filter(*conditions).all()
    return data2JSON(qData)


@app.route('/record_test', methods=['GET', 'POST'])
def query_range_test():
    conditions = []
    params = {'CREATE_TIME': ['2018-02', '2018-03'], 'STREET_NAME': '坪山街道'}
    for key in default_keys:
        if params.get(key):
            if key in str_keys:
                cond_expr_str_start = object_name + '.' + key + '>=' + '\'' + str(params[key][0]) + '\''
                cond_expr_str_end = object_name + '.' + key + '<' + '\'' + str(params[key][1]) + '\''
            else:
                cond_expr_str_start = object_name + '.' + key + '>=' + str(params[key][0])
                cond_expr_str_end = object_name + '.' + key + '<' + str(params[key][1])
            conditions.append(eval(cond_expr_str_start))
            conditions.append(eval(cond_expr_str_end))
    qData = Record.query.filter(*conditions).all()
    return data2JSON(qData)


@app.route('/records', methods=['GET', 'POST'])
def query_range():
    conditions = []
    params = {'CREATE_TIME': ['2018-02', '2018-03']}
    for key in default_keys:
        if params.get(key):
            if key in str_keys:
                cond_expr_str_start = object_name + '.' + key + '>=' + '\'' + str(params[key][0]) + '\''
                cond_expr_str_end = object_name + '.' + key + '<' + '\'' + str(params[key][1]) + '\''
            else:
                cond_expr_str_start = object_name + '.' + key + '>=' + str(params[key][0])
                cond_expr_str_end = object_name + '.' + key + '<' + str(params[key][1])
            conditions.append(eval(cond_expr_str_start))
            conditions.append(eval(cond_expr_str_end))
    qData = Record.query.filter(*conditions).all()
    data = data2JSON(qData)
    return data


# 分类依据：事件属性
@app.route('/func1', methods=['GET', 'POST'])
def query_groupBy_Count():
    start_date_str = request.json.get("date")
    if len(start_date_str.split("-")) == 2:
        start_date_str += '-01'
        d = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = d + relativedelta(months=+1)
    else:
        d = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = d + relativedelta(days=+1)
    end_date_str = end_date.strftime('%Y-%m-%d')
    conditions = []
    params = {'CREATE_TIME': [start_date_str, end_date_str]}
    for key in default_keys:
        if params.get(key):
            if key in str_keys:
                cond_expr_str_start = object_name + '.' + key + '>=' + '\'' + str(params[key][0]) + '\''
                cond_expr_str_end = object_name + '.' + key + '<' + '\'' + str(params[key][1]) + '\''
            else:
                cond_expr_str_start = object_name + '.' + key + '>=' + str(params[key][0])
                cond_expr_str_end = object_name + '.' + key + '<' + str(params[key][1])
            conditions.append(eval(cond_expr_str_start))
            conditions.append(eval(cond_expr_str_end))

    # 查询某时间段的事件分布
    qData = db.session.query(Record.EVENT_PROPERTY_NAME, func.count(Record.EVENT_PROPERTY_NAME)) \
        .filter(*conditions) \
        .group_by(Record.EVENT_PROPERTY_NAME) \
        .all()

    # process data to fit the front end
    labels = [item[0] for item in qData]
    num = [item[1] for item in qData]
    selected = {}
    for label in labels:
        selected[label] = True
    data = {
        'problem_labels': labels,
        'problem_num': num,
        'problem_selected': selected,
        'problem_colors': [
            '#DD1B16',
            '#41B883',
            '#E46651',
            '#00D8FF',
            '#cc8400',
        ],
    }
    if len(qData) == 0:
        return jsonify(data),404
    return jsonify(data)


# 分类依据：街道、事件属性
@app.route('/func2', methods=['GET', 'POST'])
def query_ByStreet_Count():
    start_date_str = request.json.get("date")

    if len(start_date_str.split("-")) == 2:
        start_date_str += '-01'
        d = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = d + relativedelta(months=+1)
    else:
        d = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = d + relativedelta(days=+1)

    end_date_str = end_date.strftime('%Y-%m-%d')
    conditions = []
    params = {'CREATE_TIME': [start_date_str, end_date_str]}
    for key in default_keys:
        if params.get(key):
            if key in str_keys:
                cond_expr_str_start = object_name + '.' + key + '>=' + '\'' + str(params[key][0]) + '\''
                cond_expr_str_end = object_name + '.' + key + '<' + '\'' + str(params[key][1]) + '\''
            else:
                cond_expr_str_start = object_name + '.' + key + '>=' + str(params[key][0])
                cond_expr_str_end = object_name + '.' + key + '<' + str(params[key][1])
            conditions.append(eval(cond_expr_str_start))
            conditions.append(eval(cond_expr_str_end))
    qData = db.session.query(Record.STREET_NAME, Record.MAIN_TYPE_NAME, func.count(Record.MAIN_TYPE_NAME)) \
        .filter(*conditions) \
        .group_by(Record.STREET_NAME, Record.MAIN_TYPE_NAME) \
        .all()

    event_types = ['市容城管', '宣传广告违法行为', '工业噪声', '教育行政管理', '占道经营', '绿化养护', '公用部件', '废弃物堆放']

    # streets_tmp = [item[0] for item in qData]
    # streets = []
    # [streets.append(i) for i in streets_tmp if not i in streets]
    streets = ['龙田街道', '坪山街道', '碧岭街道', '坑梓街道', '马峦街道', '石井街道', '-']
    statistic_for_street = {item[0]: {} for item in qData}
    # streets = [ key for key in statistic_for_street.keys()]
    for item in qData:
        statistic_for_street[item[0]][item[1]] = item[2]
    stat_data = []
    for street in streets:
        tmp = []
        if statistic_for_street.get(street):
            for event_type in event_types:
                if statistic_for_street[street].get(event_type):
                    tmp.append(statistic_for_street[street][event_type])
                else:
                    tmp.append(0)
        else:
            for event_type in event_types:
                tmp.append(0)
        stat_data.append(tmp)

    data = {
        'street_labels': streets,
        'problem_labels': event_types,
        'problem_num': list(map(list, zip(*stat_data))),
    }
    if len(qData) == 0:
        return jsonify(data),404
    return jsonify(data)


# TODO
@app.route('/func3', methods=['GET', 'POST'])
def query_finishEvent_Count():
    if request.method == 'POST':
        start_date_str = request.json.get("date")
    else:
        start_date_str = "2018-10"
    if len(start_date_str.split("-")) == 2:
        start_date_str += '-01'
        d = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = d + relativedelta(months=+1)
    else:
        d = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = d + relativedelta(days=+1)

    end_date_str = end_date.strftime('%Y-%m-%d')
    conditions = []
    params = {'CREATE_TIME': [start_date_str, end_date_str]}
    for key in default_keys:
        if params.get(key):
            if key in str_keys:
                cond_expr_str_start = object_name + '.' + key + '>=' + '\'' + str(params[key][0]) + '\''
                cond_expr_str_end = object_name + '.' + key + '<' + '\'' + str(params[key][1]) + '\''
            else:
                cond_expr_str_start = object_name + '.' + key + '>=' + str(params[key][0])
                cond_expr_str_end = object_name + '.' + key + '<' + str(params[key][1])
            conditions.append(eval(cond_expr_str_start))
            conditions.append(eval(cond_expr_str_end))

    conditions.append(Record.OVERTIME_ARCHIVE_NUM == 1)
    OverTimeVec = db.session.query(Record.EVENT_TYPE_NAME, func.count(Record.EVENT_TYPE_NAME)) \
        .filter(*conditions) \
        .group_by(Record.EVENT_TYPE_NAME) \
        .all()
    conditions.pop()
    conditions.append(Record.INTIME_ARCHIVE_NUM == 1)
    InTimeVec = db.session.query(Record.EVENT_TYPE_NAME, func.count(Record.EVENT_TYPE_NAME)) \
        .filter(*conditions) \
        .group_by(Record.EVENT_TYPE_NAME) \
        .all()
    conditions.pop()
    conditions.append(Record.INTIME_TO_ARCHIVE_NUM == 1)
    inTimetoVec = db.session.query(Record.EVENT_TYPE_NAME, func.count(Record.EVENT_TYPE_NAME)) \
        .filter(*conditions) \
        .group_by(Record.EVENT_TYPE_NAME) \
        .all()
    conditions.pop()

    InTimestat, OverTimestat, InTimetoStat = {label[0]: label[1] for label in InTimeVec}, \
                                             {label[0]: label[1] for label in OverTimeVec}, \
                                             {label[0]: label[1] for label in inTimetoVec}

    events = ['市容环卫', '环保水务', '市政设施', '规土城建', '教育卫生', '安全隐患', '交通运输', '治安维稳']
    labels = ['按期结办', '超期结办', '处置中']
    resp_data = [[InTimestat[event] if InTimestat.get(event) else 0 for event in events],
                 [OverTimestat[event] if OverTimestat.get(event) else 0 for event in events],
                 [InTimetoStat[event] if InTimetoStat.get(event) else 0 for event in events],
                 ]
    data = {
        'archive_type_labels': labels,
        'problem_labels': events,
        'values': resp_data,
        'problem_sum': [sum(row) for row in resp_data],
    }
    if data['problem_sum'][0] == 0 and data['problem_sum'][1] == 0 and data['problem_sum'][2] == 0:
        return jsonify(data),404
    return jsonify(data)


# TODO
@app.route('/func4', methods=['GET', 'POST'])
def query_ByCommunity_Count():
    start_date_str = request.json.get("date")

    if len(start_date_str.split("-")) == 2:
        start_date_str += '-01'
        d = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = d + relativedelta(months=+1)
    else:
        d = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = d + relativedelta(days=+1)

    end_date_str = end_date.strftime('%Y-%m-%d')
    conditions = []
    params = {'CREATE_TIME': [start_date_str, end_date_str]}
    for key in default_keys:
        if params.get(key):
            if key in str_keys:
                cond_expr_str_start = object_name + '.' + key + '>=' + '\'' + str(params[key][0]) + '\''
                cond_expr_str_end = object_name + '.' + key + '<' + '\'' + str(params[key][1]) + '\''
            else:
                cond_expr_str_start = object_name + '.' + key + '>=' + str(params[key][0])
                cond_expr_str_end = object_name + '.' + key + '<' + str(params[key][1])
            conditions.append(eval(cond_expr_str_start))
            conditions.append(eval(cond_expr_str_end))
    qData = db.session.query(Record.COMMUNITY_NAME, func.count(Record.COMMUNITY_NAME)) \
        .filter(*conditions) \
        .group_by(Record.COMMUNITY_NAME) \
        .all()

    labels = [item[0] for item in qData]
    num = [item[1] for item in qData]
    data = {
        'problem_labels': labels,
        'problem_num': num,
    }
    if len(qData) == 0:
        return jsonify(data),404
    return jsonify(data)

@app.route('/func6', methods=['GET', 'POST'])
def function_6():
    if os.path.exists('tmp.csv'):
        os.remove('tmp.csv')
    outpath = os.path.join(os.getcwd(), "tmp.csv")
    outfile = open(outpath, "w", encoding="utf-8", newline="")
    outcsv = csv.writer(outfile)
    header = ['REPORT_NUM', 'EVENT_PROPERTY_NAME', 'EVENT_TYPE_ID', 'EVENT_TYPE_NAME', 'EVENT_SRC_NAME', 'DISTRICT_ID',
              'INTIME_ARCHIVE_NUM', 'SUB_TYPE_ID', 'DISTRICT_NAME', 'COMMUNITY_ID', 'REC_ID', 'STREET_ID',
              'OVERTIME_ARCHIVE_NUM', 'OPERATE_NUM', 'DISPOSE_UNIT_ID', 'STREET_NAME', 'CREATE_TIME', 'EVENT_SRC_ID',
              'INTIME_TO_ARCHIVE_NUM', 'SUB_TYPE_NAME', 'EVENT_PROPERTY_ID', 'OCCUR_PLACE', 'COMMUNITY_NAME',
              'DISPOSE_UNIT_NAME', 'MAIN_TYPE_NAME', 'MAIN_TYPE_ID'
              ]
    outcsv.writerow(header)
    records = db.session.query(Record.REPORT_NUM,
                               Record.EVENT_PROPERTY_NAME,
                               Record.EVENT_TYPE_ID,
                               Record.EVENT_TYPE_NAME,
                               Record.EVENT_SRC_NAME,
                               Record.DISTRICT_ID,
                               Record.INTIME_ARCHIVE_NUM,
                               Record.SUB_TYPE_ID,
                               Record.DISTRICT_NAME,
                               Record.COMMUNITY_ID,
                               Record.REC_ID,
                               Record.STREET_ID,
                               Record.OVERTIME_ARCHIVE_NUM,
                               Record.OPERATE_NUM,
                               Record.DISPOSE_UNIT_ID,
                               Record.STREET_NAME,
                               Record.CREATE_TIME,
                               Record.EVENT_SRC_ID,
                               Record.INTIME_TO_ARCHIVE_NUM,
                               Record.SUB_TYPE_NAME,
                               Record.EVENT_PROPERTY_ID,
                               Record.OCCUR_PLACE,
                               Record.COMMUNITY_NAME,
                               Record.DISPOSE_UNIT_NAME,
                               Record.MAIN_TYPE_NAME,
                               Record.MAIN_TYPE_ID).all()
    for record in records:
        outcsv.writerow([getattr(record, c) for c in header])
    outfile.close()
    data = read_data('tmp.csv')
    if os.path.exists('tmp.csv'):
        os.remove('tmp.csv')
    [value1, value2] = test6(data)
    data = {
        'value1': value1.tolist(),
        'value2': value2.tolist(),
    }

    return jsonify(data)


@app.route('/func7', methods=['GET', 'POST'])
def get_dashboard_charts():
    num_overDue = Record.query.filter(Record.OVERTIME_ARCHIVE_NUM == 1).count()
    num_Done = Record.query.filter(Record.INTIME_ARCHIVE_NUM == 1).count()
    num_inProgress = Record.query.count()-num_overDue-num_Done

    num_all = Record.query.count()

    conditions = []
    conditions.append(Record.OVERTIME_ARCHIVE_NUM == 1)
    OverTimeVec = db.session.query(Record.STREET_NAME, func.count(Record.STREET_NAME)) \
        .filter(*conditions) \
        .group_by(Record.STREET_NAME) \
        .all()
    conditions.pop()
    conditions.append(Record.INTIME_ARCHIVE_NUM == 1)
    InTimeVec = db.session.query(Record.STREET_NAME, func.count(Record.STREET_NAME)) \
        .filter(*conditions) \
        .group_by(Record.STREET_NAME) \
        .all()
    conditions.pop()
    conditions.append(Record.INTIME_TO_ARCHIVE_NUM == 1)
    inTimetoVec = db.session.query(Record.STREET_NAME, func.count(Record.STREET_NAME)) \
        .filter(*conditions) \
        .group_by(Record.STREET_NAME) \
        .all()
    conditions.pop()

    InTimestat, OverTimestat, InTimetoStat = {label[0]: label[1] for label in InTimeVec}, \
                                             {label[0]: label[1] for label in OverTimeVec}, \
                                             {label[0]: label[1] for label in inTimetoVec}

    streets = ['龙田街道', '坪山街道', '碧岭街道', '坑梓街道', '马峦街道', '石井街道', '-']
    labels = ['按期结办', '超期结办', '处置中']
    resp_data = [[InTimestat[street] if InTimestat.get(street) else 0 for street in streets],
                 [OverTimestat[street] if OverTimestat.get(street) else 0 for street in streets],
                 [InTimetoStat[street] if InTimetoStat.get(street) else 0 for street in streets],
                 ]
    top5vec = db.session.query(Record.EVENT_TYPE_NAME, func.count(Record.EVENT_TYPE_NAME)) \
        .group_by(Record.EVENT_TYPE_NAME) \
        .order_by(func.count(Record.EVENT_TYPE_NAME).desc()) \
        .limit(5) \
        .all()
    total = [(InTimestat[street] if InTimestat.get(street) else 0) + (
        OverTimestat[street] if OverTimestat.get(street) else 0) + (
                 InTimetoStat[street] if InTimetoStat.get(street) else 0) for street in streets]
    data = {
        'array1': [num_all, num_Done, num_inProgress, num_overDue],  # [总事件数，已结办，待结办，超期结办]
        'array2': streets,
        'array3': total,  # [每个街道的总事件数]
        'array4': resp_data[0],  # [每个街道的已结办数]
        'array5': [item[0] for item in top5vec],
        'array6': [item[1] for item in top5vec],  # [5类事件数量]
    }
    return jsonify(data)


@app.route('/dashboard/table/dispose_unit', methods=['GET'])
def query_Progess_DisposeUnit():
    OverTimeVec = db.session.query(Record.DISPOSE_UNIT_NAME, func.count(Record.DISPOSE_UNIT_NAME)) \
        .filter(Record.OVERTIME_ARCHIVE_NUM == 1) \
        .group_by(Record.DISPOSE_UNIT_NAME) \
        .order_by(func.count(Record.DISPOSE_UNIT_NAME).desc()) \
        .limit(5) \
        .all()
    OverTimeDict = {item[0]: item[1] for item in OverTimeVec}
    top5DisposeUnit = [item[0] for item in OverTimeVec]
    TotalVec = db.session.query(Record.DISPOSE_UNIT_NAME, func.count(Record.DISPOSE_UNIT_NAME)) \
        .filter(or_(Record.DISPOSE_UNIT_NAME == name for name in top5DisposeUnit)) \
        .group_by(Record.DISPOSE_UNIT_NAME) \
        .all()
    TotalDict = {item[0]: item[1] for item in TotalVec}
    LastTimeProcess = db.session.query(Record.DISPOSE_UNIT_NAME, func.max(Record.CREATE_TIME)) \
        .filter(Record.INTIME_ARCHIVE_NUM == 1) \
        .filter(or_(Record.DISPOSE_UNIT_NAME == name for name in top5DisposeUnit)) \
        .group_by(Record.DISPOSE_UNIT_NAME) \
        .order_by(func.max(Record.CREATE_TIME).desc()) \
        .all()
    LastTimeDict = {item[0]: item[1].strftime("%Y-%m-%d %H:%M") for item in LastTimeProcess}

    ranking = [{'name': name, 'last_process': LastTimeDict[name], 'OvertimeCount': OverTimeDict[name],
                'Progess_percentage': math.ceil(OverTimeDict[name] / (TotalDict[name] + 1) * 100)} for name in
               top5DisposeUnit]

    return jsonify(ranking)


@app.route('/dashboard/table/recent_event', methods=['GET', 'POST'])
def query_Progess_recentEvent():
    recent_event = db.session.query(Record.REC_ID, Record.CREATE_TIME, Record.MAIN_TYPE_NAME,
                                    Record.OVERTIME_ARCHIVE_NUM, Record.INTIME_ARCHIVE_NUM,
                                    Record.INTIME_TO_ARCHIVE_NUM) \
        .order_by(Record.CREATE_TIME.desc()) \
        .limit(5) \
        .all()

    ranking = [{'id': item[0], 'create_time': item[1].strftime("%Y-%m-%d %H:%M"), 'main_type': item[2],
                'status': '已超期' if item[3] else '处理完毕' if item[4] else '处理中'} for item in
               recent_event]

    return jsonify(ranking)


@app.route('/dashboard/timeline', methods=['GET', 'POST'])
def query_timeline():
    recent_event = db.session.query(Record.REC_ID, Record.CREATE_TIME, Record.MAIN_TYPE_NAME,
                                    Record.INTIME_TO_ARCHIVE_NUM, Record.OVERTIME_ARCHIVE_NUM, Record.STREET_NAME) \
        .filter(or_(Record.INTIME_TO_ARCHIVE_NUM == 1, Record.OVERTIME_ARCHIVE_NUM == 1)) \
        .order_by(Record.CREATE_TIME.desc()) \
        .limit(3) \
        .all()
    ret_data = [{'timeString': item[1].strftime("%Y-%m-%d %H:%M"), 'title': item[0],
                 'text': item[-1] + '的' + item[2] + '事件' + ' 超期' if item[4] else ' 等待结办',
                 'color': 'primary' if item[3] else 'warning'} for item in recent_event]
    return jsonify(ret_data)


@app.route('/func5', methods=['GET', 'POST'])
def function_5():
    if os.path.exists('tmp.csv'):
        os.remove('tmp.csv')
    outpath = os.path.join(os.getcwd(), "tmp.csv")
    outfile = open(outpath, "w", encoding="utf-8", newline="")

    outcsv = csv.writer(outfile)
    header = ['REPORT_NUM', 'EVENT_PROPERTY_NAME', 'EVENT_TYPE_ID', 'EVENT_TYPE_NAME', 'EVENT_SRC_NAME', 'DISTRICT_ID',
              'INTIME_ARCHIVE_NUM', 'SUB_TYPE_ID', 'DISTRICT_NAME', 'COMMUNITY_ID', 'REC_ID', 'STREET_ID',
              'OVERTIME_ARCHIVE_NUM', 'OPERATE_NUM', 'DISPOSE_UNIT_ID', 'STREET_NAME', 'CREATE_TIME', 'EVENT_SRC_ID',
              'INTIME_TO_ARCHIVE_NUM', 'SUB_TYPE_NAME', 'EVENT_PROPERTY_ID', 'OCCUR_PLACE', 'COMMUNITY_NAME',
              'DISPOSE_UNIT_NAME', 'MAIN_TYPE_NAME', 'MAIN_TYPE_ID'
              ]
    outcsv.writerow(header)
    records = db.session.query(Record.REPORT_NUM,
                               Record.EVENT_PROPERTY_NAME,
                               Record.EVENT_TYPE_ID,
                               Record.EVENT_TYPE_NAME,
                               Record.EVENT_SRC_NAME,
                               Record.DISTRICT_ID,
                               Record.INTIME_ARCHIVE_NUM,
                               Record.SUB_TYPE_ID,
                               Record.DISTRICT_NAME,
                               Record.COMMUNITY_ID,
                               Record.REC_ID,
                               Record.STREET_ID,
                               Record.OVERTIME_ARCHIVE_NUM,
                               Record.OPERATE_NUM,
                               Record.DISPOSE_UNIT_ID,
                               Record.STREET_NAME,
                               Record.CREATE_TIME,
                               Record.EVENT_SRC_ID,
                               Record.INTIME_TO_ARCHIVE_NUM,
                               Record.SUB_TYPE_NAME,
                               Record.EVENT_PROPERTY_ID,
                               Record.OCCUR_PLACE,
                               Record.COMMUNITY_NAME,
                               Record.DISPOSE_UNIT_NAME,
                               Record.MAIN_TYPE_NAME,
                               Record.MAIN_TYPE_ID).all()
    for record in records:
        outcsv.writerow([getattr(record, c) for c in header])
    outfile.close()

    data = read_data('tmp.csv')
    if os.path.exists('tmp.csv'):
        os.remove('tmp.csv')
    events = test5(data)
    data = {
        'events': events,
    }
    if len(data['events']) == 0:
        return jsonify(data),404
    return jsonify(data)


@app.route('/fileupload', methods=['GET','POST'])
def importCSV():
    header = Record.__table__.columns.keys()
    file = request.files['file']
    file.save(os.path.join(os.getcwd(),file.filename))
    # try:
    with open(file.filename, encoding='gbk') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            data.append(row)
        resp = {
            'status': 'success',
            'data': data
        }
    # except:
    #     return {  }, status.HTTP_400_BAD_REQUEST
    return resp

def convert_time(time_str):
    is_pm = time_str[-2:].lower() == 'pm'
    time_list = list(map(int, time_str[:-2].split(':')))

    if is_pm and time_list[0] < 12:
        time_list[0] += 12

    if not is_pm and time_list[0] == 12:
        time_list[0] = 0

    return ':'.join(map(lambda x: str(x).rjust(2, '0'), time_list))

@app.route('/confirm', methods=['GET','POST'])
def confirm_import():
    data = request.json
    entries = []
    for item in data:
        rec = Record(**item)
        timestr = rec.CREATE_TIME.split(" ")
        ampm = 'AM' if timestr[1][:1] == '上午' else 'PM'
        new_timestr = timestr[1][2:] + ampm
        new_timestr = timestr[0] + ' ' + convert_time(new_timestr)
        rec.CREATE_TIME = datetime.datetime.strptime(new_timestr, '%Y/%m/%d %H:%M:%S')
        db.session.add(rec)
    # TODO: Record的内部转换（类型）
    db.session.commit()

    resp = { 'status': 'success'}
    return resp


@app.route('/query_conditional', methods=['GET','POST'])
def query_conditional():
    conditions = request.json
    print(conditions)
    retData = Record.query.filter(Record.REC_ID == int(conditions['id'])).all()
    data = {}
    data['tableData'] = retData
    return jsonify({ 'data': data, 'status':'success'})

@app.route('/confirm_modify', methods=['GET','POST'])
def confirm_modify():
    data = request.json
    entries = []
    for item in data:
        rec = Record(**item)
        timestr = rec.CREATE_TIME.split(" ")
        ampm = 'AM' if timestr[1][:1] == '上午' else 'PM'
        new_timestr = timestr[1][2:] + ampm
        new_timestr = timestr[0] + ' ' + convert_time(new_timestr)
        rec.CREATE_TIME = datetime.datetime.strptime(new_timestr, '%Y/%m/%d %H:%M:%S')
        origin = session.query.filter(Record.REC_ID == int(rec.REC_ID)).first()
        setattr(origin, Record.INTIME_TO_ARCHIVE_NUM, 0)
        setattr(origin, Record.INTIME_ARCHIVE_NUM, 1)
        setattr(origin, Record.OVERTIME_ARCHIVE_NUM,0)
        db.session.commit()
    # TODO: Record的内部转换（类型）


    resp = {'status': 'success'}
    return resp
    retData = Record.query.filter(Record.REC_ID == int(conditions['id'])).all()

    return { 'data': retData, 'status':'success'}

class Account(db.Model, UserMixin):
    __tablename__ = 'user_data'
    id = db.Column(db.String(255), nullable=False, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    authority = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password, id, authority, phone, email):
        self.id = id
        self.username = username
        self.password = password
        self.authority = authority
        self.email = email
        self.phone = phone


def query_user(user_id):
    check_id = Account.query.filter(Account.id == user_id).first()
    if check_id:
        return check_id


@login_manager.user_loader
def load_user(user_id):
    # if query_user(user_id) is not None:
    #     curr_user = Account()
    #     curr_user.id = user_id
    #     return curr_user
    user = Account.query.get(user_id)
    return user


def get_account(username):
    res = Account.query.filter(Account.username == username).first()
    return res


def insert_account(username, password, phone, email, authority=0):
    account = Account(username=username, password=password, id=username, authority=authority, phone=phone, email=email)
    db.session.add(account)
    db.session.commit()


def updata_authority(username, new_auth):
    try:
        Account.query.filter_by(username=username).update({Account.authority: new_auth})
        db.session.commit()
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        db.session.rollback()
        raise e


def updata_password(username, newpassword):
    try:
        Account.query.filter_by(username=username).update({Account.password: newpassword})
        db.session.commit()
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        db.session.rollback()
        raise e


def updata_info(username, newphone, newemail):
    try:
        Account.query.filter_by(username=username).update({Account.phone: newphone})
        db.session.commit()
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        db.session.rollback()
        raise e

    try:
        Account.query.filter_by(username=username).update({Account.email: newemail})
        db.session.commit()
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        db.session.rollback()
        raise e


@app.route('/login/', methods=["POST"])
def login():
    username = request.form.get("username")
    pswrd = request.form.get("password")
    print(username, pswrd)
    md5 = hashlib.md5()

    cur_user = Account.query.first()
    if username and pswrd and cur_user:
        res = get_account(username)
        if res:
            if res.password == pswrd:
                username = username + res.authority
                username = username.encode(encoding='utf-8')
                md5.update(username)
                token = md5.hexdigest()
                # login_user(cur_user, username)
                return jsonify({"code": 200, "token": token})
    return jsonify({"code": 400})


@app.route('/register/', methods=["POST"])
def register():
    username = request.form.get("username")
    pswrd = request.form.get("password")
    pswrd_ck = request.form.get("pswrd_ck")
    authority = request.form.get("authority")
    phone = request.form.get("phone")
    email = request.form.get("email")
    dic = {"username": username, "password": pswrd}
    print(dic)
    if username == '' or pswrd == '' or phone == '' or email == '':
        return jsonify({'code': 500})
    elif get_account(username):
        return jsonify({'code': 300})
    elif username and pswrd and pswrd == pswrd_ck:
        insert_account(username, pswrd, phone, email, authority)
        return jsonify({'code': 200})
    else:
        return jsonify({'code': 400,
                        'account': dic})


@app.route('/accountmanage/')
def get_data():
    users = Account.query.filter().all()
    userlist = []
    auth = {'1': '职工', '2': '管理员', '3': '超级用户'}
    for item in users:
        idic = {}
        idic['id'] = item.id
        idic['username'] = item.username
        idic['authority'] = auth[item.authority]
        idic['phone'] = item.phone
        idic['email'] = item.email
        userlist.append(idic)
    res = {'code': 200, 'data': userlist}
    # print(res)
    return res


@app.route('/authoritychange/', methods=["POST"])
def change_authority():
    data = request.get_json(silent=True)
    users = data['user']
    value = data['value']
    cur_user = data['curuser']
    if users and value:
        for user in users:
            if get_account(user['username']).authority < get_account(cur_user).authority:
                updata_authority(user['username'], value)
        return {'code': 200}
    else:
        return {'code': 400}


@app.route('/passwordchange/', methods=["POST"])
def change_password():
    data = request.get_json(silent=True)
    oldpassword = data['oldpassword']
    newpassword = data['newpassword']
    newpasswordck = data['newpasswordck']
    cur_user = data['curuser']
    if cur_user and oldpassword and newpassword and newpasswordck:
        if get_account(cur_user).password == oldpassword:
            if newpassword == newpasswordck:
                updata_password(username=cur_user, newpassword=newpassword)
                return {'code': 200}
            else:
                return {'code': 300}
        else:
            return {'code': 301}
    else:
        return {'code': 400}


@app.route('/infochange/', methods=["POST"])
def change_info():
    data = request.get_json(silent=True)
    newphone = data['phone']
    newemail = data['email']
    cur_user = data['user']
    updata_info(cur_user, newphone, newemail)
    return {'code': 200}


@app.route('/passwordck/', methods=['POST'])
def password_ck():
    data = request.get_json(silent=True)
    print(data)
    username = data['username']
    pswrdck = data['passwordck']
    token = data['token']
    ckuser = get_account(username)
    if ckuser:
        if ckuser.authority != '3':
            return {'code': 300}
        if ckuser and ckuser.password == pswrdck:
            return {'code': 200}
        else:
            return {'code': 400}
    else:
        return {'code': 300}


@app.route('/getuser/', methods=['POST'])
def get_user():
    data = request.get_json(silent=True)
    user = get_account(data['user'])
    userinfo = {}
    auth = {'1': '职工', '2': '管理员', '3': '超级用户'}
    userinfo['username'] = user.username
    userinfo['authority'] = auth[user.authority]
    userinfo['phone'] = user.phone
    userinfo['email'] = user.email
    return {'code': 200, 'data': userinfo}


if __name__ == '__main__':
    app.run()
