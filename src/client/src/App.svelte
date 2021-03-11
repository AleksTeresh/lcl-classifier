<script lang="ts">
  import ProblemForm from "./ProblemForm.svelte"
  import QueryForm from "./QueryForm.svelte"
</script>

<main>
  <div class="container">
    <div class="problem-form">
      <ProblemForm />
    </div>
    <div class="query-form">
      <QueryForm />
    </div>
  </div>
</main>

<style>
  .container {
    display: flex;
    justify-content: space-between;
  }

  .problem-form {
    flex-basis: 35%;
  }

  .query-form {
    flex-basis: 65%;
  }
</style>
