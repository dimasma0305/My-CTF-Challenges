<?php
// Array to map file extensions to MIME types
$mime_types = [
    'html' => 'text/html',
    'txt'  => 'text/plain',
    'jpg'  => 'image/jpeg',
    'jpeg' => 'image/jpeg',
    'png'  => 'image/png',
    'gif'  => 'image/gif',
    'css'  => 'text/css',
    'js'   => 'application/javascript',
    'json' => 'application/json',
    'pdf'  => 'application/pdf',
    // Add more file types as needed
];

// looks like cyber strike web vuln but better
if (isset($_GET['file'])) {
    $file = $_GET['file']; // Sanitize file input (basic)
    $file_path = "uploads/" . $file; // Directory where files are stored

    // Get the file extension
    $ext = strtolower(pathinfo($file, PATHINFO_EXTENSION));

    // Check if file exists and the extension is in the MIME type array
    if (file_exists($file_path) || isset($mime_types[$ext])) {
        // Set the appropriate Content-Type header based on the file extension
        $ext = isset($mime_types[$ext]) ? $mime_types[$ext] : 'application/octet-stream';
        header('Content-Type: ' . $ext);

        // Output the file contents
        echo file_get_contents($file_path);
    } else {
        // Return a 404 response if the file doesn't exist or type is not allowed
        header('HTTP/1.0 404 Not Found');
        echo "File not found or unsupported file type.";
    }
} else {
    echo "No file specified.";
}
?>
