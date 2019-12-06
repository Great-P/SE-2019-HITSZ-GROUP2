<template>
  <v-card>
    <v-toolbar text dense color="transparent" elevation="0">
      <v-toolbar-title>
        <h4>各单位事件办理进度</h4>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-divider></v-divider>
    <v-card-text class="pa-0">
      <v-data-table
        :headers="headers"
        :items="disposeunits"
        hide-default-footer
        class="elevation-0"
      >
        <!--        <template v-slot:item.avatar="{ item }">-->
        <!--          <v-avatar>-->
        <!--            <img :src="item.avatar" alt="avatar" />-->
        <!--          </v-avatar>-->
        <!--        </template>-->
        <template v-slot:item.Progess_percentage="{ item }">
          <v-progress-linear
            :value="item.Progess_percentage"
            height="5"
            :color="item.color"
          />
        </template>
        <!--        <template v-slot:item.action="{ item }">-->
        <!--          <v-btn text icon color="grey">-->
        <!--            <v-icon>edit</v-icon>-->
        <!--          </v-btn>-->
        <!--          <v-btn text icon color="grey">-->
        <!--            <v-icon>delete</v-icon>-->
        <!--          </v-btn>-->
        <!--        </template>-->
      </v-data-table>
      <v-divider/>
    </v-card-text>
  </v-card>
</template>

<script>
    import {Projects} from '@/api/project'
    import axios from 'axios'

    export default {
        data() {
            return {
                colors: ['pink', 'success', 'info', 'teal', 'grey'],
                headers: [
                    {
                        text: '处理单位',
                        align: 'left',
                        value: 'name',
                    },
                    {text: '最近一次处理', value: 'last_process'},
                    {text: '事件处理进度', value: 'Progess_percentage'},
                    {text: '剩余未处理事件数', value: 'OvertimeCount'},
                ],
                disposeunits: [],
                myInter: '',
            }
        },
        mounted() {
            this.getTableData();
            this.$nextTick(() => {
                //作图
                this.myInter = window.setInterval(() => {
                    setTimeout(this.getTableData(), 0)
                }, 3000);

            });
        },
        beforeRouteLeave(to, from, next) {
            if (this.myInter) {
                clearInterval(this.myInter);
            }
            this.myInter = null;
            next();
        },
        methods: {
            getTableData() {
                const url = 'http://127.0.0.1:5000/dashboard/table/dispose_unit'
                axios.get(url).then((res) => {
                    this.disposeunits = res.data;
                    let i;
                    for (i = 0; i < 5; i++) this.disposeunits[i].color = this.colors[i];
                })
            },
        },
        created() {

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
        },
        computed: {
            projects() {
                return Projects
            },
        },
    }
</script>
