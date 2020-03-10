<template>
  <div class="col-md-3" :class="{ 'active-category': active }">
    <button @click="activate_category($event, category.id)"
	    type="button" class="btn mp-btn-default mp-drop">
      {{category.title}}
    </button>
    <button @click="activate_category($event, category.id)"
	    type="button" class="btn mp-btn-default dropdown-toggle"
	    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
      <span class="caret"></span>
      <span class="sr-only">Toggle Dropdown</span>
    </button>
  </div>
</template>

<script>
export default {
    props: ["active", "category"],
    methods: {
	activate_category(event, cat) {
	    this.$emit("show_menu", {
		name: cat,
	    });
	}
    }
};
</script>

<style scoped>
  .active-category button.mp-btn-default {
    border: 1px solid #51ae31;
    color: #fff;
    background-color: #51ae31;
  }
</style>
