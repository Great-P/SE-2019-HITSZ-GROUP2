<template>
  <v-card
    class="mx-auto"
    max-width="600"
    max-height="900"
    outlined
  >
    <v-list-item three-line>
      <v-list-item-content>
        <div class="overline mb-4">用户卡片</div>
        <v-list-item-title class="headline mb-1">基本信息</v-list-item-title>
        <v-list-item-subtitle>坪山区人民政府</v-list-item-subtitle>
      </v-list-item-content>

      <v-list-item-content>
        <div class="">
          <v-list-item-title class="headline mb-1">{{items.username}}</v-list-item-title><br/>
          <v-list-item-title>电话:{{items.phone}}</v-list-item-title><br/>
          <v-list-item-title>邮箱:{{items.email}}</v-list-item-title><br/>
          <v-list-item-title>权限:{{items.authority}}</v-list-item-title><br/>
        </div>
      </v-list-item-content>

<!--      <v-list-item-avatar-->
<!--        tile-->
<!--        size="80"-->
<!--        color="grey"-->
<!--      ></v-list-item-avatar>-->

    </v-list-item>

    <v-card-actions>
      <v-btn text @click="dialog_password=!dialog_password">修改密码</v-btn>
      <v-btn text @click="dialog_info=!dialog_info">信息修改</v-btn>
      <v-spacer></v-spacer>
      <v-list-item-avatar
        size="30"
        color="blue"
      ></v-list-item-avatar>
    </v-card-actions>




    <div class="text-center">
      <v-dialog
        v-model="dialog_password"
        width="500"
      >
        <v-card>
          <v-card-title
            class="headline grey lighten-2"
            primary-title
          >
            密码修改
          </v-card-title>

          <v-text-field
            append-icon="lock"
            name="oldpassword"
            label="请输入旧密码"
            type="password"
            v-model="passwordchange.oldpassword"
          ></v-text-field>
          <v-text-field
            append-icon="edit"
            name="newpassword"
            label="请输入新密码"
            type="password"
            v-model="passwordchange.newpassword"
          ></v-text-field>
          <v-text-field
            append-icon="gavel"
            name="password_ck"
            label="确认密码"
            id="password_ck"
            type="password"
            v-model="passwordchange.newpasswordck"
          ></v-text-field>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              text
              @click="password_change"
            >
              确认更改
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>

    <div class="text-center">
      <v-dialog
        v-model="dialog_info"
        width="500"
      >
        <v-card>
          <v-card-title
            class="headline grey lighten-2"
            primary-title
          >
            信息修改
          </v-card-title>

          <v-text-field
            append-icon="phone"
            name="phone"
            label="电话号码"
            id="phone_number"
            type="text"
            counter = 11
            v-model="infochange.phone"
          ></v-text-field>
          <v-text-field
            append-icon="email"
            name="email"
            label="邮箱"
            id="email"
            type="text"
            v-model="infochange.email"
          ></v-text-field>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              text
              @click="info_change"
            >
              确认更改
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-card>





</template>

<script>
    import axios from "axios"
    import qs from "qs"
    export default {
        name: "userinfo",
        data(){
            return{
                dialog_password:false,
                dialog_info:false,
                items:{
                    username:'NO DATA',
                    phone:'NO DATA',
                    email:'NO DATA',
                    authority:'NO DATA',
                },
                passwordchange:{
                    oldpassword:'',
                    newpassword:'',
                    newpasswordck:'',
                },
                infochange:{
                    phone:'',
                    email:'',
                }

            }
        },
        methods:{
            getdata(){
                  let data = {
                      user:sessionStorage.getItem('user'),
                  };
                  const url = "http://127.0.0.1:5000/getuser/";
                  axios
                      .post(url,data)
                      .then((res)=>{
                            this.items = res.data.data;
                      })
                      .catch((error)=>{
                          console.error(error);
                      })
              },
            password_change(){
                let data={
                    oldpassword:this.passwordchange.oldpassword,
                    newpassword:this.passwordchange.newpassword,
                    newpasswordck:this.passwordchange.newpasswordck,
                    curuser:sessionStorage.getItem('user'),
                };
                const url = "http://127.0.0.1:5000/passwordchange/";
                axios
                    .post(url,data)
                    .then((res)=>{
                        if(parseInt(res.data.code)===200)
                        {
                            this.$message({
                                message: "密码修改成功,请重新登录",
                                type: 'success'
                            });
                            sessionStorage.clear();
                            setTimeout(() => {
                                this.$router.push("/auth/login");
                            }, 1000);
                        }
                        else if(parseInt(res.data.code)===400)
                        {
                            this.$message.error({
                                message: '修改失败，请填写表格相关信息',
                            });
                            // this.win_visible=false;
                        }
                        else if(parseInt(res.data.code)===301)
                        {
                            this.$message.error({
                                message: '密码验证错误！',
                            });
                            // this.win_visible=false;
                        }
                        else if(parseInt(res.data.code)===300)
                        {
                            this.$message.error({
                                message: '两次新密码输入不一致！',
                            });
                            // this.win_visible=false;
                        }
                        this.passwordchange.oldpassword='';
                        this.passwordchange.newpassword='';
                        this.passwordchange.newpasswordck='';
                        this.dialog_password = !this.dialog_password;
                    })
                    .catch((error)=>{
                        console.error(error);
                    })
            },
            info_change(){
                let data = {
                    phone:this.infochange.phone,
                    email:this.infochange.email,
                    user:sessionStorage.getItem('user'),
                };
                const url = "http://127.0.0.1:5000/infochange/";
                axios
                    .post(url,data)
                    .then((res)=>{
                        if(parseInt(res.data.code)===200)
                        {
                            this.$message({
                                message: "信息修改成功",
                                type: 'success'
                            });
                            this.getdata();
                            this.dialog_info = !this.dialog_info;
                        }
                    })
                    .catch((error)=>{
                        console.error(error);
                    })
            },



          },

        created() {
            this.getdata();
        }

    }
</script>

<style scoped>

</style>