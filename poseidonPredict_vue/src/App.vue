<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>


export default {
  name: 'App',
  components: {
    // Index
  },
  data() {
    return {
      user: JSON.parse(sessionStorage.getItem('CurUser'))
    };
  },
  watch: {
    '$store.state.menu': {
      handler(val, old) {
        console.log("菜单更新")
        if (!old && this.user && this.user.number) {
          this.$store.commit("setMenu", val)
        }
      },
      immediate: true
    }
  }
}
</script>

<style>
#app {
  height: 100%;
}
</style>
