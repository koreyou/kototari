Vue.use(VueMaterial.default);

const app = new Vue({
  el: '#app',
  data: function() {
    return {
      showDialog: false,
      postTitle: "",
      postContent: "",
      posts: []
    };
  },
  created: function() {
    this.getPosts();
  },
  methods: {
    getPosts: function() {
      this.$http.get('/posts').then((response) => {
	this.posts = response.body.posts;
      }, (response) => {
	console.log('Error GET /posts', response);
      });
    },
    postPosts: function() {
      const post = {
	title: this.postTitle,
	content: this.postContent
      };
      this.showDialog = false;
      this.postTitle = '';
      this.postContent = '';
      this.$http.post('/posts', post).then((response) => {
	console.log('Success POST /posts');
	this.getPosts();
      }, (response) => {
	console.log('Error POST /posts', response);
      });
    },
  },
});
