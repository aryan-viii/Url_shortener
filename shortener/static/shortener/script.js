// --------------------------------------------------
// Get HTML elements
// --------------------------------------------------

const csrfToken = document.querySelector(
    "[name=csrfmiddlewaretoken]"
).value;
const form = document.getElementById("shorten-form");

const qrCode = document.getElementById("qr-code");
const qrButton = document.getElementById("qr-button");

const urlInput = document.getElementById("url");
const shortCodeInput = document.getElementById("short-code");
const expiresAtInput = document.getElementById("expires-at");

const result = document.getElementById("result");
const shortUrlElement = document.getElementById("short-url");
const copyButton = document.getElementById("copy-button");

const errorMessage = document.getElementById("error-message");


// --------------------------------------------------
// Handle form submission
// --------------------------------------------------

form.addEventListener("submit", async function (event) {

    // Prevent normal HTML form submission
    event.preventDefault();


    // Hide old results/errors
    result.hidden = true;
    errorMessage.hidden = true;

    errorMessage.textContent = "";


    // --------------------------------------------------
    // Get form values
    // --------------------------------------------------

    const url = urlInput.value.trim();
    const shortCode = shortCodeInput.value.trim();
    const expiresAt = expiresAtInput.value;


    // --------------------------------------------------
    // Build request data
    // --------------------------------------------------

    const data = {
        url: url
    };


    // Only send short_code if user entered one
    if (shortCode) {
        data.short_code = shortCode;
    }


    // Only send expires_at if user selected one
    if (expiresAt) {
        data.expires_at = expiresAt;
    }


    // --------------------------------------------------
    // Send request to API
    // --------------------------------------------------

    try {

        const response = await fetch("/api/shorten/", {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },

            body: JSON.stringify(data)
        });


        // Convert API response into JavaScript object
        const responseData = await response.json();


        // --------------------------------------------------
        // Handle API errors
        // --------------------------------------------------

        if (!response.ok) {

            const messages = [];


            // DRF usually returns errors like:
            //
            // {
            //     "short_code": [
            //         "This short code is already taken."
            //     ]
            // }

            for (const field in responseData) {

                const errors = responseData[field];

                if (Array.isArray(errors)) {

                    errors.forEach(function (error) {
                        messages.push(`${field}: ${error}`);
                    });

                } else {

                    messages.push(`${field}: ${errors}`);

                }
            }


            errorMessage.textContent = messages.join(" ");

            errorMessage.hidden = false;

            return;
        }


        // --------------------------------------------------
        // Build the public short URL
        // --------------------------------------------------

        const shortUrl =
            `${window.location.origin}/${responseData.short_code}/`;


        // --------------------------------------------------
        // Display result
        // --------------------------------------------------

        shortUrlElement.textContent = shortUrl;
        shortUrlElement.href = shortUrl;


        // Build QR endpoint URL
        const qrUrl =
            `/api/shorten/${responseData.short_code}/qr/`;


        // Display QR image
        qrCode.src = qrUrl;


        // Open full QR image
        qrButton.href = qrUrl;


        // Show result
        result.hidden = false;


        // --------------------------------------------------
        // Reset form
        // --------------------------------------------------

        form.reset();

    }

    catch (error) {

        console.error(error);

        errorMessage.textContent =
            "Something went wrong. Please try again.";

        errorMessage.hidden = false;

    }

});


// --------------------------------------------------
// Copy shortened URL
// --------------------------------------------------

copyButton.addEventListener("click", async function () {

    const shortUrl = shortUrlElement.href;


    try {

        await navigator.clipboard.writeText(shortUrl);


        // Give user feedback
        copyButton.textContent = "Copied!";


        // Change button back after 2 seconds
        setTimeout(function () {

            copyButton.textContent = "Copy";

        }, 2000);

    }

    catch (error) {

        console.error(error);

        errorMessage.textContent =
            "Unable to copy the URL.";

        errorMessage.hidden = false;

    }

});