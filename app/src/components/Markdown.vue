<template>
  <div class="container" v-html="content">
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      content: ''
    };
  },
  async mounted() {
    try {
      const res = await axios.get('/api/markdown/index');
      this.content = res.data;
    } catch(err) {
      console.log(err.response);
    }
  }
}
</script>
