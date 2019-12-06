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
              value-format="yyyy-MM"
              placeholder="选择月"
              @blur="submit"
            >
            </el-date-picker>
          </div>
        </el-form-item>
      </div>
    </el-form>
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
    name: "StackedBarUse",
    data() {
      return {
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() > Date.now();
          },
          shortcuts: [{
            text: '今天',
            onClick(picker) {
              picker.$emit('pick', new Date());
            }
          }, {
            text: '昨天',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit('pick', date);
            }
          }, {
            text: '一周前',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', date);
            }
          }]
        },
        value: '2018-10',
        submitDate: {
          date: '2018-10'
        },
        myInter: '',
        isActive: true,
      }
    },
    mounted() {
      this.$nextTick(() => {
        //作图
        this.myInter = window.setInterval(() => {
          setTimeout(this.checkUpdate(), 0)
        }, 10000);

      });
    },
    created() {
      //获取数据
        this.checkUpdate();
    },
    beforeRouteLeave(to, from, next) {
      if (this.myInter) {
        clearInterval(this.myInter);
      }
      this.myInter = null;
      next();
    },
    methods: {
      submit() {
        let data = {
          date: this.GMTToStr(this.value),
        };
        this.submitDate = data;
        const url = "http://localhost:5000/func2";
        // this.$qs.stringify(data)
        axios.post(url, data).then((res) => {
          this.process(res);
        }, (err) => {
          this.$message({
            showClose: true,
            message: '选择的日期没有数据，请重新选择',
            type: 'warning',
            duration: 2000,
          });
        })
      },

      checkUpdate() {
        const url = "http://localhost:5000/func2";
        // this.$qs.stringify(data)
        axios.post(url, this.submitDate).then((res) => {
          this.process(res);
          this.isActive = false;
        }, (err) => {
          this.$message({
            showClose: true,
            message: '选择的日期没有数据，请重新选择',
            type: 'warning',
            duration: 2000,
          });
        })
      },
      GMTToStr(time, isMonthOnly = true) {
        if (time.toLocaleString().length > 10) {
          isMonthOnly = false;
        }
        let date = new Date(time);
        let year = date.getFullYear();
        let month = (date.getMonth() + 1);
        let day = date.getDate();
        if (month < 10)
          month = '0' + month;
        if (day < 10)
          day = '0' + day;
        let msg = '';
        if (isMonthOnly)
          msg = year + '-' + month;
        else
          msg = year + '-' + month + '-' + day;
        return msg;
      },


      filldata() {
        //绘制图片
        axios.get("http://localhost:5000/func2")
          .then((res) => {
            this.bardata = this.process(res);
          })
      },

      process(res) {
        const result = res.data;
        //初始化实例
        let stackedBar = echarts.init(document.getElementById('myChart'));
        stackedBar.setOption({
          title: {"text": ""},
          grid: {
            x: 200,
            y: 50,
            x2: 100,
            y2: 50,
          },
          tooltip: {},
          legend: {
            data: result.problem_labels,
            orient: 'horizontal',
            left: 350,
          },
          xAxis: [{
            data: result.street_labels,
            name: "街道"
          }],
          yAxis: [{
            type: 'value',
            name: '事件数'
          }],
          series: [
            {
              name: result.problem_labels[0],
              type: "bar",
              stack: "problems1",
              data: result.problem_num[0],
            },
            {
              name: result.problem_labels[1],
              type: "bar",
              stack: "problems1",
              data: result.problem_num[1],
            },
            {
              name: result.problem_labels[2],
              type: "bar",
              stack: "problems1",
              data: result.problem_num[2],
            },
            {
              name: result.problem_labels[3],
              type: "bar",
              stack: "problems1",
              data: result.problem_num[3],
            },
            {
              name: result.problem_labels[4],
              type: "bar",
              stack: "problems1",
              data: result.problem_num[4],
            },
            {
              name: result.problem_labels[5],
              type: "bar",
              stack: "problems1",
              data: result.problem_num[5],
            },
            {
              name: result.problem_labels[6],
              type: "bar",
              stack: "problems1",
              data: result.problem_num[6],
            },
            {
              name: result.problem_labels[7],
              type: "bar",
              stack: "problems1",
              data: result.problem_num[7],
            },
          ]
        })
      }

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

<style scoped>

</style>
