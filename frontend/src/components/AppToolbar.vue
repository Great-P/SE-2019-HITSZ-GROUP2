<template>
  <v-app-bar color="primary" dark app>
    <v-app-bar-nav-icon @click="handleDrawerToggle" />
    <v-spacer />
    <v-toolbar-items>
      <!--      <v-btn icon @click="handleFullScreen()">-->
      <!--        <v-icon>fullscreen</v-icon>-->
      <!--      </v-btn>-->
      <v-menu
        offset-y
        origin="center center"
        :nudge-bottom="10"
        transition="scale-transition"
      >
        <template v-slot:activator="{ on }">
          <v-btn large text slot="activator" v-on="on">

            {{ username }}
          </v-btn>
        </template>
        <v-list class="pa-0">
          <v-list-item
            v-for="(item, index) in items"
            :to="!item.href ? { name: item.name } : null"
            :href="item.href"
            @click="item.click"
            ripple="ripple"
            :disabled="item.disabled"
            :target="item.target"
            rel="noopener"
            :key="index"
          >
            <v-list-item-action v-if="item.icon">
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-toolbar-items>
    <v-dialog
      v-model="showProfile"
      hide-overlay

      width="600"
    >
      <v-card>
        <v-img src="/static/people/man/hxm.jpg" height="390">
          <v-layout column class="media ma-0">
            <v-card-title>
              <v-btn dark icon>
                <v-icon @click="showProfile=!showProfile">chevron_left</v-icon>
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn dark icon class="mr-3">
                <v-icon @click="edit">edit</v-icon>
              </v-btn>
              <!--              <v-btn dark icon>-->
              <!--              <v-icon>more_vert</v-icon>-->
              <!--            </v-btn>-->
            </v-card-title>
            <v-spacer></v-spacer>
            <v-card-title class="white--text pl-5 pt-5">
              <div class="display-1 pl-5 pt-5">{{ UserProfile.UserName }}</div>
            </v-card-title>
          </v-layout>
        </v-img>
        <v-list two-line class="pa-0">
          <v-list-item href="#">
            <v-list-item-action>
              <v-icon color="indigo">phone</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ UserProfile.MobilePhone }}</v-list-item-title>
              <v-list-item-subtitle>手机号</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider inset></v-divider>
          <v-list-item href="#">
            <v-list-item-action>
              <v-icon color="indigo">mail</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ UserProfile.Email }}</v-list-item-title>
              <v-list-item-subtitle>邮箱</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider inset></v-divider>
          <v-list-item href="#">
            <v-list-item-action>
              <v-icon color="indigo">location_on</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ UserProfile.authority }}</v-list-item-title>
              <v-list-item-subtitle>职责</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card>

    </v-dialog>

  </v-app-bar>

</template>
<script>
    import NotificationList from '@/components/widgets/list/NotificationList'
    import Util from '@/util'
    import ProfileCard from '@/components/new/ProfileCard'
    import axios from "axios"
    import qs from "qs"
    export default {
        name: 'AppToolbar',
        components: {
            NotificationList,
            ProfileCard,
        },
        data() {
            return {
                username: "请登录",
                showProfile: false,
                UserProfile: {
                    UserName: "未登录",
                    MobilePhone: '未登录',
                    Email: '未登录',
                    authority: '未登录',
                },
                notifications: [
                    {
                        title: '请及时查看突发事件',
                        color: 'light-green',
                        icon: 'account_circle',
                        timeLabel: '现在',
                    },
                    { divider: true, inset: true },
                    {
                        title: '今晚18:00召开大会',
                        color: 'light-blue',
                        icon: 'shopping_cart',
                        timeLabel: '15 分钟前',
                    },
                    { divider: true, inset: true },
                    {
                        title: '请及时查看昨日报表',
                        color: 'light-blue',
                        icon: 'shopping_cart',
                        timeLabel: '32 分钟前',
                    },
                ],
                items_login: [
                    {
                        icon: 'account_circle',
                        href: '#',
                        title: '属性',
                        click: this.handleProfile,
                    },
                    {
                        icon: 'settings',
                        href: '#',
                        title: '设置',
                        click: this.handleSetting,
                    },
                    {
                        icon: 'fullscreen_exit',
                        href: '#',
                        title: '登录',
                        click: this.handleLogin,
                    },
                ],
                items_logout: [
                    {
                        icon: 'account_circle',
                        href: '#',
                        title: '属性',
                        click: this.handleProfile,
                    },
                    {
                        icon: 'fullscreen_exit',
                        href: '#',
                        title: '注销',
                        click: this.handleLogut,
                    },
                ],
                items :[],
            }
        },
        computed: {
            toolbarColor() {
                return this.$vuetify.options.extra.mainNav
            },
        },
        methods: {
            handleDrawerToggle() {
                this.$emit('side-icon-click')
            },
            handleFullScreen() {
                Util.toggleFullScreen()
            },
            handleLogut() {
                this.$message({
                    type: "success",
                    message: "注销成功!"
                });
                this.$router.push('/auth/login');
                sessionStorage.clear();
                this.username = '请登录';
                this.UserProfile.UserName='请登录';
                this.items=this.items_login;
            },
            handleLogin(){
                this.$message("跳转中……");
                setTimeout(() => {
                    this.$router.push("/auth/login");
                }, 1000);
            },
            handleSetting() {},
            handleProfile() {
                this.showProfile = true;
            },
            getdata(){
                let data = {
                    user:sessionStorage.getItem('user'),
                };
                const url = "http://127.0.0.1:5000/getuser/";
                axios
                    .post(url,data)
                    .then((res)=>{
                        let info = res.data.data;
                        this.UserProfile.UserName=info.username;
                        this.UserProfile.MobilePhone=info.phone;
                        this.UserProfile.Email=info.email;
                        this.UserProfile.authority=info.authority;
                    })
                    .catch((error)=>{
                        console.error(error);
                    })
            },
            edit(){
                this.$router.push('/userinfo/userinfo');
                this.showProfile = false;
            }
        },
        created() {
            if(sessionStorage.getItem('user'))
            {
                this.getdata();
                this.username = sessionStorage.getItem('user');
                // this.UserProfile.UserName=sessionStorage.getItem('user');
                this.items=this.items_logout;
            }
            else
            {
                this.items=this.items_login;
            }
        },
    }
</script>

<style lang="sass" scoped></style>
