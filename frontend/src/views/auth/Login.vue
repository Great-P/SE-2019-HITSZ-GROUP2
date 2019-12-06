<template>
  <div class="login">
  <v-card class="elevation-1 pa-3 login-card">
    <v-card-text>
      <v-layout align-center justify-center column fill-height>
        <img
          src="/static/hitsz.jpg"
          alt="Vue Material Admin"
          width="120"
          height="120"
        />
        <h1 class="my-4 primary--text display-1">政府数据分析平台登录</h1>
      </v-layout>
      <v-form>
        <v-text-field
          append-icon="person"
          name="login"
          label="Login"
          type="text"
          v-model="model.username"
          placeholder="请输入用户名"
        ></v-text-field>
        <v-text-field
          append-icon="lock"
          name="password"
          label="Password"
          id="password"
          type="password"
          v-model="model.password"
          placeholder="请输入密码"
        ></v-text-field>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="jump">
        <v-icon color="blue">edit</v-icon>
        注册
      </v-btn>
      <v-btn color="primary" @click="toindex">
        <v-icon color="blue">people</v-icon>
        主页
      </v-btn>

      <v-spacer></v-spacer>
      <v-btn v-popover:verify color="primary" @click="" :loading="win_visible">
        登录
      </v-btn>
<!--      <el-button v-popover:test type="primary" :loading="win_visible" >登录</el-button>-->
    </v-card-actions>
  </v-card>

    <el-popover
      ref="verify"
      width="200px"
      trigger="click"
      @show="win_visible=true"
      @hide="win_visible=false"
    >
      <slide-verify
        :l="42"
        :r="10"
        :w="310"
        :h="155"
        @success="login"
        @fail=""
        :slider-text="tips"
        :pic_src='"../assets/images/back.jpg"'
      ></slide-verify>
    </el-popover>

  </div>
</template>

<script>
import axios from "axios"
import qs from "qs"

export default {
    name:"login",
    data: () => ({
    loading: false,
    model: {
      username: '',
      password: '',
    },
    win_visible:false,
  }),

  methods: {
    login() {
        let data={
        username: this.model.username,
        password: this.model.password,
        };
        const url = "http://127.0.0.1:5000/login/";
        axios
            .post(url,qs.stringify(data))
            .then((res)=>{
                if(parseInt(res.data.code)===200)
                {
                    this.$message({
                        message: "登录成功!",
                        type: 'success'
                    });

                    sessionStorage.setItem("token",res.data.token);
                    sessionStorage.setItem("user",this.model.username)
                    setTimeout(() => {
                        this.$router.push("/dashboard");
                    }, 1000);

                }
                else if(parseInt(res.data.code)===400)
                {
                    this.$message.error({
                        message: '登录失败，请检查你的用户名和密码',
                    });
                    // this.win_visible=false;
                }
            })
            .catch((error)=>{
                console.error(error);
            })
    },
      jump(){
          this.$message("跳转中……");
        setTimeout(() => {
              this.$router.push("/auth/register");
          }, 1000);
      },
      toindex(){
          this.$message("回到主页……");
          setTimeout(() => {
              this.$router.push("/");
          }, 1000);
      }
  },
}
</script>
<style lang="sass" scoped></style>
