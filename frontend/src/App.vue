<template>
  <v-app :dark="true">
    <router-view></router-view>
    <!-- theme setting -->
    <v-btn
      small
      fab
      dark
      falt
      fixed
      top="top"
      right="right"
      class="setting-fab"
      color="red"
      @click="openThemeSettings"
    >
      <v-icon>settings</v-icon>
    </v-btn>
    <!-- setting drawer -->
    <v-navigation-drawer
      class="setting-drawer"
      temporary
      right
      v-model="rightDrawer"
      hide-overlay
      fixed
    >
      <theme-settings></theme-settings>
    </v-navigation-drawer>
    <!-- global snackbar -->
    <v-snackbar
      :timeout="3000"
      bottom
      right
      :color="snackbar.color"
      v-model="snackbar.show"
    >
      {{ snackbar.text }}
      <v-btn dark text @click.native="snackbar.show = false" icon>
        <v-icon>close</v-icon>
      </v-btn>
    </v-snackbar>
  </v-app>
</template>

<script>
import ThemeSettings from '@/components/ThemeSettings'

export default {
  components: {
    ThemeSettings,
  },
  data() {
    return {
      rightDrawer: false,
      snackbar: {
        show: false,
        text: '',
        color: '',
      },
    }
  },

  mounted() {},
  created() {
    // add app events
  },
  methods: {
    openThemeSettings() {
      this.$vuetify.goTo(0)
      this.rightDrawer = !this.rightDrawer
    },
  },
    beforeCreate() {
      let token = sessionStorage.getItem('token');
      let user = sessionStorage.getItem('user');
      if(!token||!user||(token!==this.$md5(user+'1')&&token!==this.$md5(user+'2')&&token!==this.$md5(user+'3')))
      {
          this.$router.push('/auth/login');
          this.$message({
              type:'info',
              message:'登录后方可使用本系统',
          });
      }
    }
}
</script>

<style lang="sass" scoped>
.setting-fab
  top: 50% !important
  right: 0
  border-radius: 0
</style>
