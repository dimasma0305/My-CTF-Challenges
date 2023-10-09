<script lang="ts">
	import { goto } from "$app/navigation";
	import { browser } from "$app/environment";
	import { onMount } from "svelte";
	import { decodeBearerToken } from "$lib/js/api";

	let username: string | null;

	onMount(() => {
		const updateUsername = () => {
			if (browser) {
				let token = localStorage.bearerToken;
				if (token) {
					username = decodeBearerToken(localStorage.bearerToken)[0];
				}
			}
		};
		history.pushState = updateUsername;
		updateUsername();
	});
</script>

<header class="header">
	<nav class="navbar">
		<div class="navbar-brand">
			<a href="/">Noteify</a>
		</div>
		<div data-sveltekit-replacestate class="navbar-menu">
			<ul>
				{#if username != null}
					<li>
						<span class="green-dot" />
						{username}
					</li>
				{/if}
				<li><a href="/">Home</a></li>
				<li><a href="/about">About</a></li>
				{#if username != null}
					<li><a href="/note">Note</a></li>
					<li>
						<a
							href="/"
							on:click={async () => {
								localStorage.clear();
								location.replace("/")
							}}>Logout</a
						>
					</li>
				{:else}
					<li>
						<a data-sveltekit-replacestate href="/login">Login</a>
					</li>
					<li>
						<a data-sveltekit-replacestate href="/register"
							>Register</a
						>
					</li>
				{/if}
			</ul>
		</div>
	</nav>
</header>

<style>
	.green-dot {
		display: inline-block;
		width: 10px;
		height: 10px;
		top: 50%;
		border-radius: 50%;
		margin-right: 0px;
		background-color: green;
		animation: color-change 1s infinite alternate;
	}

	@keyframes color-change {
		from {
			background-color: green;
		}
		to {
			background-color: yellow;
		}
	}
	.header {
		background-color: #333;
		color: #fff;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
		position: sticky;
		top: 0;
		left: 0;
		right: 0;
		z-index: 999;
	}

	.navbar {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 6px;
	}

	.navbar-brand a {
		font-size: 24px;
		font-weight: bold;
		color: #fff;
		text-decoration: none;
	}

	.navbar-menu {
		color: #fff;
		text-decoration: none;
		font-size: 16px;
	}

	.navbar-menu ul {
		display: flex;
		justify-content: flex-end;
		list-style: none;
		margin: 0;
		padding: 0;
	}

	.navbar-menu ul li {
		margin: 0 10px;
	}

	.navbar-menu ul li a {
		color: #ffffff;
		text-decoration: none;
		font-size: 16px;
	}

	@media screen and (min-width: 768px) {
		.navbar-menu {
			display: block;
		}
	}
</style>
