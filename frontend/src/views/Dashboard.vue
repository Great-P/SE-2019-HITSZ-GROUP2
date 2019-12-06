<template>
  <div class="page--dash">
    <v-container grid-list-xl fluid>
<!--      <vue-element-loading :active="this.isActive" spinner="mini-spinner" color="#FF6700"/>-->
      <v-layout row wrap>
        <!-- mini statistic start -->
        <v-flex lg3 sm6 xs12>
          <mini-statistic
            icon="mdi-finance"
            :title="stat.total"
            sub-title="总上报事件"
            color="light-blue"
          />
        </v-flex>
        <v-flex lg3 sm6 xs12>
          <mini-statistic
            icon="mdi-check-bold"
            :title="stat.finished"
            sub-title="已结办事件"
            color="green"
          />
        </v-flex>
        <v-flex lg3 sm6 xs12>
          <mini-statistic
            icon="mdi-progress-check"
            :title="stat.due"
            sub-title="待结办事件"
            color="orange"
          />
        </v-flex>
        <v-flex lg3 sm6 xs12>
          <mini-statistic
            icon="mdi-progress-close"
            :title="stat.overdue"
            sub-title="超期结办事件"
            color="red"
          />
        </v-flex>
        <!-- mini statistic  end -->

        <v-flex lg8 sm12 xs12>
          <v-widget title="各街道事件办理情况统计" content-bg="white">
            <v-btn icon slot="widget-header-action">
              <v-icon class="text--secondary">refresh</v-icon>
            </v-btn>
            <div slot="widget-content">
              <el-card class="box-card">
                <div id="Chart1" :style="{width: '100%', height: '400px'}"></div>
              </el-card>
            </div>
          </v-widget>
        </v-flex>
        <!--  民生事件分布情况      -->
        <v-flex lg4 sm12 xs12>
          <v-widget title="民生事件分布情况 Top5" content-bg="white">
            <div slot="widget-content">
              <el-card class="box-card">
                <div id="Chart2" :style="{width:'100%', height:'400px'}"></div>
              </el-card>
            </div>
          </v-widget>
        </v-flex>
        <!-- social/weather card start -->
        <!--        <v-flex lg4 sm12 xs12>-->
        <!--          <profile-card />-->
        <!--        </v-flex>-->
        <v-flex lg7 sm12 xs12>
          <plain-table/>
        </v-flex>
        <v-flex lg5 sm12 xs12>
          <plain-table-order/>
        </v-flex>

        <v-flex lg8 sm12 xs12>
          <v-widget title="时间轴" content-bg="white">
            <div slot="widget-content">
              <v-timeline align-top dense>
                <v-timeline-item
                  :color="item.color"
                  small
                  v-for="(item, index) in timeline"
                  :key="index"
                >
                  <v-row>
                    <v-col cols="2">
                      <strong>{{ item.timeString }}</strong>
                    </v-col>
                    <v-col>
                      <strong>{{ item.title }} </strong> {{ item.text }}
                    </v-col>
                  </v-row>
                </v-timeline-item>
              </v-timeline>
            </div>
          </v-widget>
        </v-flex>

        <v-flex lg4 sm12 xs12>
          <el-card class="box-card">
            <div id="Chart3" :style="{width:'100%', height:'270px'}"></div>
          </el-card>
        </v-flex>

      </v-layout>
    </v-container>
  </div>
</template>

<script>
    import API from '@/api'
    import EChart from '@/components/chart/echart'
    import MiniStatistic from '@/components/widgets/statistic/MiniStatistic'
    import ProfileCard from '@/components/widgets/card/ProfileCard'
    import PlainTable from '@/components/widgets/list/PlainTable'
    import PlainTableOrder from '@/components/widgets/list/PlainTableOrder'
    import VWidget from '@/components/VWidget'
    import Material from 'vuetify/es5/util/colors'


    import axios from 'axios'

    export default {
        components: {
            VWidget,
            MiniStatistic,
            ProfileCard,
            EChart,
            PlainTable,
            PlainTableOrder,
        },
        data() {
            return {
                timeline: [],
                stat: {
                    total: '',
                    finished: '',
                    due: '',
                    overdue: '',
                },
                color: Material,
                selectedTab: 'tab-1',
                linearTrending: [
                    {
                        subheading: 'Sales',
                        headline: '2,55',
                        caption: 'increase',
                        percent: 15,
                        icon: {
                            label: 'trending_up',
                            color: 'success',
                        },
                        linear: {
                            value: 15,
                            color: 'success',
                        },
                    },
                    {
                        subheading: 'Revenue',
                        headline: '6,553',
                        caption: 'increase',
                        percent: 10,
                        icon: {
                            label: 'trending_down',
                            color: 'error',
                        },
                        linear: {
                            value: 15,
                            color: 'error',
                        },
                    },
                    {
                        subheading: 'Orders',
                        headline: '5,00',
                        caption: 'increase',
                        percent: 50,
                        icon: {
                            label: 'arrow_upward',
                            color: 'info',
                        },
                        linear: {
                            value: 50,
                            color: 'info',
                        },
                    },
                ],
                trending: [
                    {
                        subheading: '事件结办情况',
                        headline: '90%',
                        caption: '事件已经结办',
                        percent: 90,
                        icon: {
                            label: 'list',
                            color: 'primary',
                        },
                        linear: {
                            value: 90,
                            color: 'success',
                        },
                    },
                    {
                        subheading: '民众满意度',
                        headline: '98%',
                        caption: '民众感到满意',
                        percent: 98,
                        icon: {
                            label: 'email',
                            color: 'info',
                        },
                        linear: {
                            value: 15,
                            color: 'info',
                        },
                    },

                ],
                myInter: '',
                isActive: true,
            }
        },

        mounted() {
            this.$nextTick(() => {
                this.filldata();
                //作图
                this.myInter = window.setInterval(() => {
                    setTimeout(this.filldata(), 0)
                }, 3000);

            });
            // this.getTimeLine()
        },
        beforeRouteLeave(to, from, next) {
            if (this.myInter) {
                clearInterval(this.myInter);
            }
            this.myInter = null;
            next();
        },

        methods: {
            // getTimeLine() {
            //     const url = 'http://127.0.0.1:5000/dashboard/timeline'
            //     axios.get(url).then((res) => {
            //         this.timeline = res.data
            //     })
            // },
            filldata() {
                const url = 'http://127.0.0.1:5000/dashboard/timeline'
                axios.get(url).then((res) => {
                    this.timeline = res.data
                })
                //绘制图片
                axios.get("http://localhost:5000/func7")
                    .then((res) => {
                        this.process(res);
                    })
                this.isActive = false;
            },

            process(res) {
                // console.log('111');
                let result = res.data;
                this.stat.total = result.array1[0];
                this.stat.finished = result.array1[1];
                this.stat.due = result.array1[2];
                this.stat.overdue = result.array1[3];

                let Chart1 = echarts.init(document.getElementById('Chart1'));
                Chart1.setOption({
                    grid: {
                        x: 100,
                        y: 50,
                        x2: 50,
                        y2: 50,
                    },
                    legend: {},
                    tooltip: {},
                    dataset: {
                        source: [
                            ['类型', '总事件', '已结办'],
                            [result.array2[0], result.array3[0], result.array4[0]],
                            [result.array2[1], result.array3[1], result.array4[1]],
                            [result.array2[2], result.array3[2], result.array4[2]],
                            [result.array2[3], result.array3[3], result.array4[3]],
                            [result.array2[4], result.array3[4], result.array4[4]],
                            [result.array2[5], result.array3[5], result.array4[5]],
                        ]
                    },
                    xAxis: {type: 'category'},
                    yAxis: {},
                    // Declare several bar series, each will be mapped
                    // to a column of dataset.source by default.
                    series: [
                        {type: 'bar'},
                        {type: 'bar'},
                    ]
                });

                let Chart2 = echarts.init(document.getElementById('Chart2'));
                Chart2.setOption(
                    {
                        tooltip: {
                            trigger: 'item',
                            formatter: "{a} <br/>{b}: {c} ({d}%)"
                        },
                        legend: {
                            orient: 'horizontal',
                            x: 'left',
                            data: result.array5,
                        },
                        series: [
                            {
                                name: 'top5事件',
                                type: 'pie',
                                radius: ['50%', '70%'],
                                avoidLabelOverlap: false,
                                label: {
                                    normal: {
                                        show: false,
                                        position: 'center'
                                    },
                                    emphasis: {
                                        show: true,
                                        textStyle: {
                                            fontSize: '16',
                                            fontWeight: 'bold'
                                        }
                                    }
                                },
                                labelLine: {
                                    normal: {
                                        show: false
                                    }
                                },
                                data: [
                                    {value: result.array6[0], name: result.array5[0]},
                                    {value: result.array6[1], name: result.array5[1]},
                                    {value: result.array6[2], name: result.array5[2]},
                                    {value: result.array6[3], name: result.array5[3]},
                                    {value: result.array6[4], name: result.array5[4]},
                                ]
                            }
                        ]
                    }
                );

                let Chart3 = echarts.init(document.getElementById('Chart3'));
                Chart3.setOption(
                    {
                        tooltip: {
                            formatter: "{a} <br/>{b} : {c}%"
                        },
                        // toolbox: {
                        //   feature: {
                        //     restore: {},
                        //     saveAsImage: {}
                        //   }
                        // },
                        series: [
                            {
                                name: '结办率',
                                type: 'gauge',
                                detail: {formatter: '{value}%'},
                                data: [{value: (100 * this.stat.finished / this.stat.total).toFixed(1), name: '结办率'}]
                            }
                        ]
                    }
                );

            },

        },
        computed: {
            activity() {
                return API.getActivity()
            },
            posts() {
                return API.getPost(3)
            },

            tendaysTrending() {
                return {
                    msg: "较昨日增加10%",
                    icon: "trending_up",
                }
            },

        },

        beforeDestroy() {
            if (this.myInter) {
                clearInterval(this.myInter);
            }
            this.myInter = null;
        },

        destroyed() {
            if (this.myInter) {
                clearInterval(this.myInter);
            }
            this.myInter = null;
        }
    }
</script>
