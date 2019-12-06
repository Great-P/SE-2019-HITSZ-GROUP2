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
  require('echarts/extension/bmap/bmap');

  export default {
    name: "MapUse",
    data() {
      return {
        value: '2018-10',
        date: '',
        geoCoordMap: {},
        mapData: [],
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
        }, 60000);

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
        const url = "http://localhost:5000/func4";
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
      checkUpdate() {
        const url = "http://localhost:5000/func4";
        // this.$qs.stringify(data)
        axios.post(url, this.submitDate).then((res) => {
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
        axios.get("http://localhost:5000/func4")
          .then((res) => {
            this.preprocess(res);
            this.process(res);
          })
      },
      preprocess(res) {
        const result = res.data;
        //处理geodata
        this.geoCoordMap = {
          '南布社区': [114.375607, 22.70534],
          '和平社区': [114.355104, 22.697106],
          '坪山社区': [114.35256, 22.696774],
          '汤坑社区': [114.331079, 22.678805],
          '金沙社区': [114.408079, 22.743131],
          '江岭社区': [114.362596, 22.69202],
          '石井社区': [114.390978, 22.697625],
          '六和社区': [114.349914, 22.707919],
          '沙湖社区': [114.326552, 22.67909],
          '老坑社区': [114.369312, 22.734866],
          '竹坑社区': [114.395074, 22.715773],
          '秀新社区': [114.381223, 22.746873],
          '沙田社区': [114.408752, 22.769956],
          '六联社区': [114.332971, 22.795219],
          '坪环社区': [114.35474, 22.688096],
          '龙田社区': [114.372841, 22.753346],
          '坑梓社区': [114.390013, 22.753031],
          '沙坣社区': [114.377888, 22.690889],
          '田头社区': [114.410837, 22.697197],
          '田心社区': [114.421943, 22.700351],
          '碧岭社区': [114.295663, 22.67342],
          '金龟社区': [114.406461, 22.663744],
          '马峦社区': [114.338203, 22.644538],
        };
        this.mapData = [
          {
            name: result.problem_labels[0],
            value: result.problem_num[0],
          },
          {
            name: result.problem_labels[1],
            value: result.problem_num[1],
          },
          {
            name: result.problem_labels[2],
            value: result.problem_num[2],
          },
          {
            name: result.problem_labels[3],
            value: result.problem_num[3],
          },
          {
            name: result.problem_labels[4],
            value: result.problem_num[4],
          },
          {
            name: result.problem_labels[5],
            value: result.problem_num[5],
          },
          {
            name: result.problem_labels[6],
            value: result.problem_num[6],
          },
          {
            name: result.problem_labels[7],
            value: result.problem_num[7],
          },
          {
            name: result.problem_labels[8],
            value: result.problem_num[8],
          },
          {
            name: result.problem_labels[9],
            value: result.problem_num[9],
          },
          {
            name: result.problem_labels[10],
            value: result.problem_num[10],
          },
          {
            name: result.problem_labels[11],
            value: result.problem_num[11],
          },
          {
            name: result.problem_labels[12],
            value: result.problem_num[12],
          },
          {
            name: result.problem_labels[13],
            value: result.problem_num[13],
          },
          {
            name: result.problem_labels[14],
            value: result.problem_num[14],
          },
          {
            name: result.problem_labels[15],
            value: result.problem_num[15],
          },
          {
            name: result.problem_labels[16],
            value: result.problem_num[16],
          },
          {
            name: result.problem_labels[17],
            value: result.problem_num[17],
          },
          {
            name: result.problem_labels[18],
            value: result.problem_num[18],
          },
          {
            name: result.problem_labels[19],
            value: result.problem_num[19],
          },
          {
            name: result.problem_labels[20],
            value: result.problem_num[20],
          },
          {
            name: result.problem_labels[21],
            value: result.problem_num[21],
          },
          {
            name: result.problem_labels[22],
            value: result.problem_num[22],
          },
        ];
      },
      convertData(data) {
        var res = [];
        for (var i = 0; i < data.length; i++) {
          var geoCoord = this.geoCoordMap[data[i].name];
          if (geoCoord) {
            res.push({
              name: data[i].name,
              value: geoCoord.concat(data[i].value),
            });
          }
        }
        return res;
      },
      process(res) {
        const result = res.data;
        //初始化实例
        let mapChart = echarts.init(document.getElementById('myChart'));
        let _this = this;
        let _date = _this.submitDate.date;
        mapChart.setOption({
          title: {
            text: '热点社区展示',
            left: 'center',
          },
          // grid: {
          //   x: 200,
          //   y: 50,
          //   x2: 50,
          //   y2: 50,
          // },
          tooltip: {
            trigger: 'item',
          },
          bmap: {
            center: [114.375607, 22.70534],
            zoom: 12,
            roam: true,
            mapStyle: {
              styleJson: [{
                'featureType': 'water',
                'elementType': 'all',
                'stylers': {
                  'color': '#d1d1d1'
                }
              }, {
                'featureType': 'land',
                'elementType': 'all',
                'stylers': {
                  'color': '#f3f3f3'
                }
              }, {
                'featureType': 'railway',
                'elementType': 'all',
                'stylers': {
                  'visibility': 'off'
                }
              }, {
                'featureType': 'highway',
                'elementType': 'all',
                'stylers': {
                  'color': '#fdfdfd'
                }
              }, {
                'featureType': 'highway',
                'elementType': 'labels',
                'stylers': {
                  'visibility': 'off'
                }
              }, {
                'featureType': 'arterial',
                'elementType': 'geometry',
                'stylers': {
                  'color': '#fefefe'
                }
              }, {
                'featureType': 'arterial',
                'elementType': 'geometry.fill',
                'stylers': {
                  'color': '#fefefe'
                }
              }, {
                'featureType': 'poi',
                'elementType': 'all',
                'stylers': {
                  'visibility': 'off'
                }
              }, {
                'featureType': 'green',
                'elementType': 'all',
                'stylers': {
                  'visibility': 'off'
                }
              }, {
                'featureType': 'subway',
                'elementType': 'all',
                'stylers': {
                  'visibility': 'off'
                }
              }, {
                'featureType': 'manmade',
                'elementType': 'all',
                'stylers': {
                  'color': '#d1d1d1'
                }
              }, {
                'featureType': 'local',
                'elementType': 'all',
                'stylers': {
                  'color': '#d1d1d1'
                }
              }, {
                'featureType': 'arterial',
                'elementType': 'labels',
                'stylers': {
                  'visibility': 'off'
                }
              }, {
                'featureType': 'boundary',
                'elementType': 'all',
                'stylers': {
                  'color': '#fefefe'
                }
              }, {
                'featureType': 'building',
                'elementType': 'all',
                'stylers': {
                  'color': '#d1d1d1'
                }
              }, {
                'featureType': 'label',
                'elementType': 'labels.text.fill',
                'stylers': {
                  'color': '#999999'
                }
              }]
            }
          },
          series: [
            {
              name: '热点社区',
              type: 'scatter',
              coordinateSystem: 'bmap',
              data: this.convertData(this.mapData),
              symbolSize: function (val) {
                // console.log(_this.submitDate);
                if(_date.toString().split('-')[1]>8)
                {
                  return val[2]/10;
                }
                else
                {
                  return val[2]/2;
                }
              },
              label: {
                normal: {
                  formatter: '{b}',
                  position: 'right',
                  show: false,
                },
                emphasis: {
                  show: true,
                }
              },
              itemStyle: {
                normal: {
                  color: 'orange',
                }
              },
              encode: {
                tooltip: [2], // 显示事件数
              },
            },
            {
              name: 'Top 3',
              type: 'effectScatter',
              coordinateSystem: 'bmap',
              data: this.convertData(this.mapData.sort(function (a, b) {
                return b.value - a.value;
              }).slice(0, 3)),
              symbolSize: function (val) {
                // console.log(_this.submitDate);
                if(_date.toString().split('-')[1]>8)
                {
                  return val[2]/10;
                }
                else
                {
                  return val[2]/2;
                }
              },
              showEffectOn: 'render',
              rippleEffect: {
                brushType: 'stroke',
              },
              hoverAnimation: true,
              label: {
                normal: {
                  formatter: '{b}',
                  position: 'right',
                  show: true,
                }
              },
              itemStyle: {
                normal: {
                  color: 'purple',
                  shadowBlur: 10,
                  shadowColor: '#333',
                }
              },
              encode: {
                tooltip: [2], // 显示事件数
              },
              zlevel: 1,
            }
          ],
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
