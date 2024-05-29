javascript:(function(){
    /* Smart Powermeter - CYCLE IMAGES FIRST */
    [
        "header",
        ".breadcrumbs",
        "#chat-widget-container",
        ".product-add-form",
        ".product-social-links",
        ".product-reviews-summary",
        "#tab-label-reviews",
        "#tab-label-customtab",
        ".fotorama__nav-wrap",
        "footer",

    ].forEach((s) => { try { document.querySelector(s).remove(); } catch (e) { console.log(e) } });
    document.querySelectorAll("*").forEach(function (e) { e.style.fontFamily = "unset"; });
    document.querySelector("div.product.info.detailed").style.setProperty('-webkit-box-shadow', "unset");
    
    for (x in jQuery.Fotorama.measures ) { if (jQuery.Fotorama.measures[x].width > 120) { 
        i = document.createElement('img');
        p = document.createElement('p');
        p.style.pageBreakInside = "avoid";
        p.appendChild(i); i.src = x; i.style.maxHeight = "180mm"; i.style.maxWidth = "180mm";
        document.querySelector("main").after(p);
    }};
})()