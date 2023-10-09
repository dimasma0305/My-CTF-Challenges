<script lang="ts">
    import { goto } from "$app/navigation";
    import {register} from "$lib/js/api";
    var iusername: string, ipassword: string;
</script>

<svelte:head>
    <title>register | page</title>
</svelte:head>
<div class="container">
    <form class="login-form">
        <h2>Register</h2>
        <label for="username">Username:</label>
        <input
            type="text"
            id="username"
            name="username"
            bind:value={iusername}
        />
        <label for="password">Password:</label>
        <input
            type="password"
            id="password"
            name="password"
            bind:value={ipassword}
        />
        <button
            type="submit"
            on:click|preventDefault={async (e) => {
                let res = await register(iusername, ipassword)
                if (res.ok){
                    let auth = btoa(`${iusername}:${ipassword}`)
                    localStorage.setItem("bearerToken", auth)
                    goto("/note")
                } else {
                    alert((await res.json())['error'])
                }
            }}>Submit</button
        >
    </form>
</div>

<style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 72.5vh;
    }
    .login-form {
        max-width: 400px;
        margin: 0 auto;
        background-color: #f2f2f2;
        color: black;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    }

    .login-form h2 {
        text-align: center;
        margin-bottom: 20px;
        font-size: xx-large;
    }

    .login-form label {
        display: block;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .login-form input[type="text"],
    .login-form input[type="password"] {
        width: 100%;
        padding: 5px;
        border-radius: 5px;
        border: none;
        margin-bottom: 20px;
        box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
    }

    .login-form button[type="submit"] {
        background-color: #4caf50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        margin: 0 auto; /* Set left and right margin to auto */
        transition: background-color 0.3s ease;
        width: 100%;
    }

    .login-form button[type="submit"]:hover {
        background-color: #3e8e41;
    }
</style>
