document.addEventListener("DOMContentLoaded", function () {
    const msg = document.getElementById("email-btn");
    const cancel = document.getElementById("cancel");
    const ratingInput = document.getElementById("rating");
    const stars = $(".star_r");
    var rating = 0;
    const textArea = document.getElementById("testimonial-input");
    const wordCountSpan = document.getElementById("word-count");
    const reviewQuotes = $(".review-quote");
    const deleteStage = $(".delete-stage");
    const deletePush = $(".delete-push");
    const requestQuote = document.getElementById("quote");


    if (msg) {
        msg.addEventListener("click", function () {
            window.location.href = "mailto:bergamospencer@gmail.com";
        });
    }

    if (cancel) {
        cancel.addEventListener("click", function () {
            window.location.href = "/homepage";
        });
    }

    Array.from(stars).forEach(function (star) {
        star.addEventListener("mouseover", function (event) {
            if (event.target.classList.contains("fa-star")) {
                var currentRating = parseInt($(this).data('rating'));
                console.log("currentRating");
                highlightStars(currentRating);
            }
        });

        star.addEventListener("mouseleave", function (event) {
            console.log("mouseleave")
            highlightStars(rating);
        });

        star.addEventListener("click", function (event) {
            if (event.target.classList.contains("fa-star")) {
                rating = parseInt($(this).data('rating'));
                ratingInput.value = rating;
                console.log("rating");
            }
        });
        
    });

    if (textArea) {
        // console.log("textArea")
        const maxChar = 1000;
        textArea.addEventListener("input", () => {
            const inputText = textArea.value;
            const charCount = inputText.length;

            wordCountSpan.textContent = charCount;

            if (charCount > maxChar) {
                textArea.value = inputText.substring(0, maxChar);
                wordCountSpan.textContent = maxChar;
                wordCountSpan.style.color = "red";
            };
        })
    }

    if (reviewQuotes) {
        // const maxLength = 50;
        
        Array.from(reviewQuotes).forEach(function(quote) {
            // const maxLength = parseInt(quote.getAttribute('data-maxlength'));
            const maxLength = 150;
            let text = quote.textContent;
            if (text.length > maxLength) {
                text = text.substring(0, maxLength - 1) + "...";
                quote.textContent = text;
            }
            console.log(quote.textContent)
        });
    }


    if (deleteStage) {
        deleteStage.click(function () {
            var reviewId = $(this).data('review-id');
            $.ajax({
                type: "POST",
                url: '/delete-stage-id/' + reviewId,
                success: function () {
                    location.reload();
                },
                error: function() {
                    alert("failed to delete review");
                }
            })
        })
    }

    if (deletePush) {
        deletePush.click(function () {
            var reviewId = $(this).data('review-id');
            $.ajax({
                type: "POST",
                url: '/delete-push-id/' + reviewId,
                success: function () {
                    location.reload();
                },
                error: function() {
                    alert("failed to delete review");
                }
            })
        })
    }

    if (requestQuote) {
        requestQuote.addEventListener("click", function () {
            window.location.href = "/quote-form";
        });
    }

    function highlightStars(count) {
        Array.from(stars).forEach(function (star) {
            var starRating = parseInt(star.getAttribute('data-rating'));
            star.style.color = starRating <= count ? "gold" : "black";

        })
    }
});