<template>
    <div class="col-lg-12">
        <div class="input-group">
            <input v-on:keyup.enter="searchResults" v-model="filter.text" type="text" class="form-control mp-search-input" placeholder="Geben Sie einen Suchbegriff ein...">
            <span class="input-group-btn">
                <button class="btn btn-default mp-search" v-on:click.prevent="searchResults" type="button">
                    <span class="glyphicon glyphicon-search"></span>
                </button>
            </span>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                filter: {
                    text: ''
                }
            }
        },
       methods: {
           searchResults() {
               console.log(this)
               this.$emit('filtersearch', this.filter.text)
           }
       }, 
    }
</script>

<style scoped>

</style>
