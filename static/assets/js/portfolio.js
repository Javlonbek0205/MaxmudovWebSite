$(document).ready(function () {
    // Filter Click
    $(".button").click(function () {
        $(this).addClass("active").siblings().removeClass("active");

        var filter = $(this).attr("data-filter");

        if (filter === "all") {
            $(".portfolio-item").show(400);
        } else {
            $(".portfolio-item").not("." + filter).hide(200);
            $(".portfolio-item").filter("." + filter).show(400);
        }
    });

    // Magnific Popup for Portfolio Gallery
    $(".view-btn").on("click", function (e) {
        e.preventDefault();

        // Get the portfolio ID
        var portfolioId = $(this).data("portfolio-id");

        // Find gallery images for the portfolio
        var $gallery = $("#gallery-" + portfolioId + " a");

        // Open Magnific Popup with the selected images
        $.magnificPopup.open({
            items: $gallery.map(function () {
                return { src: $(this).attr("href"), title: $(this).attr("title") };
            }).get(),
            type: "image",
            gallery: {
                enabled: true,
            },
            removalDelay: 500,
            callbacks: {
                beforeOpen: function () {
                    this.st.image.markup = this.st.image.markup.replace(
                        "mfp-figure",
                        "mfp-figure mfp-with-anim"
                    );
                    this.st.mainClass = "mfp-zoom-in";
                },
            },
            closeOnContentClick: true,
            midClick: true,
        });
    });
});
