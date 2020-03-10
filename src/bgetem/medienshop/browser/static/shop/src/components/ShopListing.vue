<template>
  <div>
<!--
    <div class="row">
      <filter-search @filtersearch="doSomething"></filter-search>
    </div>
-->
    <div class="row mp-filter" v-if="iscollection == '0'">
      <FilterElementButton v-bind:category="cats.themen" v-bind:active="show_filter == cats.themen.id" @show_menu="activateCategory" />

      <FilterElementButton v-bind:category="cats.zielgruppen" v-bind:active="show_filter == cats.zielgruppen.id" @show_menu="activateCategory" />

      <FilterElementButton v-bind:category="cats.medienart" v-bind:active="show_filter == cats.medienart.id" @show_menu="activateCategory" />

      <FilterElementButton v-bind:category="cats.branchen" v-bind:active="show_filter == cats.branchen.id" @show_menu="activateCategory" />

      <transition-group name="menu">

        <filter-element v-if="show_filter == cats.themen.id" name="themen" type="normal" :key="cats.themen.id" v-bind:category="cats.themen" @fsearch="filterCategory" />

        <filter-element v-if="show_filter == cats.zielgruppen.id" name="zielgruppen" type="normal" :key="cats.zielgruppen.id" v-bind:category="cats.zielgruppen" @fsearch="filterCategory" />

        <filter-element v-if="show_filter == cats.medienart.id" name="medienart" type="normal" :key="cats.medienart.id" v-bind:category="cats.medienart" @fsearch="filterCategory" />

        <filter-element v-if="show_filter == cats.branchen.id" name="branchen" type="grouped" :key="cats.branchen.id" v-bind:category="cats.branchen" @fsearch="filterCategory" />
      </transition-group>
    </div>
    <div class="row" v-if="iscollection == '0'">
      <p class="mp-filter-display col-lg-2 col-sm-3">Gesetzte Filter:</p>
      <button @click.prevent="removeFilter(filter_item)" v-for="filter_item in getFilter" v-bind:key="filter_item" type="button" class="btn mp-btn-secondary mp-btn-sm">
        {{filter_item}}
        <span class="glyphicon glyphicon-remove-sign" aria-hidden="true"></span>
      </button>
    </div>
    <div class="row">
      <!--
      <div class="col-xs-12 col-sm-7">
	      <p class="mp-filter-display col-sm-6 col-xs-12">Ergebnisse sortieren nach:  </p>
	      <div class="btn-group mp-item-organization col-xs-12 col-sm-2 dropdown">
		      <button class="btn mp-btn-default mp-btn-xs dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Neueste zuerst<span class="caret"></span>
		      </button>
		      <ul class="dropdown-menu">
			      <li v-for="sortitem in sortItems" :key="sortitem.key">
              <span class="small">
               <input type="checkbox" :value="sortitem.key" v-model="selectedSortItems">
               <span :for="sortitem.value">{{sortitem.value}}</span>
              </span>
            </li>
		       </ul>
        </div>	
      </div>
      -->
      <p class="mp-filter-display-number col-xs-12 col-sm-3"> Gefundene Artikel: {{getArticles.length}} </p>
    </div>
    <div v-for="article in i_articles" v-bind:key="article.key">
      <article-view :user=user :article=article v-bind:key="article.artnr">
      </article-view>
    </div>
    <infinite-loading :identifier="infiniteId" @infinite="infiniteHandler">
      <div slot="no-results">Es wurden keine Ergebnisse gefunden.</div>
      <div slot="no-more">Keine weiteren Artikel vorhanden.</div>
    </infinite-loading>
  </div>
</template>

<script>
import ArticleView from "./ArticleView.vue";
import FilterElement from "./FilterElement.vue";
import FilterSearch from "./FilterSearch.vue";
import FilterElementButton from "./FilterElementButton";
import { orderBy } from 'lodash';
import InfiniteLoading from 'vue-infinite-loading';

function remove(array, element) {
  let index = array.indexOf(element);
  array.splice(index, 1);
}


function containsAny(source,target)
{
  var result = source.filter(function(item){ return target.indexOf(item) > -1});   
	return (result.length > 0); 
}

export default {
  mounted() {
  if (sessionStorage.getItem("category") === null) {
    var ma = JSON.parse(this.medienarten);
    this.cats.medienart.values = ma.medienarten;
    this.cats.branchen.values = ma.branchen;
    this.cats.zielgruppen.values = ma.zielgruppen;
    this.cats.themen.values = ma.themen;
    }
  else {
    this.cats = JSON.parse(sessionStorage.getItem("category"));
    }
  },
  props: {
    articles: {
      type: String
    },
    medienarten: {
      type: String
    },
    shop_url: {
      type: String
    },
    user: {
      type: String
    },
    iscollection: {
      type: String,
      default: '0'                                                                                                                                                          }
  },
  computed: {
    getFilter() {
      var f = Array();
      return f.concat(
        this.cats.medienart.filter,
        this.cats.branchen.filter,
        this.cats.themen.filter,
        this.cats.zielgruppen.filter
      );
    },
    getArticles() {
      //console.log('getArticle')
      var articles = JSON.parse(this.articles);
      if (this.search.text != "") {
        var articles = articles.filter(
          article =>
            article.title.toLowerCase().indexOf(this.search.text.toLowerCase()) >= 0 ||
            article.desc.toLowerCase().indexOf(this.search.text.toLowerCase()) >= 0 ||
            article.artnr.toLowerCase().indexOf(this.search.text.toLowerCase()) >= 0
        );
      }
      if (this.cats.medienart.filter.length > 0) {
        var articles = articles.filter(article =>
          this.cats.medienart.filter.includes(article.medienart)
        );
      }
      if (this.cats.themen.filter.length > 0) {
        var articles = articles.filter(article => containsAny(this.cats.themen.filter, article.themen));
      }
      if (this.cats.zielgruppen.filter.length > 0) {
        var articles = articles.filter(article => containsAny(this.cats.zielgruppen.filter, article.zielgruppen));
      }
      if (this.cats.branchen.filter.length > 0) {
        var articles = articles.filter(article => containsAny(this.cats.branchen.filter, article.branchen));
      }
      /*
      if (this.selectedSortItems.length > 0) {
        console.log(articles)
        console.log(this.selectedSortItems)
        var articles = orderBy(articles, this.selectedSortItems)
      }
      */
      //console.log(articles)
      return articles;
    }
  },
  methods: {
    removeFilter(event) {
      if (this.cats.medienart.filter.includes(event)) {
        remove(this.cats.medienart.filter, event);
        var cats = JSON.parse(sessionStorage.getItem("category"));
        remove(cats.medienart.filter, event)
        sessionStorage.setItem("category", JSON.stringify(this.cats));
      }
      if (this.cats.themen.filter.includes(event)) {
        remove(this.cats.themen.filter, event);
        var cats = JSON.parse(sessionStorage.getItem("category"));
        remove(cats.themen.filter, event)
        sessionStorage.setItem("category", JSON.stringify(this.cats));
      }
      if (this.cats.zielgruppen.filter.includes(event)) {
        remove(this.cats.zielgruppen.filter, event);
        var cats = JSON.parse(sessionStorage.getItem("category"));
        remove(cats.zielgruppen.filter, event)
        sessionStorage.setItem("category", JSON.stringify(this.cats));
      }
      if (this.cats.branchen.filter.includes(event)) {
        remove(this.cats.branchen.filter, event);
        var cats = JSON.parse(sessionStorage.getItem("category"));
        remove(cats.branchen.filter, event)
        sessionStorage.setItem("category", JSON.stringify(this.cats));
      }
      this.infiniteId += 1;
      this.i_articles = [];
    },
    doSomething(event) {
      //console.log('Trigger BASE SEARCH')
      this.search.text = event;
      this.infiniteId += 1;
      this.i_articles = [];
    },
    filterCategory(event) {
      let category = this.cats[event.name];
      category.filter.push(event.category);
      this.show_filter = "";
      sessionStorage.setItem("category", JSON.stringify(this.cats));
      this.infiniteId += 1;
      this.i_articles = [];
    },
    activateCategory(event) {
      console.log(event.name);
      this.show_filter = event.name == this.show_filter ? "" : event.name;
    },
    infiniteHandler($state) {
        const temp = [];
        var articles = this.getArticles
        var all = articles.length
        var start = this.i_articles.length
        if (start < all) {
          //console.log('SETTING ALL INFINITE_ARTICLE ')
          this.i_articles = this.i_articles.concat(articles.slice(start, start+30)) 
          $state.loaded();
        }
        else {
          //console.log('SETTING I_ARTICLE ')
          $state.complete();
        }
        }
  },
  data() {
    return {
      infiniteId: +new Date(),
      i_articles: [],
      sortItems: [
        {key: 'title', value: 'Titel'},
        {key: 'artnr', value: 'Artikelnummer'},
        {key: 'preis', value: 'Preis'}
      ],
      selectedSortItems: [],
      search: {
        text: ""
      },
      show_filter: "",
      cats: {
        medienart: {
          id: "medienart",
          title: "Medienart",
          values: [],
          filter: []
        },
        branchen: {
          id: "branchen",
          title: "Branchen",
          values: [],
          filter: [],
	  top_categories: []
        },
        zielgruppen: {
          id: "zielgruppen",
          title: "Zielgruppen",
          values: [],
          filter: []
        },
        themen: {
          id: "themen",
          title: "Themen",
          values: [],
          filter: []
        }
      }
    };
  },
  components: {
    ArticleView,
    FilterElement,
    FilterSearch,
    FilterElementButton,
    InfiniteLoading
  }
};
</script>



<style scoped>

span.small{
white-space: normal !important;
padding: 5px 15px;
}

.articles {
  backface-visibility: hidden;
  z-index: 1;
}

div.category ul.dropdown-menu {
  width: 100%;
}

/* moving */
.articles-move {
  transition: all 1s ease-in-out 50ms;
}

/* appearing */
.articles-enter-active {
  transition: all 1s ease-out;
}

/* disappearing */
.articles-leave-active {
  transition: all 500ms ease-in;
  position: absolute;
  z-index: 0;
}

/* appear at / disappear to */
.articles-enter,
.articles-leave-to {
  opacity: 0;
}

.menu-enter {
  max-height: 0;
  overflow: hidden;
}

.menu-enter-active {
  /* Set our transitions up. */
  overflow: hidden;
  -webkit-transition: max-height 0.4s ease;
  -moz-transition: max-height 0.4s ease;
  transition: max-height 0.4s ease;
}

.menu-enter-to {
  max-height: 1000px;
}

.menu-leave {
  max-height: 0;
  overflow: hidden;
}
</style>
