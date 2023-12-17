<%@ page language='java' contentType='text/html; charset=UTF-8' pageEncoding='UTF-8'%>
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>Guardian Tales</title>
    <script src='https://cdn.tailwindcss.com'></script>
</head>
<body class='container box-border flex flex-col items-center justify-center h-screen px-4 mx-auto text-center text-white bg-zinc-800'>
    <h1 class='inline-block text-left text-red-300 w-fit'>
        <span class='my-4 text-xl font-semibold'>HTTP ${pageContext.errorData.statusCode}</span><br>
        <span class='my-4 text-4xl font-bold'>
            ${pageContext.exception}
        </span><br>
        <a href='${pageContext.errorData.requestURI}' class='px-4 py-2 text-white bg-red-500 rounded-md'>Reload</a>
    </h1>
</body>
</html>
