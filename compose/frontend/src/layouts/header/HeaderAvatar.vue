<template>
  <a-dropdown>
    <div class="header-avatar" style="cursor: pointer" v-if="user">
      <a-avatar class="avatar" size="small" shape="circle" :src="user.avatar" />
      <span class="name">{{ user.username }}</span>
    </div>
    <div class="header-avatar" style="cursor: pointer" v-else>
      <a-spin size="small" />
    </div>
    <a-menu :class="['avatar-menu']" slot="overlay">
      <a-menu-item @click="logOut">
        <a-icon style="margin-right: 8px" type="poweroff" />
        <span>退出登录</span>
      </a-menu-item>
    </a-menu>
  </a-dropdown>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import { logout } from '@/services/users'

export default {
  name: 'HeaderAvatar',
  computed: {
    ...mapGetters('account', ['user'])
  },
  methods: {
    ...mapMutations('account', ['removeUser']),
    logOut() {
      logout()
      this.removeUser()
      this.$router.push('/login')
    }
  }
}
</script>

<style lang="less">
.header-avatar {
  display: inline-flex;
  .avatar,
  .name {
    align-self: center;
  }
  .avatar {
    margin-right: 8px;
  }
  .name {
    font-weight: 500;
  }
}
.avatar-menu {
  width: 150px;
}
</style>
