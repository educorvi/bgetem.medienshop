<template>
    <div class="row">
        <hr class="media-default">
        <div class="media col-lg-9">
            <a class="col-xs-12" v-bind:href="article.artikel">
                <div class="article-image col-sm-3 col-xs-6">
                    <img class="media-object img-responsive" v-bind:src="article.titelbild">
                </div>
                <div class="col-sm-9 col-xs-12">
                    <h3 class="newsDescription">{{article.title}}</h3>
                    <p class="tileBody">
                        <span class="bgetem_folder_description">{{article.desc}}</span>
                    </p>
                </div>
            </a>
        </div>
        <div class="mp-price-table col-lg-3">
            <div class="list-group">
                <p v-if="article.downloads == false" class="list-group-item disabled" v-html="article.textversicherte"> </p>
                <p v-if="article.downloads == true" class="list-group-item disabled"> Diesen Artikel können Sie nicht bestellen, sondern nur herunterladen. </p>
                <div class="list-group-item">
                    <p v-if="article.downloads == false && user == 'anon'" class="mp-order-info" v-html="article.textbesteller"></p>
                    <div class="mp-wrapper">
                        <div class="row mp-new-section">
                            <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
                                <div class="panel panel-accordion">
                                    <div class="panel-heading-inverse" role="tab" id="heading1">
                                        <a name="section-1" id="section-1"></a>
                                        <h4 class="panel-title-inverse">
                                            <a role="button" data-parent="#accordion" v-bind:href="article.artikel" aria-expanded="false" aria-controls="collapse1" class="collapsed">Details</a>
                                        </h4>
                                    </div>
                                    <div id="collapse1" class="panel-collapse collapse" role="tabpanel" aria-labelledby="heading1" aria-expanded="false">
                                    </div>
                                </div>
                            </div>
                            <div v-if="article.downloads == false && article.bestand == true" class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
                                <div class="panel panel-accordion">
                                    <div class="panel-heading-inverse" role="tab" id="heading1">
                                        <a name="section-1" id="section-1"></a>
                                        <h4 class="panel-title-inverse">
                                            <a role="button" data-parent="#accordion" v-bind:href="article.warenkorb" aria-expanded="false" aria-controls="collapse1" class="collapsed">Jetzt bestellen</a>
                                        </h4>
                                    </div>
                                    <div id="collapse1" class="panel-collapse collapse" role="tabpanel" aria-labelledby="heading1" aria-expanded="false">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <p v-if="article.downloads != true && article.bestand != true">
                        <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                        <em>nicht lieferbar</em>
                    </p>
                    <p v-if="article.downloads != true && article.bestand != true && article.files_available == true">
                        <span class="glyphicon glyphicon-save" aria-hidden="true"></span>
                        <em>Bitte für Download auf "Details" klicken</em>
                    </p>
                    <p v-if="article.downloads != true && article.bestand == true && article.artbestand > 99">
                        <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                        <em>sofort lieferbar</em>
                    </p>
                    <p v-if="article.downloads != true && article.bestand == true && article.artbestand <= 99">
                        <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                        <em> {{article.artbestand}} Stück lieferbar</em>
                    </p>
                    <p v-if="article.downloads == true">
                        <span class="glyphicon glyphicon-save" aria-hidden="true"></span>
                        <em>Bitte für Download auf "Details" klicken</em>
                    </p>

                </div>
            </div>
        </div>
        <div class="row mp-list-devider">
            <hr class="media-default">
            <p class="col-lg-3">
                <em>
                    <strong>Medienart:</strong>
                </em> {{article.medienart}}</p>
            <p class="col-lg-3">
                <em>
                    <strong>Bestellnummer:</strong>
                </em> {{article.artnr}}</p>
        </div>

    </div>
</template>

<script>
import ShopListing from "./ShopListing.vue";
export default {
  props: {
    article: {
      type: Object
    },
    user: {
      type: String
    }
  },
  components: { ShopListing }
};
</script>

<style scoped>
</style>
