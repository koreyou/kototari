Vue.use(VueMaterial.default);

const CardContainer = {
  template: `<div class="viewport">
    <h3 class="md-title">{{ title }}</h3>
    <md-card v-for="(items, valueName) in result[position]"
      :key="valueName" md-with-hover>
         <md-ripple>
           <md-card-header>
             <div class="md-subheading">{{ valueName }}</div>
             <i class="badge">{{ items.length }}</i>
           </md-card-header>
           <md-card-content>
             <p class="card-text caption">
               <template v-for="item in items">
                 {{ sentences[item].text }}
               </template>
             </p>
           </md-card-content>
           <md-card-actions>
           <md-button @click="selectValue(position, valueName)">
             Show
           </md-button>
           </md-card-actions>
         </md-ripple>
       </md-card>
  </div>`,
  props: ['result', 'position', 'sentences', 'selectValue', 'title'],
};


const app = new Vue({
  el: '#app',
  data: function() {
    return {
      // 定数としてエンドポイントを記載
      api_endpoint: {
        value_search: 'https://133.145.160.206/nlu/v1/value-dictionaries:search',
        supportiveness_classify: 'https://133.145.160.206/nlu/v1/sentences/supportiveness',
        speech: 'https://133.145.160.206/media/v1/speech',
      },
      keyword: '',
      // 賛否(for|against) から、価値-文オブジェクトに射影する。
      // 価値-文オブジェクトは価値(str)から文IDのリスト(list of str)に射影する。
      result: {
        for: {},
        against: {},
      },
      // 文ID (str)から文の実体(str)に射影する。md-steppersの@md-changed
      // がIDを使うため、上記resultと分けている。
      sentences: {},
      // 2つの変数はユーザがどのcardを選んだかを記録
      selectedValue: null,
      selectedPosition: 'for',
      showDialog: false,
      audioURL: null,
      // 0: 初期状態、1: 検索中、2: 検索完了
      inProcess: 0,
      authKey: "",
      // 0: 初期状態、1: ログイン中、3: ログイン完了、4: エラー
      authStatus: 0,
      authPrompt: false,
    };
  },
  mounted: function() {
    // this.audioURLが書き換えられると自動的にトリガーされる
    this.$watch('audioURL', function() {
      console.log('Start playing ' + this.audioURL);
      // .play()はDOMの書き換えを待たなければならないため
      setTimeout(function() {
        app.$refs.audio.play();
      }, 500);
    });
  },
  components: {
    'card-container': CardContainer,
  },
  methods: {
　　authenticate: function() {
      // sentence APIのみ使っているのでglobalに設定
      Vue.http.headers.common['Authorization'] = "Bearer " + this.authKey;
      this.authStatus = 1;
      // Test sentence
      const body = [
         {
              "keyword": "喫煙 タバコ",
              "text": "世界保健機関は「安全な受動喫煙は存在しない」という。",
              "value": "health",
              "value_category": "health"
          }
      ];
      this.$http.post(this.api_endpoint.supportiveness_classify, body)
        .then(function(response) {
            this.authStatus = 2;
        }, function(response) {
            console.log('supportiveness failed when testing authorization', response);
            this.authStatus = 3;
        });
    },
    search: function() {
      this.inProcess = 1;
      this.result = {
        for: {},
        against: {},
      };
      let params = {
        'value_dictionary_id': '1',
        'keyword': this.keyword,
      };
      this.$http.get( this.api_endpoint.value_search, {'params': params})
        .then(function(response) {
          console.log('Value search OK');
          console.log(response.body);
          const sent = [];
          for (const issue of response.body.results) {
            sent.push({
              'text': issue['text'],
              'keyword': response.body.keyword,
              'value': issue['value'],
              'value_category': issue['value_category'],
            });
          }

          return this.$http.post(
            this.api_endpoint.supportiveness_classify, sent
          ).then(function(response) {
            console.log(['supportiveness OK', response]);
            console.log(response);
            const predictions = response.body.predictions;
            for (const i in predictions) {
              if ({}.hasOwnProperty.call(predictions, i)) {
                const r = predictions[i];
                if (r['label'] != 'o') {
                  let result = null;
                  if (r['label'] == 'p') {
                    result = this.result.for;
                  } else {
                    result = this.result.against;
                  }
                  const valueId = sent[i].value_category + '-' + sent[i].value;
                  const sentenceId = valueId + i;
                  const supportivenessSentence = {
                    'text': r['text']};
                  if (!result.hasOwnProperty(valueId)) {
                    this.$set(result, valueId, []);
                  }
                  const rlength = result[valueId].length;
                  this.$set(this.sentences, sentenceId, supportivenessSentence);
                  this.$set(result[valueId], rlength, sentenceId);
                }
              }
            }
          }, function(response) {
            console.log('supportiveness failed');
            console.log(response);
          });
        }, function(response) {
          console.log('Value search failed');
          console.log(response);
          return Promise.reject();
        }).then(function(response) {
          this.inProcess = 2;
          console.log('The whole process succeeded');
        }, function(response) {
          console.log('The process failed');
          this.inProcess = 0;
          alert('Oops... something went wrong. Please contact admin.');
        });
    },
    selectValue: function(position, valueName) {
      this.selectedValue = valueName;
      this.selectedPosition = position;
      this.showDialog = true;
      // slippersの@md-changedは最初の要素に対してトリガーされない
      this.getAudio(this.result[position][valueName][0]);
    },
    getAudioURL: function(text) {
      console.log('Speech POST request', text);
      return this.$http.post(
        this.api_endpoint.speech, text
      ).then(function(response) {
        const speechId = response.body.speech_id;
        // Promiseを返すとこのpromiseが現在のpromiseにチェインされている
        // ような挙動をする。speechIdを参照したいためこのような形。
        return new Promise(function(resolve, reject) {
          // pollSpeechはポリングが成功するまで再帰的に自分を呼び続ける
          (function pollSpeech() {
            // Promiseオブジェクト内でthisへの参照が書き換わる
            app.$http.get(
              app.api_endpoint.speech + '/' + speechId
            ).then(function(response) {
              console.log(response);
              if (response.status == '200') {
                resolve(response.body.url);
                return;
              }
              setTimeout(pollSpeech, 2000);
            }, function(response) {
              reject(response);
            });
          })();
        });
      }, function(response) {
        console.log(['Speech POST failed', response]);
      });
    },
    getAudio: function(valueId) {
      this.getAudioURL(
        this.sentences[valueId].text
      ).then(function(url) {
        console.log(url);
        this.audioURL = url;
      }, function(response) {
        console.log(['Speech GET failed', response]);
      });
    },
  },
});
