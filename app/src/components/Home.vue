<template>
  <div>
    <nav-bar></nav-bar>
    <section class="section">
      <router-view></router-view>
    </section>
  </div>
</template>

<script>
export default {
  mounted() {
    if (this.$route.query.redirect) {
      // redirect先がクエリに指定されているならリダイレクト
      this.$router.push(this.$route.query.redirect);
    } else {
      // this.$router.push('/dashboard/');
    }
  }
}
</script>