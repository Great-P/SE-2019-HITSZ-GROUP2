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
    <el-row>
      <el-col>
        <el-card class="box-card">
          <vue-element-loading :active="this.isActive" spinner="mini-spinner" color="#FF6700"/>
          <div id="myChart" :style="{width: '100%', height: '500px'}"></div>
        </el-card>
      </el-col>
    </el-row>

  </div>
</template>

<script>
  /* eslint-disable */
  import axios from 'axios'

  var echarts = require('echarts');
  export default {
    name: "SpecialPieChartUse",
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
        piedata: [],
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
        const url = "http://localhost:5000/func1";
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
        const url = "http://localhost:5000/func1";
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
        axios.get("http://localhost:5000/func1")
          .then((res) => {
            this.piedata = this.process(res);
          })
      },
      getSeriesData(labels, values) {
        var seriesData = [];
        for (var i = 0; i < labels.length; i++) {
          seriesData.push({
            name: labels[i],
            value: values[i]
          });
        }
        return seriesData;
      },
      process(res) {
        const result = res.data;
        //初始化实例
        let SpecialPie = echarts.init(document.getElementById('myChart'));
        SpecialPie.setOption({
          title: {
            text: '民生情况',
            x: 'center',
          },
          tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
          },
          legend: {
            type: 'scroll',
            orient: 'vertical',
            right: 100,
            top: 20,
            bottom: 20,
            data: result.problem_labels,

            selected: result.problem_selected,
          },
          series: [
            {
              name: '问题性质',
              type: 'pie',
              radius: '60%',
              center: ['50%', '60%'],
              data: this.getSeriesData(result.problem_labels, result.problem_num),
              itemStyle: {
                emphasis: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }]
        })
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

<style scoped>

</style>
