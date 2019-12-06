<template>
  <div>
    <vue-element-loading :active="this.isActive" spinner="mini-spinner" color="#FF6700"/>
    <el-card class="box-card">
      <div class="topEvent" :data="top">
        <div v-for="top1 in top">
          <span class="title" v-text="top1.time"></span>
          <span class="street" v-text="top1.street"></span>
          <span>的</span>
          <span class="community" v-text="top1.community"></span>
          <span>从</span>
          <span class="eventsrc" v-text="top1.eventsrc"></span>
          <span>接到</span>
          <span class="subtype" v-text="top1.subtype"></span>
          <span class="eventtype" v-text="top1.eventtype"></span>
          <span>，请</span>
          <span class="unit" v-text="top1.unit"></span>
          <span>尽快前往处理</span>
        </div>
      </div>
      <br>
      <vue-seamless-scroll :data="items" class="seamless-warp">
        <div v-for="item in items">
          <span class="title" v-text="item.time"></span>
          <span class="street" v-text="item.street"></span>
          <span>的</span>
          <span class="community" v-text="item.community"></span>
          <span>从</span>
          <span class="eventsrc" v-text="item.eventsrc"></span>
          <span>接到</span>
          <span class="subtype" v-text="item.subtype"></span>
          <span class="eventtype" v-text="item.eventtype"></span>
          <span>，请</span>
          <span class="unit" v-text="item.unit"></span>
          <span>尽快前往处理</span>
        </div>
      </vue-seamless-scroll>
    </el-card>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "ScrollPage",
    data() {
      return {
        items: [],
        top: [],
        isActive: true,
      }
    },
    mounted() {
      this.$nextTick(() => {
        //作图
        this.filldata();
      });
    },
    methods: {
      filldata() {
        //绘制图片
        axios.get("http://localhost:5000/func5")
          .then((res) => {
            this.preprocess(res);
            this.isActive = false;
          })
      },
      preprocess(res) {
        const result = res.data;
        this.top = [
          {
            time: result.events[0][0][0],
            street: result.events[0][0][1],
            community: result.events[0][0][2],
            eventsrc: result.events[0][0][3],
            subtype: result.events[0][0][4],
            eventtype: result.events[0][0][5],
            unit: result.events[0][0][6],
          },
        ];
        this.items = [
          {
            time: result.events[0][0][0],
            street: result.events[0][0][1],
            community: result.events[0][0][2],
            eventsrc: result.events[0][0][3],
            subtype: result.events[0][0][4],
            eventtype: result.events[0][0][5],
            unit: result.events[0][0][6],
          },
          {
            time: result.events[0][1][0],
            street: result.events[0][1][1],
            community: result.events[0][1][2],
            eventsrc: result.events[0][1][3],
            subtype: result.events[0][1][4],
            eventtype: result.events[0][1][5],
            unit: result.events[0][1][6],
          },
          {
            time: result.events[0][2][0],
            street: result.events[0][2][1],
            community: result.events[0][2][2],
            eventsrc: result.events[0][2][3],
            subtype: result.events[0][2][4],
            eventtype: result.events[0][2][5],
            unit: result.events[0][2][6],
          },
          {
            time: result.events[0][3][0],
            street: result.events[0][3][1],
            community: result.events[0][3][2],
            eventsrc: result.events[0][3][3],
            subtype: result.events[0][3][4],
            eventtype: result.events[0][3][5],
            unit: result.events[0][3][6],
          },
          {
            time: result.events[0][4][0],
            street: result.events[0][4][1],
            community: result.events[0][4][2],
            eventsrc: result.events[0][4][3],
            subtype: result.events[0][4][4],
            eventtype: result.events[0][4][5],
            unit: result.events[0][4][6],
          },
          {
            time: result.events[0][5][0],
            street: result.events[0][5][1],
            community: result.events[0][5][2],
            eventsrc: result.events[0][5][3],
            subtype: result.events[0][5][4],
            eventtype: result.events[0][5][5],
            unit: result.events[0][5][6],
          },
          {
            time: result.events[0][6][0],
            street: result.events[0][6][1],
            community: result.events[0][6][2],
            eventsrc: result.events[0][6][3],
            subtype: result.events[0][6][4],
            eventtype: result.events[0][6][5],
            unit: result.events[0][6][6],
          },
          {
            time: result.events[0][7][0],
            street: result.events[0][7][1],
            community: result.events[0][7][2],
            eventsrc: result.events[0][7][3],
            subtype: result.events[0][7][4],
            eventtype: result.events[0][7][5],
            unit: result.events[0][7][6],
          },
          {
            time: result.events[0][8][0],
            street: result.events[0][8][1],
            community: result.events[0][8][2],
            eventsrc: result.events[0][8][3],
            subtype: result.events[0][8][4],
            eventtype: result.events[0][8][5],
            unit: result.events[0][8][6],
          },
          {
            time: result.events[0][9][0],
            street: result.events[0][9][1],
            community: result.events[0][9][2],
            eventsrc: result.events[0][9][3],
            subtype: result.events[0][9][4],
            eventtype: result.events[0][9][5],
            unit: result.events[0][9][6],
          },
        ];
      }
    }
  }
</script>

<style scoped>
  .seamless-warp {
    height: 500px;
    overflow: hidden;
    font-family: 华文宋体;
    font-size: 24px;
    font-weight: bold;
  }

  .topEvent {
    font-family: 华文宋体;
    font-size: 24px;
    font-weight: bold;
    border: dashed;
    background-color: khaki;
  }

  .street {
    color: darkblue;
  }

  .community {
    color: darkcyan;
  }

  .eventsrc {
    color: mediumpurple;
  }

  .subtype {
    color: red;
  }

  .eventtype {
    color: dodgerblue;
  }

  .unit {
    color: hotpink;
  }
</style>