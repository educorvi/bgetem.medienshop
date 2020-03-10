<template>
  <div>
    <!--<div v-if="dirty">The cart has been modified, please save</div>-->
    <table class="mp-desktop-table table table-bordered table-striped">
      <thead>
        <tr>
          <th class="checkbox-cart"></th>
          <th>Artikel</th>
          <th>Menge</th>
          <th v-if="user == 'mitglied' || user == 'anon'">Preis für Mitglieder</th>
          <th v-if="user != 'mitglied'" class="col-sm-2">Preis für Nicht-Mitglieder</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(value, key) in data" v-bind:key="key">
          <td class="checkbox-cart">
            <input type="checkbox" v-model="marked" :id="key" :value="key" />
          </td>
          <td>
            <div class="media">
              <a class="col-xs-12" :href="value.uri" target="_blank">
                <div class="artikel-bild col-sm-3">
                  <img class="media-object col-sm-12 img-responsive" :src="value.image" />
                </div>
                <div class="col-sm-9 col-xs-12">
                  <p class="mp-product-name">
                      {{value.artikel}}
                  </p>
                  <p>
                    {{value.bestellung}}
                    </p>
                </div>
              </a>
            </div>
          </td>
          <td class="counter col-sm-3 col-md-2">
            <div class="input-group">
              <span class="input-group-btn">
                <button type="button" id="down" @click="minus(value)" class="btn btn-number">
                  <span class="glyphicon glyphicon-minus"></span>
                </button>
              </span>
              <input type=text maxlength="2" @keyup="validate(value, $event.target.value)" name="quantity" v-bind:value="value.menge" />
              <span class="input-group-btn">
                <button type="button" class="btn btn-number" @click="plus(value)">
                  <span class="glyphicon glyphicon-plus"></span>
                </button>
              </span>
            </div>
          </td>
          <td v-if="user == 'mitglied' || user == 'anon'" class="text-right">{{value.preis_mem | currency}}</td>
          <td v-if="user != 'mitglied'" class="text-right">{{value.preis | currency}}</td>
        </tr>
        <tr>
          <td class="checkbox-warenkorb">
          </td>
          <td>
            <a class="btn mp-btn-default" href="#" role="button" v-on:click.prevent="delete_marked">Löschen</a> &nbsp;
            <a v-if="dirty" class="btn mp-btn-default" href="#" role="button" v-on:click.prevent="revert">Rückgängig</a>
          </td>
          <td>
            <b>Summe:</b>
          </td>
          <td v-if="user == 'mitglied' || user == 'anon'" class="text-right">
            <b>{{summe_preis_mem | currency}}</b>
          </td>
          <td v-if="user != 'mitglied'" class="text-right">
            <b>{{summe_preis | currency}}</b>
          </td>
        </tr>
      </tbody>
    </table>

    <table class="mp-mobile-table table table-bordered table-striped">
      <thead>
        <tr>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(value, key) in data" v-bind:key="key">
          <td><input type="checkbox" v-model="marked" :id="key" :value="key">Diesen Artikel auswählen.
            <div class="mp-new-section media col-lg-9">
              <a class="col-xs-12" :href="value.uri" target="_blank">
                <div class="artikel-bild col-xs-2 col-sm-3">
                  <img class="media-object img-responsive" :src="value.image"></div>
                <div class="col-sm-9 col-xs-10">
                  <p class="mp-product-name">
                    {{value.artikel}}
                  </p>
                  <p class="discret">{{value.bestellung}}</p>
                </div>
              </a>
              <div class="mp-new-section col-xs-12">
                <div class="counter col-xs-6">
                  <div class="input-group">
                    <span class="input-group-btn">
                      <button type="button" id="down" @click="minus(value)" class="btn btn-number">
                        <span class="glyphicon glyphicon-minus"></span>
                      </button>
                    </span>
                    <input class="form-control input-number" type=text maxlength="2" @keyup="validate(value, $event.target.value)" name="quantity" v-bind:value="value.menge" />
                    <span class="input-group-btn">

                      <button type="button" class="btn btn-number" @click="plus(value)">
                        <span class="glyphicon glyphicon-plus"></span>
                      </button>
                    </span>
                  </div>
                </div>
                <div class="price col-xs-6">
                  <p v-if="user == 'mitglied' || user == 'anon'">{{value.preis_mem | currency}} <em>Preis für versicherte Unternehmen</em></p>
                  <p v-if="user != 'mitglied'" class="text-right">{{value.preis | currency}} <em>Preis für Nichtversicherte Unternehmen</em></p>
                </div>
              </div>
            </div>
          </td>
        </tr>
        <tr>

          <td>
            <div v-if="user != 'mitglied'" class="media col-lg-9">
              <p class="total-price col-xs-4">
                <b> Summe </b>
              </p>
              <p class="price text-right col-xs-4"><span v-if="user == 'mitglied' || user == 'anon'"> Mitglied: {{summe_preis_mem | currency}}</span></p>
              <p class="price text-right col-xs-4"><span v-if="user != 'mitglied'">Nicht Mitglied: {{summe_preis | currency}}</span></p>
            </div>
          </td>
        </tr>
        <tr>
          <td>
            <a class="btn mp-btn-default" href="#" role="button" v-on:click.prevent="delete_marked">Löschen</a> &nbsp;
            <a v-if="dirty" class="btn mp-btn-default" href="#" role="button" v-on:click.prevent="revert">Rückgängig</a>
          </td>
        </tr>
      </tbody>
    </table>

    <div>
      <a style="margin-top: 10px; margin-left:8px" class="btn btn-primary" href="#" role="button" v-on:click.prevent="submit(shop_url + '/loginform')">Mit der Bestellung fortfahren</a>
      <a style="margin-top: 10px; margin-left:8px" class="btn btn-default" href="#" role="button" v-on:click.prevent="submit(shop_url)">Weitere Artikel auswählen</a>
    </div>
  </div>
</template>

<script>
import "babel-polyfill";
import axios from "axios";
import "babel-polyfill";

function calc_preis(menge, preis, freimenge) {
  if (menge <= freimenge) {
    return 0;
  }
  return (menge - freimenge) * preis;
}

export default {
  computed: {
    summe_preis_mem() {
      var sum = 0;
      for (let [key, value] of Object.entries(this.data)) {
        sum += calc_preis(
          Number(value.menge),
          Number(value.preis_mem),
          Number(value.freimenge)
        );
      }
      return sum;
    },
    summe_preis() {
      var sum = 0;
      for (let [key, value] of Object.entries(this.data)) {
        sum += Number(value.menge) * Number(value.preis);
      }
      return sum;
    }
  },
  mounted() {
    console.log("My CART", this.cart);
  },
  props: ["cart", "shop_url", "user"],
  watch: {
    data: {
      handler: function(val, oldVal) {
        console.log("TRY TO UPDATE");
        this.persist();
        console.log("UPDATED");
      },
      deep: true
    }
  },
  methods: {
    validate(value, menge) {
      console.log(value.artbestand);
      console.log(menge)
      if (isNaN(menge) == true) {
        alert("Bitte nur Zahlen eingeben");
        return;
      } else if (value.artbestand < menge) {
        alert(
          "Momentan können nicht mehr von diesen Artikeln bestellt werden."
        );
        if (value.artbestand > 99) {
          value.menge = 99;
        } else {
          //value.menge = value.artbestand;
          console.log('WHY THE HELL')
        }
      } else if (menge > 99) {
        alert("Es können nicht mehr als 99 Artikel bestellt werden.");
      } else {
        value.menge = menge;
      }
    },
    minus(value) {
      if (value.menge > 0) {
        value.menge -= 1;
      }
    },
    plus(value) {
      value.menge = Number(value.menge);
      if (value.menge >= 99) {
        alert(
          "Momentan können nicht mehr von diesen Artikeln bestellt werden."
        );
        return;
      }
      if (value.artbestand > value.menge) {
        value.menge += 1;
      } else {
        alert(
          "Momentan können nicht mehr von diesen Artikeln bestellt werden."
        );
      }
    },
    persist() {
      let bodyFormData = new FormData();
      console.log('bodyFormData')
      bodyFormData.append("cart", JSON.stringify(this.data));
      console.log(this.shop_url);
      axios
        .post(this.shop_url + "/updatecart", bodyFormData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          this.dirty = false;
          return true;
        })
        .catch(error => {
          console.log(error);
          return false;
        });
    },
    submit(nextURL) {
      console.log("SUBMIT");
      //this.persist();
      console.log("SUBMIT");
      window.location.assign(this.shop_url + nextURL);
    },
    delete_marked() {
      if (this.marked.length) {
        for (let key of this.marked) {
          if (this.data.hasOwnProperty(key)) {
            this.$delete(this.data, key);
          }
        }
        this.marked = [];
        this.persist();
      }
    }
  },
  data() {
    return {
      original: JSON.parse(this.cart),
      data: JSON.parse(this.cart),
      dirty: false,
      marked: []
    };
  }
};
</script>

<style scoped>
</style>
