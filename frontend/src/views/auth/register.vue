<template>
  <div class="register">
    <v-card class="elevation-1 pa-3 login-card">
      <v-card-text>
        <v-layout align-center justify-center column fill-height>
          <img
            src="/static/hitsz.jpg"
            alt="Vue Material Admin"
            width="120"
            height="120"
          />
          <h1 class="my-4 primary--text display-1">政府数据分析平台注册</h1>
        </v-layout>
        <v-form>
          <v-text-field
            append-icon="person"
            name="login"
            label="用户名"
            type="text"
            v-model="model.username"
          ></v-text-field>
          <v-text-field
            append-icon="phone"
            name="phone"
            label="电话号码"
            id="phone_number"
            type="text"
            counter = 11
            v-model="model.phone"
          ></v-text-field>
          <v-text-field
            append-icon="email"
            name="email"
            label="邮箱"
            id="email"
            type="text"
            v-model="model.email"
          ></v-text-field>
          <v-text-field
            append-icon="lock"
            name="password"
            label="设置密码"
            id="password"
            type="password"
            v-model="model.password"
          ></v-text-field>
          <v-text-field
            append-icon="gavel"
            name="password_ck"
            label="确认密码"
            id="password_ck"
            type="password"
            v-model="model.pswrd_ck"
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>

        <v-btn color="primary" @click="jump">
          <v-icon color="blue">edit</v-icon>
          登录
        </v-btn>

        <v-spacer></v-spacer>
        <v-btn v-popover:verify color="primary" @click="register">
          注册
        </v-btn>
        <!--      <el-button v-popover:test type="primary" :loading="win_visible" >登录</el-button>-->
      </v-card-actions>
    </v-card>

  </div>
</template>

<script>
    import axios from "axios"
    import qs from "qs"
    export default {
        name: "register",
        data() {
            return {
                model:{
                username: "",
                phone:"",
                email:"",
                password: "",
                pswrd_ck: "",
                authority:'1',
                }
            }
        },
        methods:{
            register() {
                let data={
                    username: this.model.username,
                    password: this.model.password,
                    pswrd_ck: this.model.pswrd_ck,
                    phone: this.model.phone,
                    email: this.model.email,
                    authority: this.model.authority
                };
                const url = "http://127.0.0.1:5000/register/";
                axios
                    .post(url,qs.stringify(data))
                    .then((res) => {
                        if (parseInt(res.data.code)===200)
                        {
                            this.$message({
                                message: "注册成功!",
                                type: 'success'
                            });
                            setTimeout(() => {
                                this.$router.push("/auth/login");
                            }, 1000);
                        }
                        else if(parseInt(res.data.code)===400)
                        {
                            this.$message.error({
                                message: '两次密码输入不一致！',
                            });
                            const ac=res.data.account;
                            this.model.username=ac["username"];
                            this.model.password=ac["password"];
                            this.model.pswrd_ck=''
                        }
                        else if (parseInt(res.data.code)===500)
                        {
                            this.$message.error({
                                message: "所有填写信息均不能为空！",
                            });
                        }
                        else if (parseInt(res.data.code)===300)
                        {
                            this.$message.error({
                                message: "用户已存在!",
                            });
                        }
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            },
            jump(){
                this.$message("跳转中……");
                setTimeout(() => {
                    this.$router.push("/auth/login");
                }, 1000);
            },
            channelInputLimit (e){
                let key = e.key;
                // 不允许输入'e'和'.'
                if (key === 'e' || key === '.') {
                    e.returnValue = false;
                    return false
                }
                return true
            },
        }
    }
</script>
<style lang="sass" scoped></style>
