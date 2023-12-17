<!DOCTYPE html>
<html>

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/alpinejs" defer></script>
  <title>Guardian Tales</title>
</head>

<body>
  <%@ include file="parts/header.jsp" %>
    <div class="flex items-center justify-center w-full h-screen bg-white ">
      <form method="post" class="w-full rounded-lg md:w-1/3">
        <div class="flex justify-center mt-6 font-bold">
          <img class="w-40 mb-3" src="/img_char1.png" />
        </div>
        <h2 class="mb-8 text-2xl text-center text-gray-200">Login</h2>
        <div class="px-12 pb-10">
          <div class="w-full mb-2">
            <div class="flex items-center">
              <input name="email" type="text" placeholder="Email Address" class="w-full px-3 py-2 text-gray-700 border rounded focus:outline-none" />
            </div>
          </div>
          <div class="w-full mb-2">
            <div class="flex items-center">
              <input name="password" type="password" placeholder="Password" class="w-full px-3 py-2 text-gray-700 border rounded focus:outline-none" />
            </div>
          </div>
          <button type="submit" class="w-full py-2 mt-8 text-gray-100 bg-blue-400 rounded-full focus:outline-none">
            Login
          </button>
        </div>
      </form>
    </div>
    <%@ include file="parts/footer.jsp" %>

</body>

</html>
