<template>
  <v-card>
    <v-toolbar text dense color="transparent" elevation="0">
      <v-toolbar-title>
        <h4>热门事件处置情况</h4>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-divider/>
    <v-card-text class="pa-0">
      <template>
        <v-data-table
          :headers="headers"
          :items="items"
          hide-default-footer
          class="elevation-0 table-striped"
        >
          <template v-slot:item.status="{ item }">
            <v-chip
              label
              small
              :color="getColorByStatus(item.status)"
              text-color="white"
            >
              {{ item.status }}
            </v-chip>
          </template>
        </v-data-table>
      </template>
      <v-divider></v-divider>
    </v-card-text>
  </v-card>
</template>

<script>
    import axios from 'axios'

    export default {

        data() {
            return {
                headers: [
                    {
                        text: '记录号',
                        align: 'left',
                        sortable: false,
                        value: 'id',
                    },
                    {text: '反馈时间', value: 'create_time'},
                    {text: '事件简述', value: 'main_type'},
                    {text: '处置情况', value: 'status'},
                ],
                items: [],
                colors: {
                    '处理中': 'blue',
                    '已超期': 'red',
                    '处理完毕': 'green',
                },
                myInter: '',
            }
        },
        mounted() {
            this.getRecentEvents();
            this.$nextTick(() => {
                //作图
                this.myInter = window.setInterval(() => {
                    setTimeout(this.getRecentEvents(), 0)
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
        computed: {
            randomColor() {
                let item = Math.floor(Math.random() * this.colors.length)
                return this.colors[item]
            },
        },
        methods: {
            getRecentEvents() {
                const url = 'http://127.0.0.1:5000/dashboard/table/recent_event'
                axios.get(url).then((res) => {
                    this.items = res.data
                })
            },
            getColorByStatus(status) {
                return this.colors[status]
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
