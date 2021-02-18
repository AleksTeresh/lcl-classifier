<script lang="ts">
	let activeConstraints = ""
	let passiveConstraints = ""

	let graphType: 'tree' | 'cycle' | 'path' = 'tree'
	let isDirected: boolean = false
	let isRooted: boolean = false
	let isRegular: boolean = false
</script>

<main>
	<form>
		<label>Active configurations:</label>
		<textarea bind:value={activeConstraints}></textarea>

		<label>Passive configurations:</label>
		<textarea bind:value={passiveConstraints}></textarea>

		<label>
			<input type=radio bind:group={graphType} value="tree">
			Tree
		</label>
		<label>
			<input type=radio bind:group={graphType} value="cycle">
			Cycle
		</label>
		<label>
			<input type=radio bind:group={graphType} value="path">
			Path
		</label>

		<label>
			<input type=checkbox bind:value={isDirected}>
			Directed
		</label>
		<label>
			<input type=checkbox bind:value={isRooted}>
			Rooted
		</label>
		<label>
			<input type=checkbox bind:value={isRegular}>
			Regular
		</label>

		{#if graphType === 'path'}
			<label>Leaf configurations (optional):</label>
			<textarea bind:value={activeConstraints}></textarea>

			<label>Root configurations (optional):</label>
			<textarea bind:value={passiveConstraints}></textarea>
		{/if}
	</form>
</main>
