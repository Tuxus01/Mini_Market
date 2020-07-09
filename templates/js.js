<script>
var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
      message: 'Hello Vue!',
      people: people,
  },
  methods: {
      greet: function(name) {
          console.log('Hello from ' + name + '!')
      }
  }
});
</script>