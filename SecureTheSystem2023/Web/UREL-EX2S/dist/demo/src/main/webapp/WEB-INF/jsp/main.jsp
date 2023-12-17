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
    <section class="text-gray-600 body-font">
      <div class="container flex flex-col items-center px-5 py-24 mx-auto md:flex-row">
        <div
          class="flex flex-col items-center mb-16 text-center lg:flex-grow md:w-1/2 lg:pr-24 md:pr-16 md:items-start md:text-left md:mb-0">
          <h1 class="mb-4 text-3xl font-medium text-gray-900 title-font sm:text-4xl">Embark on an Epic Adventure
            <br class="hidden lg:inline-block">in Guardian Tales
          </h1>
          <p class="mb-8 leading-relaxed">Join the world of Guardian Tales and experience a captivating storyline,
            exciting battles, and a vibrant community.</p>
          <div class="flex justify-center">
            <button
              class="inline-flex px-6 py-2 text-lg text-white bg-indigo-500 border-0 rounded focus:outline-none hover:bg-indigo-600">Play
              Now</button>
            <button
              class="inline-flex px-6 py-2 ml-4 text-lg text-gray-700 bg-gray-100 border-0 rounded focus:outline-none hover:bg-gray-200">Learn
              More</button>
          </div>
        </div>
        <div class="w-5/6 lg:max-w-lg lg:w-full md:w-1/2">
          <img class="object-cover object-center rounded" alt="hero"
            src="/2c8e04df5b0a67cadda0b78f4848ee28d901ee581028bcaea5c2adf861b7b145">
        </div>
      </div>
      <%@ include file="parts/footer.jsp" %>
    </section>


</body>

</html>
