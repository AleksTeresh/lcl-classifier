<script lang="ts">
	import { getProblem } from './api'
import type { Problem } from './types';

	let activeConstraints = ""
	let passiveConstraints = ""
	let leafConstraints = undefined
	let rootConstraints = undefined

	let graphType: 'tree' | 'cycle' | 'path' = 'tree'
	let isDirected: boolean = false
	let isRooted: boolean = false
	let isRegular: boolean = false

	async function handleProblemSubmit(e: any) {
		e.preventDefault();

		const problem: Problem = {
			activeConstraints: activeConstraints.split('\n'),
			passiveConstraints: passiveConstraints.split('\n'),
			leafConstraints: leafConstraints?.split('\n'),
			rootConstraints: rootConstraints?.split('\n'),
			isTree: graphType === 'tree',
			isCycle: graphType === 'cycle',
			isPath: graphType === 'path',
			isDirected,
			isRooted,
			isRegular
		}

		const response = await getProblem(problem)
		console.log(response)
	}
</script>

<main>
	<form>
		<label for="activeConfigs">Active configurations:</label>
		<textarea id="activeConfigs" bind:value={activeConstraints}></textarea>

		<label for="activeConfigs">Passive configurations:</label>
		<textarea id="passiveConfigs" bind:value={passiveConstraints}></textarea>

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
			<input type=checkbox bind:checked={isDirected}>
			Directed
		</label>
		<label>
			<input type=checkbox bind:checked={isRooted}>
			Rooted
		</label>
		<label>
			<input type=checkbox bind:checked={isRegular}>
			Regular
		</label>

		{#if graphType === 'path'}
			<label for="leafConfig">Leaf configurations (optional):</label>
			<textarea id="leafConfig" bind:value={leafConstraints}></textarea>

			<label for="rootConfig">Root configurations (optional):</label>
			<textarea id="rootConfig" bind:value={rootConstraints}></textarea>
		{/if}

		<button
			on:click={handleProblemSubmit}>
			Find
		</button>
	</form>
</main>
