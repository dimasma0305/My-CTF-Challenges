<script lang="ts">
    import { addnote } from "$lib/js/api";
    import DOMPurify from "dompurify";
    import { marked } from "marked";
    let title = "";
    let content = "";
    let html = "";

    const handleContentChange = (event: Event) => {
        //@ts-ignore
        content = event.target.value;
        //@ts-ignore
        html = DOMPurify.sanitize(marked.parse(content));
    };
</script>

<svelte:head>
    <title>{title}</title>
</svelte:head>

<div class="form-container">
    <div class="form-column">
        <div class="form-group">
            <label for="title-input">Title</label>
            <input id="title-input" type="text" bind:value={title} />
        </div>
        <div class="form-group">
            <label for="content-input">Content</label>
            <textarea
                id="content-input"
                bind:value={content}
                on:input={handleContentChange}
            />
        </div>
        <button
            on:click={async () => {
                addnote(title, content).then(async (res) => {
                    if (res.ok) {
                        location.assign("/note");
                    } else {
                        alert((await res.json())["error"]);
                    }
                });
            }}>Save</button
        >
    </div>
    <div class="form-column">
        <div class="form-group">
            <label for="html-output">HTML Output</label>
            <div
                id="html-output"
                class="html-output"
                contenteditable
                bind:innerHTML={html}
            />
        </div>
    </div>
</div>

<style>
    button {
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
    .form-container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        gap: 2rem;
    }
    textarea {
        height: 40vh;
        resize: none;
    }

    .form-column {
        width: 50%;
    }

    .form-group {
        display: flex;
        flex-direction: column;
        margin-bottom: 1rem;
    }

    label {
        margin-bottom: 0.5rem;
    }

    input,
    textarea {
        border: 1px solid #ccc;
        padding: 0.5rem;
    }

    textarea {
        min-height: 10rem;
    }

    .html-output {
        border: 1px solid #ccc;
        padding: 0.5rem;
        height: 63vh;
    }
</style>
