<template>
  <div>
    <el-form :inline="true">
    <div class="container">
      <el-form-item>
      <div class="block">
        <span class="demonstration">选择日期:</span>
        <el-date-picker
          v-model="value"
          align="right"
          type="date"
          placeholder="选择日期"
          :picker-options="pickerOptions"
          @blur="submit"
        >
        </el-date-picker>
      </div>
      </el-form-item>
      <el-form-item>
      <div class="block">
        <span class="demonstration">月:</span>
        <el-date-picker
          v-model="value"
          type="month"
          placeholder="选择月"
          @blur="submit2"
        >
        </el-date-picker>
      </div>
      </el-form-item>
    </div>
    </el-form>

  <el-card class="box-card">
    <div id="myChart" :style="{width: '1000px', height: '500px'}"></div>
    </el-card>
  </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios'

var echarts = require('echarts');

export default {
  name: "NestedPieUse",
  data() {
    return {
      value: '',
      piedata: [],
    }
  },
  mounted() {
    this.$nextTick(() => {
      //作图
      this.filldata();
    });
  },
  created() {
    //获取数据
    //   this.checkUpdate();
      },
  methods: {
    submit() {
      let data={
          date: this.GMTToStr(this.value, false),
      };
      const url = "http://localhost:5000/func3";
      // this.$qs.stringify(data)
      axios.post(url, data).then((res) => {
        this.process(res);
      }, (err) => {
        alert("出错啦！")
      })
    },
    submit2() {
      let data={
          date: this.GMTToStr(this.value, true),
      };
      const url = "http://localhost:5000/func3";
      // this.$qs.stringify(data)
      axios.post(url, data).then((res) => {
        this.process(res);
      }, (err) => {
        alert("出错啦！")
      })
    },
    GMTToStr(time, isMonthOnly) {
      let date = new Date(time);
      let year = date.getFullYear();
      let month = (date.getMonth()+1);
      let day = date.getDate();
      if (month < 10)
        month = '0'+month;
      if (day < 10)
        day = '0'+day;
      let msg = '';
      if (isMonthOnly)
        msg = year + '-' + month;
      else
        msg = year + '-' + month + '-' + day;
      return msg;
    },
    timer() {
      return setTimeout(()=>{
        this.filldata();
      }, 1000)
    },
    filldata() {
      //绘制图片
      axios.get("http://localhost:5000/func3")
        .then((res) => {
          this.piedata = this.process(res);
        })
    },
    process(res) {
      const result = res.data;
      //初始化实例
      let nestedPie = echarts.init(document.getElementById('myChart'));
      nestedPie.setOption({
        title: { "text": "" },
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
          orient: 'vertical',
          x: 'left',
          data: '',
        },
        series: [
          {
            name: '事件数量',
            type: 'pie',
            selectedMode: '',
            radius: [0, '30%'],
            label: {
                normal: {
                    position: 'inner',
                }
            },
            labelLine: {
                normal: {
                    show: false,
                }
            },
            data: [
              {
                value: result.problem_sum[0],
                name: result.archive_type_labels[0],
              },
              {
                value: result.problem_sum[1],
                name: result.archive_type_labels[1],
              },
              {
                value: result.problem_sum[2],
                name: result.archive_type_labels[2],
              }
            ]
          },
          {
            name: '事件数量',
            type: 'pie',
            radius: ['40%', '55%'],
            label: {
                normal: {
                    formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                    backgroundColor: '#eee',
                    borderColor: '#aaa',
                    borderWidth: 1,
                    borderRadius: 4,
                    // shadowBlur:3,
                    // shadowOffsetX: 2,
                    // shadowOffsetY: 2,
                    // shadowColor: '#999',
                    // padding: [0, 7],
                    rich: {
                        a: {
                            color: '#999',
                            lineHeight: 22,
                            align: 'center'
                        },
                        // abg: {
                        //     backgroundColor: '#333',
                        //     width: '100%',
                        //     align: 'right',
                        //     height: 22,
                        //     borderRadius: [4, 4, 0, 0]
                        // },
                        hr: {
                            borderColor: '#aaa',
                            width: '100%',
                            borderWidth: 0.5,
                            height: 0
                        },
                        b: {
                            fontSize: 16,
                            lineHeight: 33
                        },
                        per: {
                            color: '#eee',
                            backgroundColor: '#334455',
                            padding: [2, 4],
                            borderRadius: 2
                        }
                    }
                }
            },
            data: [
              {
                value: result.problem_num[0],
                name: result.problem_labels[0],
              },
              {
                value: result.problem_num[1],
                name: result.problem_labels[1],
              },
              {
                value: result.problem_num[2],
                name: result.problem_labels[2],
              },
              {
                value: result.problem_num[3],
                name: result.problem_labels[3],
              },
              {
                value: result.problem_num[4],
                name: result.problem_labels[4],
              },
              {
                value: result.problem_num[5],
                name: result.problem_labels[5],
              },
              {
                value: result.problem_num[6],
                name: result.problem_labels[6],
              },
            ]

          }
        ]
      })
    }

  },
  watch: {
    bardata() {
      this.timer();
    }
  },
  destroyed() {
      clearTimeout(this.timer)
  }
}
</script>

<style scoped>
  .box-card {
    width: 1000px;
    height: 500px;
  }
</style>
