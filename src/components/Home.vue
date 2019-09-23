<template>
  <section class="section">
    <div class="container">
      <div class="markdown-body" v-html="markdown_html"></div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import marked from 'marked'

export default {
  data() {
    return {
      markdown_html: ''
    }
  },

  async mounted() {
    const res = await axios.get('/index.md')
    this.markdown_html = marked(res.data)

    // code block highlight
    hljs.initHighlightingOnLoad()
  }
}
</script>
