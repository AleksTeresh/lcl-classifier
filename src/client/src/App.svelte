<script lang="ts">
  import ProblemForm from "./ProblemForm.svelte"
  import QueryForm from "./QueryForm.svelte"
</script>

<main>
  <div class="container">
    <ProblemForm />
    <QueryForm />
  </div>
</main>

<style>
  .container {
    display: flex;
    justify-content: space-between;
  }
</style>
