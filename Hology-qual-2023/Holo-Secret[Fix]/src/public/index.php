<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Holo Curl</title>
    <!-- Include Bootstrap CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom CSS for background color -->
    <style>
        body {
            background-color: #00a4e4;
            /* Lighter blue */
        }

        .holo-gif {
            max-width: 100%;
        }

        .white-box {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
        }

        /* Added CSS for fixed size iframe */
        .fixed-size-iframe {
            width: 500px;
            /* You can adjust the width as needed */
            height: 300px;
            /* You can adjust the height as needed */
        }
    </style>
</head>

<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h1 class="text-center text-white">Holo Curl</h1>
                <form method="POST">
                    <div class="form-group">
                        <label for="urlInput" class="text-white">Enter URL:</label>
                        <input type="text" class="form-control" name="urlInput" id="urlInput" placeholder="https://example.com">
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">Submit</button>
                </form>
            </div>
        </div>
        <div class="row mt-5">
            <div class="col-md-12 text-center">
                <?php
                if (isset($_POST['urlInput']) && !empty($_POST['urlInput'])) {
                    $url = $_POST['urlInput'];
                    $url = str_replace(array("[", "]", "{", "}"), "", $url);
                    $content = shell_exec("curl " . escapeshellcmd($url));
                    if ($content !== false) {
                        echo '<iframe srcdoc="' . htmlspecialchars($content) . '" class="white-box fixed-size-iframe" frameborder="0"></iframe>';
                    } else {
                        echo '<img src="https://media.tenor.com/brIDwsDiqtQAAAAi/hololive.gif" alt="Hololive Agent" class="holo-gif">';
                    }
                } else {
                    echo '<img src="https://media.tenor.com/brIDwsDiqtQAAAAi/hololive.gif" alt="Hololive Agent" class="holo-gif">';
                }
                ?>
            </div>
        </div>
    </div>

    <!-- Include Bootstrap JS and jQuery -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>

</html>
