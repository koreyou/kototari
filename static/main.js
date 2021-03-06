Vue.use(VueMaterial.default);

class Metric {
  constructor(size, score, sentences) {
    this.size = size || 30;
    this.score = score || -1;
    this.sentences = sentences || [];
  }
  style() {
    return {
      'width': this.size + 'px',
      'height': this.size + 'px',
      'line-height': this.size + 'px',
      'background-color': this.color,
    };
  }
}

class Trend extends Metric {
  constructor(size, score, sentences) {
    super(size, score, sentences);
    this.color = "orange";
    this.title = "トレンド";
    this.titleEn = "Trend"
  }
}

class Mentions extends Metric {
  constructor(size, score, sentences) {
    super(size, score, sentences);
    this.color = "indigo";
    this.title = "コメント";
    this.titleEn = "Mentions"
  }
}

class Publicity extends Metric {
  constructor(size, score, sentences) {
    super(size, score, sentences);
    this.color = "teal";
    this.title = "メリット";
    this.titleEn = "Merits"
  }
}


const app = new Vue({
  el: '#app',
  data: function() {
    return {
      mentions: new Mentions(),
      publicity: new Publicity(),
      trend: new Trend(),
      measures: [],
      selected: null,
      keyword: "",
      searched: false,
    };
  },
  methods: {
    sizeStyle: function(s) {
      return {
	'width': s + 'px',
	'height': s + 'px',
	'line-height': s + 'px'
      };
    },
    search: function() {
      function calcSize(x) {
	const BASE_SIZE = 30;
	const SIZE_COEFF = 100;
	const MAX_SIZE = 150;
	return Math.min(SIZE_COEFF * x + BASE_SIZE, MAX_SIZE); 
      }
      this.searched = true;
      const params = {"params": {"keyword": this.keyword}}
      this.$http.get('/publicity-score', params).then((response) => {
	this.publicity = new Publicity(
	  calcSize(response.body.num / response.body.numall),
	  response.body.num,
	  response.body.sentences
	);
	this.publicitySize = calcSize(
	  response.body.num / response.body.numall);
	this.numPublicity = response.body.num;
      }, (response) => {
	console.log('Error GET /publicity-score', response);      
      });
      this.$http.get('/mention-score', params).then((response) => {
	this.mentions = new Mentions(
	  calcSize(response.body.num / response.body.numall) * 1.5,
	  response.body.num,
	  response.body.sentences
	);
      }, (response) => {
	console.log('Error GET /mention-score', response);      
      });
      this.$http.get('/trend-score', params).then((response) => {
	this.trend = new Trend(
	  calcSize(response.body.score) * 0.8,
	  response.body.score,
	  response.body.sentences
	);
	
      }, (response) => {
	console.log('Error GET /trend-score', response);      
      });
      this.$http.get('/measures', params).then((response) => {
	this.measures = response.body.sentences;
      }, (response) => {
	console.log('Error GET /measures', response);      
      });
    },
  },
});


Vue.filter('round', ((value, decimals) => {
  if (!value) {
    value = 0;
  }
  if (!decimals) {
    // Round to 0 (integer)
    decimals = 0;
  }
  const numerator = Math.round(value * Math.pow(10, decimals));
  const delimiter = Math.pow(10, decimals);
  value = numerator / delimiter;
  return value;
}));
