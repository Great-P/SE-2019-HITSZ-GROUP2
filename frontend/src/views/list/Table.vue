<template>
  <div class="list-table">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex sm12>
          <h3>用户管理</h3>
        </v-flex>
        <v-flex lg12>
          <v-card>
            <v-toolbar flat color="white">
              <v-text-field
                text
                solo
                flat
                prepend-icon="search"
                placeholder="搜索……"
                v-model="search"
                hide-details
                class="hidden-sm-and-down"
              ></v-text-field>
              <v-btn icon @click="showsel=!showsel">
                <v-icon>filter_list</v-icon>
<!--                选择-->
              </v-btn>
            </v-toolbar>
            <v-divider></v-divider>
            <v-card-text class="pa-0">
              <v-data-table
                :headers="complex.headers"
                :search="search"
                :items="complex.items"
                :items-per-page-options="[
                  10,
                  25,
                  50,
                  { text: 'All', value: -1 },
                ]"
                class="elevation-1"
                item-key="username"
                v-bind:show-select="showsel"
                v-model="complex.selected"
              >
                <template v-slot:item.avatar="{ item }">
                  <v-avatar>
                    <img :src="item.avatar" alt="avatar" size="16" />
                  </v-avatar>
                </template>
                <template v-slot:item.action="{ item }">
                  <v-btn
                    depressed
                    outline
                    icon
                    fab
                    dark
                    color="primary"
                    small
                    @click="handleClick(props.item)"
                  >
                    <v-icon>edit</v-icon>
                  </v-btn>
                  <v-btn
                    depressed
                    outline
                    icon
                    fab
                    dark
                    color="pink"
                    small
                    @click="handleDelete(props.item)"
                  >
                    <v-icon>delete</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
      <v-col class="d-flex" cols="12" sm="3">
        <v-select
          :items="access"
          label="权限选择"
          outlined
          dense
          v-model="access_change"
        ></v-select>
      <v-btn v-popover:verify color="primary" @click="dialog=true">
        确认修改
      </v-btn>

      </v-col>
    </v-container>
<!--    <v-dialog v-model="dialog" max-width="60vh">-->
<!--      <v-card>-->
<!--        <v-toolbar card>Edit User</v-toolbar>-->
<!--        <v-card-text>-->
<!--          <form>-->
<!--            <v-text-field-->
<!--              v-model="formModel.name"-->
<!--              :counter="10"-->
<!--              label="Name"-->
<!--              required-->
<!--            ></v-text-field>-->
<!--            <v-text-field-->
<!--              v-model="formModel.email"-->
<!--              label="E-mail"-->
<!--              required-->
<!--            ></v-text-field>-->
<!--            <v-divider class="mt-3 mb-3"></v-divider>-->
<!--            <v-btn @click="handleSubmit">submit</v-btn>-->
<!--          </form>-->
<!--        </v-card-text>-->
<!--      </v-card>-->
<!--    </v-dialog>-->
    <div class="text-center">
      <v-dialog
        v-model="dialog"
        width="500"
      >
        <v-card>
          <v-card-title
            class="headline grey lighten-2"
            primary-title
          >
            修改确认
          </v-card-title>
          <v-card-text>
            <br/>我们需要确认是管理员或超级权限人员本人进行如下风险操作
          </v-card-text>
          <v-text-field
            append-icon="lock"
            name="paswrd_ck"
            label="请确认密码"
            type="password"
            v-model="passwordck"
          ></v-text-field>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              text
              @click="authchange"
            >
              确认更改
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
<!--    {{this.complex.items}}-->
<!--  <br/>-->
<!--    {{this.complex.selected}}-->
<!--   <br/>-->
<!--    {{this.access_change}}-->
  </div>

</template>

<script>
import { Items as Users } from '@/api/user'
import axios from "axios"
import qs from "qs"
export default {
  data() {
    return {
      access:[{text:"管理员",value:'2'},{text:"职工",value:'1'}],
      access_change:'',
      passwordck:'',
      cktimes:0,
      showsel:false,
      formModel: {
        name: '',
        email: '',
      },
      dialog: false,
      search: '',
      complex: {
        selected: [],
        headers: [
          {
            text: '姓名',
            value: 'username',
          },
          {
            text: '邮箱',
            value: 'email',
          },
          {
              text: '电话',
              value: 'phone',
          },
          {
            text: '权限',
            value: 'authority',
          },
          {
            text: 'Action',
            value: '',
          },
        ],
        items: [],
        // items: Users,
      },

    }
  },
  methods: {
    getdata(){
        const path = 'http://127.0.0.1:5000/accountmanage';
        axios.get(path)
            .then((res) => {
                this.complex.items = res.data.data;
            })
            .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
            });

    },
    authchange(){
        this.dialog = false;
        // if(sessionStorage.getItem('user')===this.$md5(sessionStorage.getItem('token')+'3'))
        let data = {
            username:sessionStorage.getItem('user'),
            token:sessionStorage.getItem('token'),
            passwordck:this.passwordck,
        };
        this.passwordck='';
        const url = "http://127.0.0.1:5000/passwordck/";
        axios
            .post(url,data)
            .then((res)=>{
                console.log(parseInt(res.data.code));
            if(parseInt(res.data.code)===300)
              {
                  this.$message.error({
                      message: '您无权访问',
                  });
                  setTimeout(() => {
                      this.$router.push("/");
                  }, 1000);
              }
            else if(parseInt(res.data.code)===200)
                {
                    this.postdata();
                }
            else if(parseInt(res.data.code)===400)
                {
                    if(this.cktimes >= 3)
                    {
                        this.$message.error({
                            message: '密码错误次数过多，帐号自动注销',
                        });
                        setTimeout(() => {
                            this.$router.push("/auth/login");
                            sessionStorage.clear();
                        }, 1000);
                    }
                    else
                    {
                        this.$message.error({
                            message: '输入密码错误,还剩'+String(3-this.cktimes)+'次机会',
                        });
                        this.cktimes = this.cktimes + 1;
                    }

                }

            })
            .catch((error)=>{
                console.error(error);
            })
    },
    postdata(){
          let data = {
              user:this.complex.selected,
              value:this.access_change,
              curuser:sessionStorage.getItem('user'),
          };
        const url = "http://127.0.0.1:5000/authoritychange/";
        axios
            .post(url,data)
            .then((res)=>{
                if(parseInt(res.data.code)===200)
                {
                    this.$message({
                        message: "修改成功!自动绕过高权限账户",
                        type: 'success'
                    });
                    this.getdata();
                }
                else if(parseInt(res.data.code)===400)
                {
                    this.$message.error({
                        message: '请选择变更人员和变更权限',
                    });
                    // this.win_visible=false;
                }
            })
            .catch((error)=>{
                console.error(error);
            })
    },
    handleClick(row) {
      this.formModel = Object.assign(this.formModel, row);
      this.dialog = true
    },
    /* eslint-disable-line no-unused-vars */
    handleDelete(row) {},
    handleSubmit() {},

  },
    beforeCreate() {
        let token = sessionStorage.getItem('token');
        let user = sessionStorage.getItem('user');
        if(token!==this.$md5(user+'3'))
        {
            this.$router.push('/auth/login');
            this.$message.error('您无权访问该页面！');
        }
    },
    created() {
       this.getdata();
    }
}
</script>
