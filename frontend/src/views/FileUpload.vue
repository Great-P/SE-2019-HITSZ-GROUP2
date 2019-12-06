<template>
  <div class="media">
    <v-snackbar
      v-model="snackbar"
      :color="color"
      :timeout="2000"
      top
    >
      {{ successtext }}
      <v-btn
        dark
        text
        @click="snackbar = false"
      >
        关闭
      </v-btn>
    </v-snackbar>
    <v-toolbar class="elevation-0 transparent media-toolbar">
      <v-dialog v-model="showUploadDialog" persistent max-width="600px">
        <template v-slot:activator="{ on }">
          <v-btn text color="primary" outlined="true" large v-on="on">
            <v-icon color="primary">cloud_upload</v-icon>
            &nbsp;上传数据图表
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">文件上传</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <el-upload
                class="avatar-uploader"
                drag
                action="http://localhost:5000/fileupload"
                :show-file-list="false"
                :on-success="uploadSuccess"
                :before-upload="beforeAvatarUpload">
                <img v-if="imageUrl" :src="imageUrl" class="avatar">
                <i v-else class="el-icon-plus avatar-uploader-icon"></i>
              </el-upload>
              <!--              {{// files}}-->
            </v-container>
            <!--            <small>*indicates required field</small>-->
            <v-divider></v-divider>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn color="blue darken-1" text @click="showUploadDialog = false">关闭</v-btn>
            <!--            <v-btn color="blue darken-1" text @click="uploadFile">Upload</v-btn>-->
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-spacer></v-spacer>
      <v-menu
        offset-y
        :close-on-content-click="closeOnContentClick"

      >

        <template v-slot:activator="{ on }">
          <v-btn
            color="primary"
            text
            v-on="on"
            class="mr-2"
            outlined="true"
            large
          >
            选择分组方式
          </v-btn>
        </template>
        <v-list>
          <v-list-item-group v-model="groupByItemIdx"  color="indigo">
            <v-list-item
              v-for="(item, i) in headerSelect"
              :key="i"
            >
              <v-list-item-icon>
                <v-icon v-text="item.icon"></v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title v-text="item.text"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-menu>
      <v-menu
        offset-y
        :close-on-content-click="closeOnContentClick"

      >

        <template v-slot:activator="{ on }">
          <v-btn
            color="primary"
            text
            v-on="on"
            class="mr-2"
            outlined="true"
            large
          >
            选择显示属性
          </v-btn>
        </template>
        <v-list>
          <v-list-item-group v-model="selectedHeader" multiple color="indigo">
            <v-list-item
              v-for="(item, i) in headerSelect"
              :key="i"
            >
              <v-list-item-icon>
                <v-icon v-text="item.icon"></v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title v-text="item.text"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-menu>


      <v-btn
        color="primary"
        v-on="on"
        class="mr-2"
        large
        @click="confirmUpload"
      >
        确认上传
      </v-btn>



    </v-toolbar>
    <v-divider></v-divider>

    <v-card class="ma-2 ">
      <v-card-title>数据导入预览
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="search"
          label="搜索数据"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="displayItems"
        :sort-by="['CREATE_TIME']"
        :sort-desc="[false]"
        item-key="REC_ID"
        multi-sort
        :group-by.sync="groupByItem"
        :search="search"
        show-select
        v-model="selected_items"
        :loading="tableloading"
        loading-text="加载中，请稍候"
        class="elevation-1"
        :footer-props="{
      showFirstLastPage: true,
      firstIcon: 'mdi-arrow-collapse-left',
      lastIcon: 'mdi-arrow-collapse-right',
      prevIcon: 'mdi-minus',
      nextIcon: 'mdi-plus'
    }"
      ></v-data-table>
    </v-card>
  </div>
</template>


<script>

    import Bytes from 'bytes'
    import { getFileMenu, getFile } from '@/api/file'
    import VuePerfectScrollbar from 'vue-perfect-scrollbar'
    import axios from 'axios'
    export default {
        components: {
            VuePerfectScrollbar,
        },
        props: {
            type: {
                type: String,
                default: 'image',
            },
        },
        data() {
            //只要把请求数据的部分修改清楚就可以了
            return {
                search:'',
                color: 'success',
                tableloading: false,
                snackbar: false,
                successtext: '',
                selected_items:[],
                groupByItemIdx: [4],
                groupByItem: ['COMMUNITY_NAME'],
                groupdesc: [false,false,true],
                totalItemNum: 0,
                loading: false,
                options: {},
                closeOnContentClick: false,
                showUploadDialog: false,
                size: 'lg',
                view: 'grid',
                files: [],
                selectedHeader: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                headerSelect: [
                    {
                        icon: 'mdi-format-list-numbered',
                        text: '记录号',
                    },
                    {
                        icon: 'mdi-clock-outline',
                        text: '创建时间',
                    },
                    {
                        icon: 'mdi-map',
                        text: '区域',
                    },
                    {
                        icon: 'mdi-map-marker',
                        text: '街道',
                    },
                    {
                        icon: 'mdi-map-marker-outline',
                        text: '社区',
                    },
                    {
                        icon: 'mdi-file-document-box',
                        text: '事件类型',
                    },
                    {
                        icon: 'mdi-format-list-bulleted-type',
                        text: '主类',
                    },
                    {
                        icon: 'mdi-file-tree',
                        text: '子类',
                    },
                    {
                        icon: 'mdi-account-multiple-check',
                        text: '处理单位',
                    },
                    {
                        icon: 'mdi-source-branch',
                        text: '事件来源',
                    },
                    {
                        icon: 'mdi-alert-circle',
                        text: '事件属性',
                    },
                    {
                        icon: 'mdi-state-machine',
                        text: '办理状态',
                    },
                ],
                numtoheaders: [
                    {
                        value: 'REC_ID',
                        text: '记录号',
                    },
                    {
                        value: 'CREATE_TIME',
                        text: '创建时间',
                    },
                    {
                        value: 'DISTRICT_NAME',
                        text: '区域',
                    },
                    {
                        value: 'STREET_NAME',
                        text: '街道',
                    },
                    {
                        value: 'COMMUNITY_NAME',
                        text: '社区',
                    },
                    {
                        value: 'EVENT_TYPE_NAME',
                        text: '事件类型',
                    },
                    {
                        value: 'MAIN_TYPE_NAME',
                        text: '主类',
                    },
                    {
                        value: 'SUB_TYPE_NAME',
                        text: '子类',
                    },
                    {
                        value: 'DISPOSE_UNIT_NAME',
                        text: '处理单位',
                    },
                    {
                        value: 'EVENT_SRC_NAME',
                        text: '事件来源',
                    },
                    {
                        value: 'OVERTIME_ARCHIVE_NUM',
                        text: '超期结办',
                    },
                    {
                        value: 'INTIMETO_ARCHIVE_NUM',
                        text: '正在结办',
                    },
                    {
                        value: 'INTIME_ARCHIVE_NUM',
                        text: '按时结办',
                    },
                    {
                        value: 'EVENT_PROPERTY_NAME',
                        text: '事件属性',
                    },
                ],

                headers: [
                    {
                        value: 'REC_ID',
                        text: '记录号',
                    },
                    {
                        value: 'CREATE_TIME',
                        text: '创建时间',
                    },
                    {
                        value: 'DISTRICT_NAME',
                        text: '区域',
                    },
                    {
                        value: 'STREET_NAME',
                        text: '街道',
                    },
                    {
                        value: 'COMMUNITY_NAME',
                        text: '社区',
                    },
                    {
                        value: 'EVENT_TYPE_NAME',
                        text: '事件类型',
                    },
                    {
                        value: 'MAIN_TYPE_NAME',
                        text: '主类',
                    },
                    {
                        value: 'SUB_TYPE_NAME',
                        text: '子类',
                    },
                    {
                        value: 'DISPOSE_UNIT_NAME',
                        text: '处理单位',
                    },
                    {
                        value: 'EVENT_SRC_NAME',
                        text: '事件来源',
                    },
                ],
                displayItems:[]
            }

        }
        ,
        computed: {
            mediaMenu() {
                return getFileMenu
            },

        },

        methods: {
            confirmUpload(){
                if( this.selected_items.length === 0) {
                    this.successtext = "请至少选择一个项！"
                    this.color = 'error'
                    this.snackbar = true
                    return
                }
                const url = 'http://127.0.0.1:5000/confirm'
                //TODO: 错误处理
                axios.post(url, this.selected_items).then((res) => {
                    this.successtext = "所选数据已成功加入数据库！"
                    this.color = 'success'
                    this.snackbar = true
                })
            },
            uploadSuccess(response, file, fileList){
                this.showUploadDialog = false
                this.successtext = '上传成功，请选择需要的条目后，点击右上方“确认上传”按钮！'
                this.color = 'success'
                this.snackbar = true
                this.tableloading = true
                this.getTableData(response.data)
                this.tableloading = false
            },
            uploadFile(){
                const url = 'http://127.0.0.1:5000/files'
                let file = this.files[0]
                let formdata = new FormData()
                formdata.append('file', file)
                let config = {
                    headers:{'Content-Type':'multipart/form-data'}
                }; //添加请求头
                axios.post('http://127.0.0.1:5000/files', formdata, config)
                this.showUploadDialog=false
            },
            refreshHeaders() {
                var i
                let sorted = this.selectedHeader.slice()
                sorted.sort(function(a, b) {
                    return a - b
                })
                this.headers = []
                for (i in sorted) {
                    this.headers.push(this.numtoheaders[sorted[i]])
                }
            },
            QueryAll() {
                const path = 'http://localhost:5000/queryAll'
                const { sortBy, sortDesc, page, itemsPerPage } = this.options
                let queryHead = {
                    'pageSize': itemsPerPage,
                    'pageNum': page,
                }
                console.log(this.pageSize, this.currentPage)
                axios.post(path, queryHead).then((res) => {
                    this.displayItems = res.data.json_data
                    this.totalItemNum = res.data.total
                })
                let i
                for (i=0 ; i<this.displayItems.length;i++) {
                    this.displayItems.CREATE_TIME=this.formateDate(this.displayItems.CREATE_TIME)
                }
            },
            getTableData(data) {
                this.loading=true
                this.displayItems = data
                this.totalItemNum=this.displayItems.length
                let i
                for (i=0 ; i<this.displayItems.length;i++) {
                    this.displayItems[i].CREATE_TIME=this.formateDate(this.displayItems[i].CREATE_TIME)
                }
                this.loading = false
            },
            isImage(file) {
                return this.imageMime.includes(file.fileType)
            },
            mimeIcons(file) {
                return this.imageMime.includes(file.fileType)
                    ? 'image'
                    : 'insert_drive_file'
            },
            showDetail(file) {
                this.selectedFile = file
            },
            fileSize(number) {
                return Bytes.format(number)
            },
            formateDate(string) {
                return string ? new Date(string).toLocaleString() : ''
            },
            computeFileImage(file) {
                return this.isImage(file) ? file.path : '/static/icon/file_empty.svg'
            },
        },
        watch: {
            selectedHeader() {
                this.refreshHeaders()
            },
            groupByItemIdx(){
                this.groupByItem=this.numtoheaders[this.groupByItemIdx].value
            }
        },
        beforeCreate() {
            let token = sessionStorage.getItem('token');
            let user = sessionStorage.getItem('user');
            if(token!==this.$md5(user+'2')&&token!==this.$md5(user+'3'))
            {
                this.$router.push('/auth/login');
                this.$message.error('您无权访问该页面！');
            }
        },

    }
</script>
<style lang="sass" scoped>
  .card-media img
    width: 100%

    .media
      &-cotent--wrap, &-menu
        min-width: 260px
        border-right: 1px solid #eee
        min-height: calc(100vh - 50px - 64px)

      &-detail
        min-width: 300px
        border-left: 1px solid #eee
</style>
