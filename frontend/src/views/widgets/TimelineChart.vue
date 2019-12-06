<template>
    <div>
        <el-card class="box-card">
          <vue-element-loading :active="this.isActive" spinner="mini-spinner" color="#FF6700"/>
            <div id="myChart" :style="{width: '100%', height: '500px'}"></div>
        </el-card>
    </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios'

var echarts = require('echarts');

export default {
    name: "TimelineChart",
    data() {
        return {
            value: '',
            dataMap: {},
            isActive: true,
        }
    },
    mounted() {
        // this.$nextTick(() => {
            //作图
            this.filldata();
        // });
    },
    created() {
        //获取数据
        // this.filldata();
    },
    methods: {
        filldata() {
            //绘制图片
            axios.get("http://localhost:5000/func6")
                .then((res) => {
                    this.preprocess(res);
                    this.process(res);
                    this.isActive = false;
                })
        },
        dataFormatter(obj) {
            var pList = ['龙田街道', '坪山街道', '碧岭街道', '坑梓街道', '马峦街道', '石井街道'];
            var temp;
            for (var ym = 201807; ym <= 201810; ym++) {
                var max = 0;
                var sum = 0;
                temp = obj[ym];
                for (var i = 0, l = temp.length; i < l; i++) {
                    max = Math.max(max, temp[i]);
                    sum += temp[i];
                    obj[ym][i] = {
                        name : pList[i],
                        value : temp[i]
                    }
                }
                obj[ym + 'max'] = Math.floor(max / 100) * 100;
                obj[ym + 'sum'] = sum;
            }
            return obj;
        },
        preprocess(res) {
            const result = res.data;
            this.dataMap.dataType1 = this.dataFormatter({
                201807:result.value1[0],
                201808:result.value1[1],
                201809:result.value1[2],
                201810:result.value1[3],
            });
            this.dataMap.dataType2 = this.dataFormatter({
                201807:result.value2[0],
                201808:result.value2[1],
                201809:result.value2[2],
                201810:result.value2[3],
            });
        },
        process(res) {
            const result = res.data;
            //初始化实例
            let timelineChart = echarts.init(document.getElementById('myChart'));
            timelineChart.setOption({
                baseOption: {
                    timeline: {
                        // y: 0,
                        axisType: 'category',
                        // realtime: false,
                        // loop: false,
                        autoPlay: true,
                        // currentIndex: 2,
                        playInterval: 1000,
                        // controlStyle: {
                        //     position: 'left'
                        // },
                        data: [
                            '2018-07','2018-08','2018-09',
                            {
                                value: '2018-10',
                                tooltip: {
                                    formatter: '{b} 到现在'
                                },
                                symbol: 'diamond',
                                symbolSize: 16
                            },
                        ],
                        label: {
                            formatter : function(s) {
                                return (new Date(s)).getFullYear()+"-"+((new Date(s)).getMonth()+1);
                            }
                        }
                    },
                    title: {
                        // subtext: '数据来自项目'
                    },
                    tooltip: {},
                    legend: {
                        x: 'right',
                        data: ['投诉事件', '非投诉事件'],
                    },
                    calculable : true,
                    grid: {
                        top: 80,
                        bottom: 100
                    },
                    xAxis: [
                        {
                            'type':'category',
                            'axisLabel':{'interval':0},
                            'data':[
                                '龙田街道', '坪山街道', '碧岭街道', '坑梓街道', '马峦街道', '石井街道',
                            ],
                            splitLine: {show: false}
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '事件数目',
                            // max: 53500
                            max: 1000
                        }
                    ],
                    series: [
                        {name: '投诉事件', type: 'bar'},
                        {name: '非投诉事件', type: 'bar'},
                        {
                            name: '投诉事件占比',
                            type: 'pie',
                            center: ['75%', '35%'],
                            radius: '28%'
                        }
                    ]
                },
                options: [
                    {
                        title: {text: "2018年7月街道事件情况统计"},
                        series: [
                            {data: this.dataMap.dataType1['201807']},
                            {data: this.dataMap.dataType2['201807']},
                            {data: [
                                {name: '投诉事件', value: this.dataMap.dataType1['201807sum']},
                                {name: '非投诉事件', value: this.dataMap.dataType2['201807sum']},
                            ]}
                        ]
                    },
                    {
                        title: {text: "2018年8月街道事件情况统计"},
                        series: [
                            {data: this.dataMap.dataType1['201808']},
                            {data: this.dataMap.dataType2['201808']},
                            {data: [
                                {name: '投诉事件', value: this.dataMap.dataType1['201808sum']},
                                {name: '非投诉事件', value: this.dataMap.dataType2['201808sum']},
                            ]}
                        ]
                    },
                    {
                        title: {text: "2018年9月街道事件情况统计"},
                        series: [
                            {data: this.dataMap.dataType1['201809']},
                            {data: this.dataMap.dataType2['201809']},
                            {data: [
                                {name: '投诉事件', value: this.dataMap.dataType1['201809sum']},
                                {name: '非投诉事件', value: this.dataMap.dataType2['201809sum']},
                            ]}
                        ]
                    },
                    {
                        title: {text: "2018年10月街道事件情况统计"},
                        series: [
                            {data: this.dataMap.dataType1['201810']},
                            {data: this.dataMap.dataType2['201810']},
                            {data: [
                                {name: '投诉事件', value: this.dataMap.dataType1['201810sum']},
                                {name: '非投诉事件', value: this.dataMap.dataType2['201810sum']},
                            ]}
                        ]
                    },
                ]
            })
        }
    }
}
</script>

<style scoped>

</style>