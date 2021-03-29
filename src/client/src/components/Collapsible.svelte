<script lang="ts">
  export let open: boolean
  export let label: string
</script>

<div class="wrapper">
  <p
    class="collapsible"
    class:openCollapsible={open}
    on:click={() => {
      open = !open
    }}
  >
    {label}
  </p>
  <div class="content" class:showContent={open}>
    <slot />
  </div>
</div>

<style>
  .wrapper {
    margin-bottom: 15px;
  }
  .collapsible {
    font-weight: bold;
    border-bottom: 1px solid rgb(184, 184, 184);
    cursor: pointer;
    -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
    -khtml-user-select: none; /* Konqueror HTML */
    -moz-user-select: none; /* Old versions of Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */
    user-select: none;
    margin-bottom: 10px;
  }

  .collapsible::after {
    content: '\002B';
    float: right;
    margin-left: 5px;
  }

  .openCollapsible::after {
    content: '\2212';
  }

  .content {
    overflow: hidden;
    max-height: 0;
  }

  .showContent {
    max-height: 100%;
  }
</style>
