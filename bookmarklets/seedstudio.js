javascript:(function(){
    [
        ".header-container",
        ".me-product-info-col",
        ".footer-static-container",
        ".pager",
        "#uservoice-btn",
        "#page-back-top",
        "#thumbnail-slider",
        "footer"

    ].forEach((s) => { try { document.querySelector(s).remove(); } catch (e) { console.log(e) } });
    [
        "//span[normalize-space(text())='SHARED BY USERS']/ancestor::h3/parent::div",
        "//span[normalize-space(text())='REVIEWS']/ancestor::h3/parent::div",
    ].forEach((s) => {
        try { document.evaluate(s, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.remove() } catch (e) { console.log(e) }
    });
    document.querySelector(".page-wrapper").style.setProperty('--header-h', 0);
    document.querySelectorAll("ul#main-slider-list img").forEach((e) => {
        if (e.src.startsWith("http")) { src = e.src; } else { src = e.getAttribute("data-splide-lazy"); }
        i = document.createElement('img');
        p = document.createElement('p');
        p.style.pageBreakInside = "avoid";
        p.appendChild(i); i.src = src; i.style.maxHeight = "180mm"; i.style.maxWidth = "180mm";
        document.querySelector(".product-view").after(p);

    });

    setTimeout(function () { 
        prompt("Save%20PDF%20as", document.location.href.replace("https://www.tindie.com/products/", "").replace(/([^/]*)\/([^/]*).*/, function (m, p1, p2) { return p1 + "_" + p2 + ".pdf"; })); window.print(); }, 2000);

})()