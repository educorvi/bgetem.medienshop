<template>
  <div class="row" id="category-menu">
    <ul class="multi-column columns-3" v-if="type == 'normal'">
      <h2>{{ category.title }}</h2>
      <div class="row">
	<div class="col-sm-4" v-for="portion in chunkCat(category.values)">
	  <ul class="multi-column-dropdown dropdown-right">
	    <li class="catitem" v-for="cat in portion" v-bind:key="cat.id">
	      <a class="catitem"
		 v-if="!category.filter.includes(cat)"
		 v-on:click.prevent="filterCategory($event, cat)"
		 href="">{{ cat }}</a>
	    </li>
	  </ul>
	</div>
      </div>
    </ul>
    <ul class="multi-column columns-3" v-if="type == 'grouped'">
      <h2>{{ category.title }}</h2>
      <div class="row">
	<div class="col-sm-4"
	     v-for="portion in chunkCat(Object.keys(category.values))">
	  <ul class="multi-column-dropdown dropdown-right">
	    <li class="catitem" v-for="cat in portion">
	      <h3>
		<input type="checkbox"
		       v-model.lazy="category.top_categories"
                       v-bind:value="cat"
                       @change="toggleCategory($event, cat)"
		       />
		{{ cat }}
	      </h3>
	      <div class="subcategories">
		<div v-for="scat in category.values[cat]"
		     v-bind:key="scat" class="subcat">
		  <a v-on:click.prevent="filterCategory($event, scat)"
		     v-if="!category.filter.includes(scat)"
		     href="">{{ scat }}</a>
		  <a class="text-muted" v-else>{{ scat }}</a>
		</div>
	      </div>
	    </li>
	  </ul>
	</div>
      </div>
    </ul>
  </div>
</div>
</template>

<script>
Object.defineProperty(Array.prototype, "chunk", {
    value: function(chunkSize) {
	return this.reduce(function(previous, current) {
	    var chunk;
	    if (
		previous.length === 0 ||
		    previous[previous.length - 1].length === chunkSize
	    ) {
		chunk = [];
		previous.push(chunk);
	    } else {
		chunk = previous[previous.length - 1];
	    }
	    chunk.push(current);
	    return previous;
	}, []);
    }
});

Array.prototype.diff = function(a) {
    return this.filter(function(i) {return a.indexOf(i) < 0;});
};

export default {
    props: {
	category: {
	    type: Object
	},
	name: {
	    type: String
	},
	type: {
	    type: String
	},
    },
    methods: {
	chunkCat(values) {
	    return values.chunk(parseInt(values.length / 3));
	},
	filterCategory(event, cat) {
            this.$emit("fsearch", { name: this.name, category: cat });
	},
	toggleCategory(event, cat) {
	    let checked = event.target.checked;
            let cats = this.category.values[cat].slice()
            cats.push(cat)
	    if (checked) {
		for (var subcat of cats) {
		    this.$emit("fsearch", {
			name: this.name, category: subcat
		    });
		}
	    } else {
		for (var subcat of cats) {
		    if (this.category.filter.includes(subcat)) {
			let index = this.category.filter.indexOf(subcat);
			this.category.filter.splice(index, 1);
		    }
		}
	    }
	}
    }
};
</script>

<style scoped>
.subcategories {
    border-left: 1px solid #ddd;
    margin-left: 1em;
    padding-left: 1em;
}

#category-menu {
  margin: 4em 2em 1em 2em;
  border: 1px solid #ddd;
  background-color: #fafafa;
}

#content-core #category-menu ul li {
  text-indent: 0;
}

#content-core ul.multi-column {
  margin: 2em;
}

.dropdown-menu {
  min-width: 200px;
}

.dropdown-menu.columns-2 {
  min-width: 400px;
}

.dropdown-menu.columns-3 {
  min-width: 900px;
}

.dropdown-menu li a {
  padding: 5px 15px;
  font-weight: 300;
}

.multi-column-dropdown {
  list-style: none;
  margin: 0px;
  padding: 0px;
}

.multi-column-dropdown li a {
  display: inline-block;
  color: #333;
  width: 90%;
  padding: 0.2em 2em;
}

.multi-column-dropdown li a:hover {
  text-decoration: none;
  color: #262626;
  background-color: #ddd;
}

.multi-column-dropdown li a.text-muted:before {
    content: '✔ ';
}

.multi-column-dropdown a {
    padding-bottom: 5px;
    border-bottom: 1px solid #eee;
    margin-bottom: 5px;
    margin-right: 28px;
}

.multi-column-dropdown li h3 a {
    display: inline-block !important;
    margin: 0;
    width: 90%;
}

li.catitem {
  margin-left: 0px;
  margin-right: 0px;
}

@media (max-width: 767px) {
  .dropdown-menu.multi-column {
    min-width: 240px !important;
    overflow-x: hidden;
  }
}
</style>
