<template>
  <v-card>
    <v-img src="/static/people/man/m1.jpg" height="390">
      <v-layout column class="media ma-0">
        <v-card-title>
          <v-btn dark icon @click="back">
            <v-icon>chevron_left</v-icon>
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn dark icon class="mr-3">
            <v-icon>edit</v-icon>
          </v-btn>
          <v-btn dark icon>
            <v-icon>more_vert</v-icon>
          </v-btn>
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
          <v-list-item-title>{{ UserProfile.Office }}</v-list-item-title>
          <v-list-item-subtitle>办公室</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
  export default {

    data() {
      return {
        UserProfile: {
          UserName: '',
          MobilePhone: '',
          Email: '',
          Office: '',
        },
      }
    },

      methods:{
        back(){
            this.$router.push('/');
        },
      },
  }
</script>
