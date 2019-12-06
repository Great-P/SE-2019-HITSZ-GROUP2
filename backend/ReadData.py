import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 绘制扇形图
def draw_pie(values, labels, colors=None):
    # 中文乱码和坐标轴负号的处理
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.style.use('ggplot')
    # if colors == None:
    #     colors = ['#9999ff', '#ff9999', '#7777aa', '#2442aa', '#dd5555']  # 定义颜色

    # 将横、纵坐标轴标准化处理，保证饼图是一个正圆，否则为椭圆
    plt.axes(aspect='equal')

    plt.pie(x=values,
            labels=labels,
            labeldistance=1.1,
            colors=colors,
            autopct='%.2f%%',  # 设置百分比的格式，这里保留2位小数
            pctdistance=0.8,  # 设置百分比标签与圆心的距离
            startangle=0.8,  # 设置饼图的初始角度
            radius=1.5,  # 设置饼图的半径
            counterclock=False,  # 是否逆时针，这里设置为顺时针方向
            wedgeprops={'linewidth': 1.5, 'edgecolor': 'green'},  # 设置饼图内外边界的属性值
            textprops={'fontsize': 12, 'color': 'k'},  # 设置文本标签的属性值
            center=(1.8, 1.8),  # 设置饼图的原点

            )
    plt.legend(loc='upper left', bbox_to_anchor=(0.1, 0.05), borderaxespad=0.1)
    plt.show()

# 绘制堆叠柱状图
def draw_stackedHist(values, streets, types):
    # 中文乱码和坐标轴负号的处理
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.style.use('ggplot')

    N = len(streets)
    width = 0.35
    ind = np.arange(N) # 间隔
    plt.bar(ind, values[:, 0], width)
    for i in range(1, len(types)):
        plt.bar(ind, values[:, i], width, bottom=values[:, i - 1])
    plt.xticks(ind, streets)
    plt.show()

# 去除为0的值和对应的类型，绘图时省略
def remove_zero(values, labels):
    new_values = []
    new_labels = []
    for k, v in enumerate(values):  # k和v分别表示org中的下标和该下标对应的元素
        if v != 0:
            new_values.append(values[k])
            new_labels.append(labels[k])
    return new_values, new_labels

# 根据用户选择的时间提取数据
def filter_by_time(data, date='2018-07'):
    # date = input("请输入年月：(格式如2018-07):")
    # date = '2018-07'
    rows = data.CREATE_TIME.str.contains(date)
    filter_data = data[rows]
    print('事件总数:', len(filter_data))
    if len(filter_data)==0:
        print("没有这个日期的信息！")
        exit(-1)
    return filter_data

# 展示指定日期的不同问题性质的问题数目，扇形图
def test1(data, date):
    filter_data = filter_by_time(data, date)
    # pd.set_option('display.max_rowsfilter_data = filter_by_time(data)',100)
    # print(filter_data.EVENT_PROPERTY_NAME)

    types = ['投诉', '感谢', '建议', '咨询', '求决', '-']

    i = 0
    values = np.zeros(len(types))
    for type in types:
        # values[i] = sum(filter_data.EVENT_PROPERTY_NAME.str.contains(type)) / len(filter_data)
        values[i] = sum(filter_data.EVENT_PROPERTY_NAME.str.contains(type))
        i = i + 1
    # print(sum(values))

    # 去除值为0的和其对应标签，作图时不画
    # print(values!=0)
    [nv, nl] = remove_zero(values, types)
    # print(nv)
    # print(nl)
    # draw_pie(nv, nl)
    return nv, nl

# 展示今日和特定月份下的各街道民生事件情况，
# 横坐标为“所属街道”，纵坐标为“事件数目”，色块为“小类名称”
# 堆叠直方图
def test2(data, date):
    filter_data = filter_by_time(data, date)

    pd.set_option('display.max_rows',100)
    streets = ['龙田街道', '坪山街道', '碧岭街道', '坑梓街道', '马峦街道', '石井街道', '-']
    types = ['市容城管', '禽畜养殖污染', '市政、公共设施设置及维护', '商业经营噪声',
              '城乡规划', '房屋征收', '宣传广告违法行为', '工业噪声', '教育行政管理',
              '占道经营', '垃圾问题', '绿化养护', '公用部件', '交通设施', '废弃物堆放',
              '道路交通安全', '车辆乱停放', '社会生活噪声', '道路保洁', '医患纠纷',
              '人力资源', '行政效能', '医政监管', '道路设施', '水污染', '招生中的违法行为',
              '教育体制', '城市建设和市政管理', '其他市容违法行为或影响市容事件', '劳动就业',
              '经济纠纷', '建设工程质量', '渣土问题', '公共交通管理', '城市公共资源管理',
              '服务行业废气扰民', '人口房屋', '住房保障和房地产', '违法建筑与用地行为',
              '交通管理', '教育收费', '工业、住宅废气扰民', '违反计生政策', '工商经济联络',
              '交通运输噪声', '建筑市场', '建筑消防安全', '危险化学品安全',
              '住宅区（园区）或建筑物内安全、环卫问题', '医疗机构违规经营',
              '集体土地上房屋拆迁与补偿', '扬尘污染', '教学违规', '环保管理',
              '劳动社保', '物业服务管理监督', '医疗机构违规收费', '药品（医疗器械）监管',
              '面源污染隐患', '供、排水及水质问题', '党的建设', '刑案侦破', '公共设施保洁',
              '社区公共管理']

    # for name in filter_data.MAIN_TYPE_NAME:
    #     if name not in types:
    #         types.append(name)
    # print(types)

    # r1 = filter_data.STREET_NAME.str.contains('龙田街道')
    # text = filter_data.MAIN_TYPE_NAME.str.match('公共交通管理')
    # text2 = filter_data.MAIN_TYPE_NAME.str.contains('公共交通管理')
    # print(sum(text))
    # print(sum(text2))
    # count = 0
    #     # for type in types:
    #     #     r2 = filter_data.MAIN_TYPE_NAME.str.match(type) # 会有重复，交通管理和公共交通管理
    #     #     print(type,':',sum(r1&r2))
    #     #     count = count+sum(r1&r2)
    #     # print(sum(r1))
    #     # print(count)

    i = 0
    j = 0
    values = np.zeros((len(streets), len(types)))
    print(len(types))
    for street in streets:
        r1 = filter_data.STREET_NAME.str.match(street)
        j = 0
        for type in types:
            r2 = filter_data.MAIN_TYPE_NAME.str.match(type)
            values[i][j] = sum(r1&r2) # bool数组取交集
            j = j+1
        i = i + 1

    # 绘制堆叠柱状图
    # draw_stackedHist(values, streets, types)
    most = [0,6,7,8,9,11,12,14]
    new_types = []
    new_values = np.zeros((len(streets), len(most)))
    # v2 = sum(values)
    new_values = values[:, most]
    # print(new_values[:, 7])
    # print(sum(new_values))
    for i in most:
        # print(types[i])
        new_types.append(types[i])
    # return new_values.T

    return new_values.T, streets, new_types

# 结办情况记录
def test3(data, date):
    filter_data = filter_by_time(data, date)

    # print(sum(filter_data['INTIME_TO_ARCHIVE_NUM']))
    index = [3178, 3742, 6741, 8018, 9697] # 5个'-'的下标

    types = ['市容环卫', '环保水务', '市政设施', '规土城建', '教育卫生',
             '安全隐患', '组织人事', '党纪政纪', '劳动社保', '社区管理',
             '交通运输', '治安维稳', '专业事件采集', '统一战线', '民政服务',
             '文体旅游', '食药市监', '党建群团']
    archive_types = ['0', '1', '-'] # 三类结办情况
    values = np.zeros((3, len(types)))

    i=0
    j=0
    for archive_type in archive_types:
        t1 = filter_data.OVERTIME_ARCHIVE_NUM.str.match(archive_type)
        j=0
        for type in types:
            t2 = filter_data.EVENT_TYPE_NAME.str.match(type)
            values[i][j] = sum(t1&t2)
            j = j+1
        i=i+1

    # print(sum(sum(values)))
    # print(values[2][2])
    archive_types_name = ['按期结办', '超期结办', '处置中']
    most = [0,1,2,3,4,5,10]
    new_values = values[:, most]
    new_types = []
    for i in most:
        # print(types[i])
        new_types.append(types[i])
    # draw_stackedHist(values, archive_types, types)
    # return values
    row_sums = np.sum(new_values, axis=1)
    col_sums = np.sum(new_values, axis=0)
    # print(sums)
    return col_sums, archive_types_name, new_types, row_sums

# 结办情况记录
def test33(data, date):
    filter_data = filter_by_time(data, date)

    # print(sum(filter_data['INTIME_TO_ARCHIVE_NUM']))
    index = [3178, 3742, 6741, 8018, 9697] # 5个'-'的下标

    types = ['市容环卫', '环保水务', '市政设施', '规土城建', '教育卫生',
             '安全隐患', '组织人事', '党纪政纪', '劳动社保', '社区管理',
             '交通运输', '治安维稳', '专业事件采集', '统一战线', '民政服务',
             '文体旅游', '食药市监', '党建群团']
    archive_types = ['0', '1', '-'] # 三类结办情况
    values = np.zeros((3, len(types)))

    i=0
    j=0
    for archive_type in archive_types:
        t1 = filter_data.OVERTIME_ARCHIVE_NUM.str.match(archive_type)
        j=0
        for type in types:
            t2 = filter_data.EVENT_TYPE_NAME.str.match(type)
            values[i][j] = sum(t1&t2)
            j = j+1
        i=i+1

    # print(sum(sum(values)))
    # print(values[2][2])
    archive_types_name = ['按期结办', '超期结办', '处置中']
    most = [0,1,2,3,4,5,10,11]
    new_values = values[:, most]
    new_types = []
    for i in most:
        # print(types[i])
        new_types.append(types[i])
    # draw_stackedHist(values, archive_types, types)
    # return values
    row_sums = np.sum(new_values, axis=1)
    for i in range(2):
        new_values[i, 7] = row_sums[i] - np.sum(new_values[i, 0:5])
    new_values[2, 7] = row_sums[2] - np.sum(new_values[2, 0:3])
    col_sums = np.sum(new_values, axis=0)
    # print(sums)
    return new_values, archive_types_name, new_types, row_sums

# 热点社区分析
def test4(data, date):
    filter_data = filter_by_time(data, date)

    communities = ['南布社区', '和平社区', '坪山社区', '汤坑社区',
                   '金沙社区', '江岭社区', '石井社区', '六和社区',
                   '沙湖社区', '老坑社区', '竹坑社区', '秀新社区',
                   '沙田社区', '六联社区', '坪环社区', '龙田社区',
                   '坑梓社区', '沙坣社区', '田头社区', '田心社区',
                   '碧岭社区', '-', '金龟社区', '马峦社区']

    values = np.zeros(len(communities))
    i=0
    for community in communities:
        values[i] = sum(filter_data.COMMUNITY_NAME.str.match(community))
        i=i+1

    # draw_pie(values, communities)
    filter = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23]
    new_values = values[filter]
    communities.remove('-')
    return new_values, communities

# 异常事件预警
def test5(data, date = '2018-10-30'):
    '''
    2018年10月30日坑梓街道的秀新社区从12319接到商业经营红线内噪声投诉，
    请城管办（坑梓街道办事处）尽快前往处理。
    '''
    org_data = data
    data = filter_by_time(data, date)


    emergency_index = sortByPriority(org_data, data)
    emergency_list = []
    # timeToStr(time[time.keys()[0]])
    # print(time.keys())

    for i in emergency_index:
        # print(event)
        # print(i)
        info = data.loc[data['REC_ID'] == i]
        time = info['CREATE_TIME'].iloc[0]
        street = info['STREET_NAME'].iloc[0]
        community = info['COMMUNITY_NAME'].iloc[0]
        eventsrc = info['EVENT_SRC_NAME'].iloc[0]
        subtype = info['SUB_TYPE_NAME'].iloc[0]
        eventtype = info['EVENT_PROPERTY_NAME'].iloc[0]
        unit = info['DISPOSE_UNIT_NAME'].iloc[0]

        # print(time)
        # print(street)
        formattime = timeToStr(time)

        info_list = []
        info_list.append(formattime)
        info_list.append(street)
        info_list.append(community)
        info_list.append(eventsrc)
        info_list.append(subtype)
        info_list.append(eventtype)
        info_list.append(unit)

        # info_list =  formattime + street + '的' + community + '从' + eventsrc + '接到' + subtype + eventtype + ',请' + unit + '尽快前往处理'

        # print(info_list)
        emergency_list.append(info_list)
        # print(info)
    return emergency_list,

# timeline扩展动态图
def test6(data):
    '''
    201807:[按街道统计]
    201808:[按街道统计]
    '''
    streets = ['龙田街道', '坪山街道', '碧岭街道', '坑梓街道', '马峦街道', '石井街道', '-']
    types = ['投诉']
    dates = ['2018-07','2018-08','2018-09','2018-10']
    i = 0
    j = 0
    values1 = np.zeros((len(dates), len(streets)), dtype=int) #投诉
    values2 = np.zeros((len(dates), len(streets)), dtype=int) #非投诉
    # print(len(types))
    for date in dates:
        j = 0
        filter_data = filter_by_time(data, date)
        for street in streets:
            r1 = filter_data.STREET_NAME.str.match(street)
            r2 = filter_data.EVENT_PROPERTY_NAME.str.match(types[0])
            values1[i][j] = sum(r1 & r2)  # bool数组取交集
            values2[i][j] = sum(r1) - values1[i][j]
            j = j + 1
        i = i + 1

    return values1, values2

# 将时间标准化
def timeToStr(time):
    return time[0:4]+'年'+str(int(time[5:7]))+'月'+str(int(time[8:10]))+'日'

# 按照优先级对时间排序
def sortByPriority(org_data, data):
    # 1、按subtype自定义
    # 2、按时间，越早越优先
    # 3、

    all_events = list(org_data.groupby('SUB_TYPE_ID'))
    # print(all_events[1][1])

    over_time = {}
    for one_type_event in all_events:

        even = one_type_event[1]
        # print(type(even))
        tousu = list(even.groupby('EVENT_PROPERTY_NAME'))
        over = list(even.groupby('OVERTIME_ARCHIVE_NUM'))

        ts = 0
        for leixing in tousu:
            if (leixing[0] == '投诉'):
                ts = leixing[1].shape[0]
            # state = (超时数，及时率，超时率， 投诉率)
            state = [-1, -1, -1, -1]

            if len(over) == 3:
                overtime = over[2][1]
                state[0] = overtime.shape[0]
                state[1] = over[1][1].shape[0]
            elif len(over) == 2:
                # 如果有超时
                overtime = over[1][1]
                state[0] = overtime.shape[0]
                state[1] = over[0][1].shape[0]
            else:
                state[0] = 0
                state[1] = over[0][1].shape[0]

                # over time rate

            # state[1] = ts * 1.0 /even.shape[0]
            state[2] = 1 - (state[1] * 1.0 / even.shape[0])
            state[3] = ts * 1.0 / even.shape[0]
            over_time[str(one_type_event[0])] = state


    data_list = list(data.groupby('REC_ID'))
    data_list.sort(key=lambda x:(0.2*(over_time[str(x[1].iloc[0][7])][2])/(0.93)+0.8*(over_time[str(x[1].iloc[0][7])][3])),reverse=True)
    emergency_list = []
    for i in range(10):
        emergency_list.append(data_list[i][0])
    # print(emergency_list)
    return emergency_list


def read_data(path):
    data = pd.read_csv(path, encoding='utf-8')
    # print(data.shape)
    data = pd.DataFrame(data)
    return data

# 推送数据
def push_data(before_today_data, after_today_data, index, k):

    i, s = index[k]
    # print(before_today_data.shape)
    # print(pd.DataFrame(data.iloc[i]).T)
    before_today_data = pd.concat([before_today_data, pd.DataFrame(data.iloc[i]).T], ignore_index=True)
    # print(before_today_data.shape)
    return before_today_data

# 筛选数据
def filter_data_today(data, today='2018-10-30'):
    rows = np.zeros(10000, dtype=bool)
    rows_after = np.zeros(10000, dtype=bool)
    index = {}
    i = 0
    for date_org in data.CREATE_TIME:
        # print(date_org)
        date = date_org.split('-')
        if int(date[1])<10 or (int(date[1])==10 and int(date[2][:2])<30):
            rows[i] = True
            rows_after[i] = False
        else:
            rows[i] = False
            rows_after[i] = True
            con = ''.join(date).split(' ')[0]+''.join(''.join(date).split(' ')[1].split(':'))
            index[i] = int(con)
        i = i+1

    index = sorted(index.items(), key=lambda x:x[1])
    # print(index)
    before_today_data = data[rows]
    after_today_data = data[rows_after]
    # print(after_today)
    # print('事件总数:', len(filter_data))

    return before_today_data, after_today_data, index

# def sortbydate(data):


if __name__ == '__main__':

    data = read_data('test.csv')

    # data = pd.read_csv('test.csv', encoding='gbk')
    print(data.shape)

    col_names = data.columns
    # print(col_names)

    # before_today_data, after_today_data, index = filter_data_today(data)
    # push_data(before_today_data, after_today_data, index, 0)
    # i,s = index[0]
    # print(before_today_data.shape)
    # before_today_data.append(pd.DataFrame(data.iloc[i]))
    # print(pd.DataFrame(data.iloc[i]).T)
    # before_today_data = pd.concat([before_today_data, pd.DataFrame(data.iloc[i]).T], ignore_index=True)
    # print(before_today_data.shape)
    # sortbydate(after_today_data)
    # print(type(before_today_data))
    # test1(data)
    # values = test2(data, '2018-07')

    # test3(data, '2018-07')
    new_values, archive_types_name, new_types, row_sums = test33(data, '2018-07')
    print(new_values)
    print(row_sums)
    # test4(data, '2018-07')

    # ee = test5(data)
    # print(ee)
    # print(values)
    # [values, labels] = test1(data)
    # new_labels = ['其它' if x=='-' else x for x in labels]
    #
    # print(labels)
    # print(new_labels)

    # v1, v2 = test6(data)
    # print(v1)
    # print('*******************************')
    # print(v1[0])
