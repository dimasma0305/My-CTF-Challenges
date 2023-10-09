<script lang="ts">
    import { goto } from "$app/navigation";
    import { getnotes, decodeBearerToken } from "$lib/js/api";
    import { onMount } from "svelte";

    interface Note {
        ID: string;
        Title: string;
        Content: string;
    }

    var username = "";
    var data: Promise<Note[]> = getnotes().then(async (res) => {
        if (res.ok) {
            return res.json();
        } else {
            alert((await res.json())["error"]);
        }
    });
    onMount(() => {
        username = decodeBearerToken(localStorage.bearerToken)[0];
        if (!username) {
            goto("/login");
        }
    });
</script>

<section>
    <h2>Hi {username}!</h2>
    <p>
        Welcome to your Noteify! We are thrilled to provide you with a
        convenient platform where you can access and view all of your important
        notes in one place. Whether you need to jot down a quick reminder, keep
        track of important tasks, or simply record your thoughts, our
        note-taking feature is designed to make your life easier.
    </p>
    <a data-sveltekit-reload class="button" href="/note/addnote">Add Note</a>
    {#await data}
        <p>Loading...</p>
    {:then data}
        <ul>
            {#each data as val}
                <li><a href="/note/{val.ID}">{val.Title}</a></li>
            {/each}
        </ul>
    {/await}
</section>

<style>
    .button {
        background-color: #4caf50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        margin: 0 auto; /* Set left and right margin to auto */
        transition: background-color 0.3s ease;
        width: 100%;
        position: static;
    }
</style>
