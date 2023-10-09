<script lang="ts">
    import { page } from "$app/stores";
    import { getnote } from "$lib/js/api";
    import { onMount } from "svelte";
    import DOMPurify from "dompurify";
    import { marked } from "marked";
    let title = "";
    let content = "";

    onMount(async () => {
        if (
            localStorage.getItem($page.params.id + "-content") &&
            localStorage.getItem($page.params.id + "-title")
        ) {
            title = localStorage[$page.params.id + "-title"];
            content = localStorage[$page.params.id + "-content"];
        } else {
            //@ts-ignore
            await getnote($page.params.id).then(async (res) => {
                if (res.ok) {
                    let tmp = await res.json();
                    //@ts-ignore
                    content = DOMPurify.sanitize(marked.parse(tmp.Content));
                    title = tmp.Title;
                    localStorage.setItem($page.params.id + "-title", title);
                    localStorage.setItem(
                        $page.params.id + "-content",
                        content
                    );
                    return tmp;
                } else {
                    alert((await res.json())["error"]);
                }
            });
        }
        //@ts-ignore
        content = config["default-content"] || content;
    });
</script>

<svelte:head>
    <title>{title}</title>
</svelte:head>

<section>
    <h1>{title}</h1>
    <div>{@html content}</div>
    <a class="button" href="/note">back</a>
</section>

<style>
    section {
        width: 100%;
    }
    .button {
        background-color: #4caf50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        margin: 0 auto;
        text-align: center;
        transition: background-color 0.3s ease;
        width: 100%;
        left: 0;
    }
</style>
