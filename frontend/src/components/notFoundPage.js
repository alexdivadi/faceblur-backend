import React from "react";

function NotFoundPage() {
    return <section class="flex items-center w-screen p-16">
        <div class="container flex flex-col items-center ">
            <div class="flex flex-col gap-6 max-w-md text-center">
                <h2 class="font-extrabold text-9xl text-gray-600 dark:text-gray-100">
                    <span class="sr-only">Error</span>404
                </h2>
                <p class="text-2xl md:text-3xl dark:text-gray-300">Sorry, we couldn't find this page.</p>
                <a href="/" class="px-8 py-4 text-xl font-semibold rounded bg-amber-400 text-gray-50 hover:bg-amber-600">Back to home</a>
            </div>
        </div>
    </section>
}

export default NotFoundPage;