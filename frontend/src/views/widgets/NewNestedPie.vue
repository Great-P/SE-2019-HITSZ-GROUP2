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
              value-format="yyyy-MM"
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
    name: "NewNestedPie",
    data() {
      return {
        value: '2018-10',
        piedata: [],

        level1: [],
        level2: [],
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
        // this.myInter = window.setInterval(() => {
        //     setTimeout(this.checkUpdate(), 0)
        // }, 3000);
        this.filldata();
      });
    },
    created() {
      //获取数据
      // this.filldata();
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
        const url = "http://localhost:5000/func3";
        // this.$qs.stringify(data)
        axios.post(url, data).then((res) => {
          this.preprocess(res);
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
        axios.get("http://localhost:5000/func3")
          .then((res) => {
            this.preprocess(res);
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
      preprocess(res) {
        const result = res.data;
        this.level1 = [
          {
            name: result.archive_type_labels[0],
            color: "#28bcf3",
            category: 0,
            value: result.problem_sum[0],
          },
          {
            name: result.archive_type_labels[1],
            color: "#ffc767",
            category: 1,
            value: result.problem_sum[1],
          },
          {
            name: result.archive_type_labels[2],
            color: "#92fb88",
            category: 2,
            value: result.problem_sum[2],
          },
        ];
        this.level2 = [
          {
            name: result.problem_labels[0],
            color: "#2196F3",
            category: 0,
            value: result.values[0][0],
          },
          {
            name: result.problem_labels[1],
            color: "#48B1F3",
            category: 0,
            value: result.values[0][1],
          },
          {
            name: result.problem_labels[2],
            color: "#41CCFB",
            category: 0,
            value: result.values[0][2],
          },
          {
            name: result.problem_labels[3],
            color: "#5EDDFB",
            category: 0,
            value: result.values[0][3],
          },
          {
            name: result.problem_labels[4],
            color: "#acdcfb",
            category: 0,
            value: result.values[0][4],
          },
          {
            name: "others",
            color: "#D2EEFB",
            category: 0,
            value: result.values[0][7],
          },

          {
            name: result.problem_labels[0],
            color: "#FFF3E0",
            category: 1,
            value: result.values[1][0],
          },
          {
            name: result.problem_labels[1],
            color: "#FFE0B2",
            category: 1,
            value: result.values[1][1],
          },
          {
            name: result.problem_labels[2],
            color: "#FFCC80",
            category: 1,
            value: result.values[1][2],
          },
          {
            name: result.problem_labels[3],
            color: "#ffbe48",
            category: 1,
            value: result.values[1][3],
          },
          {
            name: result.problem_labels[4],
            color: "#ffa829",
            category: 1,
            value: result.values[1][4],
          },
          {
            name: "others",
            color: "#ff8506",
            category: 1,
            value: result.values[1][7],
          },

          {
            name: result.problem_labels[0],
            color: "#4CAF50",
            category: 2,
            value: result.values[2][0],
          },
          {
            name: result.problem_labels[1],
            color: "#E8F5E9",
            category: 2,
            value: result.values[2][1],
          },
          {
            name: result.problem_labels[2],
            color: "#C8E6C9",
            category: 2,
            value: result.values[2][2],
          },
          {
            name: "others",
            color: "#B2E635",
            category: 2,
            value: result.values[2][7],
          },
        ];
      },
      process(res) {
        const result = res.data;
        //初始化实例
        let nestedPie = echarts.init(document.getElementById('myChart'));
        /**
         * @params params
         * params.name 标识当前点击的legend
         * params.selected 标识当前选中的legend集合
         */
        let _this = this;
        nestedPie.on('legendselectchanged', function (params) {
          let options = this.getOption();
          let keys = Object.keys(params.selected);
          let selected = [];

          // 获取选中目录的 category 值
          let i = 0;
          for (let item of keys) {
            if (params.selected[item]) {
              selected.push(i);
            }
            i = i + 1;
          }

          // 根据 category 获取 series 中 data 数据项
          options.series[1].data = _this.level2.filter(item => {
            return selected.includes(item.category);
          });
          // options.series[2].data = this.level3.filter(item => {
          //     return selected.includes(item.category);
          // });

          this.setOption(options);
        });

        nestedPie.setOption({
          tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
          },
          legend: {
            orient: 'vertical',
            x: 'left',
            data: ['按期结办', '超期结办', '处置中'],
          },
          series: [
            {
              name: '结办情况',
              type: 'pie',
              label: {
                normal: {
                  show: false,
                }
              },
              itemStyle: {
                normal: {
                  /**
                   * 自定义饼图 扇形 颜色
                   * @param params
                   */
                  color(params) {
                    return params.data.color;
                  }
                }
              },
              radius: ['25%', '40%'],
              data: this.level1
            },
            {
              name: '事件类型',
              type: 'pie',
              label: {
                normal: {
                  show: false,
                }
              },
              itemStyle: {
                normal: {
                  color(params) {
                    return params.data.color;
                  }
                }
              },
              radius: ['60%', '75%'],
              data: this.level2
            },
          ]
        });

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
