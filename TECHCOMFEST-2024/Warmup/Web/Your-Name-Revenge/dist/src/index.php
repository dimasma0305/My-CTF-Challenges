<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Name</title>
</head>

<body>
    <form action="/">
        <input type="text" name="name">
        <button type="submit">Submit</button>
    </form>
    <h1></h1>
</body>

<script>
    <?php
    if (isset($_GET['name'])) {
    ?>
        const name = "<?= str_replace('\\', '', htmlentities($_GET['name'])) ?>"
    <?php
    }
    ?>
    if (name) {
        document.querySelector("h1").innerHTML = name
    }
</script>

</html>
