import Vue from 'vue/dist/vue.esm'
import ShopListing from './components/ShopListing.vue'
import ShopCart from './components/ShopCart.vue'
//import vueCustomElement from 'vue-custom-element'
import 'document-register-element/build/document-register-element';
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueCurrencyFilter from 'vue-currency-filter'

Vue.use(VueCurrencyFilter,
    {
      symbol : '€',
      thousandsSeparator: '.',
      fractionCount: 2,
      fractionSeparator: ',',
      symbolPosition: 'back',
      symbolSpacing: true
    })


Vue.use(VueAxios, axios)
Vue.config.productionTip = true

/*
Vue.config.ignoredElements = [
    'shop-listing',
    'shop-cart'
];
*/

//Vue.customElement('shop-listing', ShopListing);
//Vue.customElement('shop-cart', ShopCart);


new Vue({
    el: "#main",
    components: {ShopListing, ShopCart}
})