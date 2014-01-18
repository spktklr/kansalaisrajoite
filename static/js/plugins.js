// Avoid `console` errors in browsers that lack a console.
(function () {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

// Place any jQuery/helper plugins in here.

// Tooltipster by Caleb Jacob and Louis Ameline
(function(d,f,g,b){var e="tooltipster",c={animation:"fade",arrow:true,arrowColor:"",content:"",delay:200,fixedWidth:0,maxWidth:210,functionBefore:function(l,m){m()},functionReady:function(l,m){},functionAfter:function(l){},icon:"(?)",iconDesktop:false,iconTouch:false,iconTheme:".tooltipster-icon",interactive:false,interactiveTolerance:350,offsetX:0,offsetY:0,onlyOne:true,position:"bottom",speed:350,timer:0,theme:".tooltipster-default",touchDevices:true,trigger:"hover",updateAnimation:true};function h(m,l){this.element=m;this.options=d.extend({},c,l);this._defaults=c;this._name=e;this.init()}function j(){return !!("ontouchstart" in f)}function a(){var l=g.body||g.documentElement;var n=l.style;var o="transition";if(typeof n[o]=="string"){return true}v=["Moz","Webkit","Khtml","O","ms"],o=o.charAt(0).toUpperCase()+o.substr(1);for(var m=0;m<v.length;m++){if(typeof n[v[m]+o]=="string"){return true}}return false}var k=true;if(!a()){k=false}h.prototype={init:function(){var r=d(this.element);var n=this;var q=true;if((n.options.touchDevices==false)&&(j())){q=false}if(g.all&&!g.querySelector){q=false}if(q==true){if((this.options.iconDesktop==true)&&(!j())||((this.options.iconTouch==true)&&(j()))){var m=r.attr("title");r.removeAttr("title");var p=n.options.iconTheme;var o=d('<span class="'+p.replace(".","")+'" title="'+m+'">'+this.options.icon+"</span>");o.insertAfter(r);r.data("tooltipsterIcon",o);r=o}var l=d.trim(n.options.content).length>0?n.options.content:r.attr("title");r.data("tooltipsterContent",l);r.removeAttr("title");if((this.options.touchDevices==true)&&(j())){r.bind("touchstart",function(t,s){n.showTooltip()})}else{if(this.options.trigger=="hover"){r.on("mouseenter.tooltipster",function(){n.showTooltip()});if(this.options.interactive==true){r.on("mouseleave.tooltipster",function(){var t=r.data("tooltipster");var u=false;if((t!==b)&&(t!=="")){t.mouseenter(function(){u=true});t.mouseleave(function(){u=false});var s=setTimeout(function(){if(u==true){t.mouseleave(function(){n.hideTooltip()})}else{n.hideTooltip()}},n.options.interactiveTolerance)}else{n.hideTooltip()}})}else{r.on("mouseleave.tooltipster",function(){n.hideTooltip()})}}if(this.options.trigger=="click"){r.on("click.tooltipster",function(){if((r.data("tooltipster")=="")||(r.data("tooltipster")==b)){n.showTooltip()}else{n.hideTooltip()}})}}}},showTooltip:function(m){var n=d(this.element);var l=this;if(n.data("tooltipsterIcon")!==b){n=n.data("tooltipsterIcon")}if(!n.hasClass("tooltipster-disable")){if((d(".tooltipster-base").not(".tooltipster-dying").length>0)&&(l.options.onlyOne==true)){d(".tooltipster-base").not(".tooltipster-dying").not(n.data("tooltipster")).each(function(){d(this).addClass("tooltipster-kill");var o=d(this).data("origin");o.data("plugin_tooltipster").hideTooltip()})}n.clearQueue().delay(l.options.delay).queue(function(){l.options.functionBefore(n,function(){if((n.data("tooltipster")!==b)&&(n.data("tooltipster")!=="")){var w=n.data("tooltipster");if(!w.hasClass("tooltipster-kill")){var s="tooltipster-"+l.options.animation;w.removeClass("tooltipster-dying");if(k==true){w.clearQueue().addClass(s+"-show")}if(l.options.timer>0){var q=w.data("tooltipsterTimer");clearTimeout(q);q=setTimeout(function(){w.data("tooltipsterTimer",b);l.hideTooltip()},l.options.timer);w.data("tooltipsterTimer",q)}if((l.options.touchDevices==true)&&(j())){d("body").bind("touchstart",function(B){if(l.options.interactive==true){var D=d(B.target);var C=true;D.parents().each(function(){if(d(this).hasClass("tooltipster-base")){C=false}});if(C==true){l.hideTooltip();d("body").unbind("touchstart")}}else{l.hideTooltip();d("body").unbind("touchstart")}})}}}else{d("body").css("overflow-x","hidden");var x=n.data("tooltipsterContent");var u=l.options.theme;var y=u.replace(".","");var s="tooltipster-"+l.options.animation;var r="-webkit-transition-duration: "+l.options.speed+"ms; -webkit-animation-duration: "+l.options.speed+"ms; -moz-transition-duration: "+l.options.speed+"ms; -moz-animation-duration: "+l.options.speed+"ms; -o-transition-duration: "+l.options.speed+"ms; -o-animation-duration: "+l.options.speed+"ms; -ms-transition-duration: "+l.options.speed+"ms; -ms-animation-duration: "+l.options.speed+"ms; transition-duration: "+l.options.speed+"ms; animation-duration: "+l.options.speed+"ms;";var o=l.options.fixedWidth>0?"width:"+l.options.fixedWidth+"px;":"";var z=l.options.maxWidth>0?"max-width:"+l.options.maxWidth+"px;":"";var t=l.options.interactive==true?"pointer-events: auto;":"";var w=d('<div class="tooltipster-base '+y+" "+s+'" style="'+o+" "+z+" "+t+" "+r+'"><div class="tooltipster-content">'+x+"</div></div>");w.appendTo("body");n.data("tooltipster",w);w.data("origin",n);l.positionTooltip();l.options.functionReady(n,w);if(k==true){w.addClass(s+"-show")}else{w.css("display","none").removeClass(s).fadeIn(l.options.speed)}var A=x;var p=setInterval(function(){var B=n.data("tooltipsterContent");if(d("body").find(n).length==0){w.addClass("tooltipster-dying");l.hideTooltip()}else{if((A!==B)&&(B!=="")){A=B;w.find(".tooltipster-content").html(B);if(l.options.updateAnimation==true){if(a()){w.css({width:"","-webkit-transition":"all "+l.options.speed+"ms, width 0ms, height 0ms, left 0ms, top 0ms","-moz-transition":"all "+l.options.speed+"ms, width 0ms, height 0ms, left 0ms, top 0ms","-o-transition":"all "+l.options.speed+"ms, width 0ms, height 0ms, left 0ms, top 0ms","-ms-transition":"all "+l.options.speed+"ms, width 0ms, height 0ms, left 0ms, top 0ms",transition:"all "+l.options.speed+"ms, width 0ms, height 0ms, left 0ms, top 0ms"}).addClass("tooltipster-content-changing");setTimeout(function(){w.removeClass("tooltipster-content-changing");setTimeout(function(){w.css({"-webkit-transition":l.options.speed+"ms","-moz-transition":l.options.speed+"ms","-o-transition":l.options.speed+"ms","-ms-transition":l.options.speed+"ms",transition:l.options.speed+"ms"})},l.options.speed)},l.options.speed)}else{w.fadeTo(l.options.speed,0.5,function(){w.fadeTo(l.options.speed,1)})}}l.positionTooltip()}}if((d("body").find(w).length==0)||(d("body").find(n).length==0)){clearInterval(p)}},200);if(l.options.timer>0){var q=setTimeout(function(){w.data("tooltipsterTimer",b);l.hideTooltip()},l.options.timer+l.options.speed);w.data("tooltipsterTimer",q)}if((l.options.touchDevices==true)&&(j())){d("body").bind("touchstart",function(B){if(l.options.interactive==true){var D=d(B.target);var C=true;D.parents().each(function(){if(d(this).hasClass("tooltipster-base")){C=false}});if(C==true){l.hideTooltip();d("body").unbind("touchstart")}}else{l.hideTooltip();d("body").unbind("touchstart")}})}w.mouseleave(function(){l.hideTooltip()})}});n.dequeue()})}},hideTooltip:function(m){var p=d(this.element);var l=this;if(p.data("tooltipsterIcon")!==b){p=p.data("tooltipsterIcon")}var o=p.data("tooltipster");if(o==b){o=d(".tooltipster-dying")}p.clearQueue();if((o!==b)&&(o!=="")){var q=o.data("tooltipsterTimer");if(q!==b){clearTimeout(q)}var n="tooltipster-"+l.options.animation;if(k==true){o.clearQueue().removeClass(n+"-show").addClass("tooltipster-dying").delay(l.options.speed).queue(function(){o.remove();p.data("tooltipster","");d("body").css("verflow-x","");l.options.functionAfter(p)})}else{o.clearQueue().addClass("tooltipster-dying").fadeOut(l.options.speed,function(){o.remove();p.data("tooltipster","");d("body").css("verflow-x","");l.options.functionAfter(p)})}}},positionTooltip:function(O){var A=d(this.element);var ab=this;if(A.data("tooltipsterIcon")!==b){A=A.data("tooltipsterIcon")}if((A.data("tooltipster")!==b)&&(A.data("tooltipster")!=="")){var ah=A.data("tooltipster");ah.css("width","");var ai=d(f).width();var B=A.outerWidth(false);var ag=A.outerHeight(false);var al=ah.outerWidth(false);var m=ah.innerWidth()+1;var M=ah.outerHeight(false);var aa=A.offset();var Z=aa.top;var u=aa.left;var y=b;if(A.is("area")){var T=A.attr("shape");var af=A.parent().attr("name");var P=d('img[usemap="#'+af+'"]');var n=P.offset().left;var L=P.offset().top;var W=A.attr("coords")!==b?A.attr("coords").split(","):b;if(T=="circle"){var N=parseInt(W[0]);var r=parseInt(W[1]);var D=parseInt(W[2]);ag=D*2;B=D*2;Z=L+r-D;u=n+N-D}else{if(T=="rect"){var N=parseInt(W[0]);var r=parseInt(W[1]);var q=parseInt(W[2]);var J=parseInt(W[3]);ag=J-r;B=q-N;Z=L+r;u=n+N}else{if(T=="poly"){var x=[];var ae=[];var H=0,G=0,ad=0,ac=0;var aj="even";for(i=0;i<W.length;i++){var F=parseInt(W[i]);if(aj=="even"){if(F>ad){ad=F;if(i==0){H=ad}}if(F<H){H=F}aj="odd"}else{if(F>ac){ac=F;if(i==1){G=ac}}if(F<G){G=F}aj="even"}}ag=ac-G;B=ad-H;Z=L+G;u=n+H}else{ag=P.outerHeight(false);B=P.outerWidth(false);Z=L;u=n}}}}if(ab.options.fixedWidth==0){ah.css({width:m+"px","padding-left":"0px","padding-right":"0px"})}var s=0,V=0;var X=parseInt(ab.options.offsetY);var Y=parseInt(ab.options.offsetX);var p="";function w(){var an=d(f).scrollLeft();if((s-an)<0){var am=s-an;s=an;ah.data("arrow-reposition",am)}if(((s+al)-an)>ai){var am=s-((ai+an)-al);s=(ai+an)-al;ah.data("arrow-reposition",am)}}function t(an,am){if(((Z-d(f).scrollTop()-M-X-12)<0)&&(am.indexOf("top")>-1)){ab.options.position=an;y=am}if(((Z+ag+M+12+X)>(d(f).scrollTop()+d(f).height()))&&(am.indexOf("bottom")>-1)){ab.options.position=an;y=am;V=(Z-M)-X-12}}if(ab.options.position=="top"){var Q=(u+al)-(u+B);s=(u+Y)-(Q/2);V=(Z-M)-X-12;w();t("bottom","top")}if(ab.options.position=="top-left"){s=u+Y;V=(Z-M)-X-12;w();t("bottom-left","top-left")}if(ab.options.position=="top-right"){s=(u+B+Y)-al;V=(Z-M)-X-12;w();t("bottom-right","top-right")}if(ab.options.position=="bottom"){var Q=(u+al)-(u+B);s=u-(Q/2)+Y;V=(Z+ag)+X+12;w();t("top","bottom")}if(ab.options.position=="bottom-left"){s=u+Y;V=(Z+ag)+X+12;w();t("top-left","bottom-left")}if(ab.options.position=="bottom-right"){s=(u+B+Y)-al;V=(Z+ag)+X+12;w();t("top-right","bottom-right")}if(ab.options.position=="left"){s=u-Y-al-12;myLeftMirror=u+Y+B+12;var K=(Z+M)-(Z+A.outerHeight(false));V=Z-(K/2)-X;if((s<0)&&((myLeftMirror+al)>ai)){var o=parseFloat(ah.css("border-width"))*2;var l=(al+s)-o;ah.css("width",l+"px");M=ah.outerHeight(false);s=u-Y-l-12-o;K=(Z+M)-(Z+A.outerHeight(false));V=Z-(K/2)-X}else{if(s<0){s=u+Y+B+12;ah.data("arrow-reposition","left")}}}if(ab.options.position=="right"){s=u+Y+B+12;myLeftMirror=u-Y-al-12;var K=(Z+M)-(Z+A.outerHeight(false));V=Z-(K/2)-X;if(((s+al)>ai)&&(myLeftMirror<0)){var o=parseFloat(ah.css("border-width"))*2;var l=(ai-s)-o;ah.css("width",l+"px");M=ah.outerHeight(false);K=(Z+M)-(Z+A.outerHeight(false));V=Z-(K/2)-X}else{if((s+al)>ai){s=u-Y-al-12;ah.data("arrow-reposition","right")}}}if(ab.options.arrow==true){var I="tooltipster-arrow-"+ab.options.position;if(ab.options.arrowColor.length<1){var R=ah.css("background-color")}else{var R=ab.options.arrowColor}var ak=ah.data("arrow-reposition");if(!ak){ak=""}else{if(ak=="left"){I="tooltipster-arrow-right";ak=""}else{if(ak=="right"){I="tooltipster-arrow-left";ak=""}else{ak="left:"+ak+"px;"}}}if((ab.options.position=="top")||(ab.options.position=="top-left")||(ab.options.position=="top-right")){var U=parseFloat(ah.css("border-bottom-width"));var z=ah.css("border-bottom-color")}else{if((ab.options.position=="bottom")||(ab.options.position=="bottom-left")||(ab.options.position=="bottom-right")){var U=parseFloat(ah.css("border-top-width"));var z=ah.css("border-top-color")}else{if(ab.options.position=="left"){var U=parseFloat(ah.css("border-right-width"));var z=ah.css("border-right-color")}else{if(ab.options.position=="right"){var U=parseFloat(ah.css("border-left-width"));var z=ah.css("border-left-color")}else{var U=parseFloat(ah.css("border-bottom-width"));var z=ah.css("border-bottom-color")}}}}if(U>1){U++}var E="";if(U!==0){var C="";var S="border-color: "+z+";";if(I.indexOf("bottom")!==-1){C="margin-top: -"+U+"px;"}else{if(I.indexOf("top")!==-1){C="margin-bottom: -"+U+"px;"}else{if(I.indexOf("left")!==-1){C="margin-right: -"+U+"px;"}else{if(I.indexOf("right")!==-1){C="margin-left: -"+U+"px;"}}}}E='<span class="tooltipster-arrow-border" style="'+C+" "+S+';"></span>'}ah.find(".tooltipster-arrow").remove();p='<div class="'+I+' tooltipster-arrow" style="'+ak+'">'+E+'<span style="border-color:'+R+';"></span></div>';ah.append(p)}ah.css({top:V+"px",left:s+"px"});if(y!==b){ab.options.position=y}}}};d.fn[e]=function(m){if(typeof m==="string"){var o=this;var l=arguments[1];if(o.data("plugin_tooltipster")==b){var n=o.find("*");o=d();n.each(function(){if(d(this).data("plugin_tooltipster")!==b){o.push(d(this))}})}o.each(function(){switch(m.toLowerCase()){case"show":d(this).data("plugin_tooltipster").showTooltip();break;case"hide":d(this).data("plugin_tooltipster").hideTooltip();break;case"disable":d(this).addClass("tooltipster-disable");break;case"enable":d(this).removeClass("tooltipster-disable");break;case"destroy":d(this).data("plugin_tooltipster").hideTooltip();d(this).data("plugin_tooltipster","").attr("title",o.data("tooltipsterContent")).data("tooltipsterContent","").data("plugin_tooltipster","").off("mouseenter.tooltipster mouseleave.tooltipster click.tooltipster");break;case"update":d(this).data("tooltipsterContent",l);break;case"reposition":d(this).data("plugin_tooltipster").positionTooltip();break}});return this}return this.each(function(){if(!d.data(this,"plugin_"+e)){d.data(this,"plugin_"+e,new h(this,m))}var p=d(this).data("plugin_tooltipster").options;if((p.iconDesktop==true)&&(!j())||((p.iconTouch==true)&&(j()))){var q=d(this).data("plugin_tooltipster");d(this).next().data("plugin_tooltipster",q)}})};if(j()){f.addEventListener("orientationchange",function(){if(d(".tooltipster-base").length>0){d(".tooltipster-base").each(function(){var l=d(this).data("origin");l.data("plugin_tooltipster").hideTooltip()})}},false)}d(f).on("resize.tooltipster",function(){var l=d(".tooltipster-base").data("origin");if((l!==null)&&(l!==b)){l.tooltipster("reposition")}})})(jQuery,window,document);

// Pajinate
;
(function($) { /*******************************************************************************************/
        // jquery.pajinate.js - version 0.4
        // A jQuery plugin for paginating through any number of DOM elements
        // 
        // Copyright (c) 2010, Wes Nolte (http://wesnolte.com)
        // Licensed under the MIT License (MIT-LICENSE.txt)
        // http://www.opensource.org/licenses/mit-license.php
        // Created: 2010-04-16 | Updated: 2010-04-26
        //
        /*******************************************************************************************/

        $.fn.pajinate = function(options) {
                // Set some state information
                var current_page = 'current_page';
                var items_per_page = 'items_per_page';

                var meta;

                // Setup default option values
                var defaults = {
                        item_container_id: '.rajoitelista',
                        items_per_page: 20,
                        nav_panel_id: '.pagination',
                        nav_info_id: '.info_text',
                        num_page_links_to_display: 3,
                        start_page: 0,
                        wrap_around: false,
                        nav_label_first: 'Ensimmäinen',
                        nav_label_prev: 'Edellinen',
                        nav_label_next: 'Seuraava',
                        nav_label_last: 'Viimeinen',
                        nav_order: ["first", "prev", "num", "next", "last"],
                        nav_label_info: 'Esillä {0}-{1} yhteensä {2} rajoitteesta',
                        show_first_last: true,
                        abort_on_small_lists: false,
                        jquery_ui: false,
                        jquery_ui_active: "ui-state-highlight",
                        jquery_ui_default: "ui-state-default",
                        jquery_ui_disabled: "ui-state-disabled"
                };

                var options = $.extend(defaults, options);
                var $item_container;
                var $page_container;
                var $items;
                var $nav_panels;
                var total_page_no_links;
                var jquery_ui_default_class = options.jquery_ui ? options.jquery_ui_default : '';
                var jquery_ui_active_class = options.jquery_ui ? options.jquery_ui_active : '';
                var jquery_ui_disabled_class = options.jquery_ui ? options.jquery_ui_disabled : '';

                return this.each(function() {
                        $page_container = $(this);
                        $item_container = $(this).find(options.item_container_id);
                        $items = $page_container.find(options.item_container_id).children();

                        if (options.abort_on_small_lists && options.items_per_page >= $items.size()) return $page_container;

                        meta = $page_container;

                        // Initialize meta data
                        meta.data(current_page, 0);
                        meta.data(items_per_page, options.items_per_page);

                        // Get the total number of items
                        var total_items = $item_container.children().size();

                        // Calculate the number of pages needed
                        var number_of_pages = Math.ceil(total_items / options.items_per_page);

                        // Construct the nav bar
                        var more = '<span class="ellipse more">...</span>';
                        var less = '<span class="ellipse less">...</span>';
                        var first = !options.show_first_last ? '' : '<a class="first_link ' + jquery_ui_default_class + '" href="">' + options.nav_label_first + '</a>';
                        var last = !options.show_first_last ? '' : '<a class="last_link ' + jquery_ui_default_class + '" href="">' + options.nav_label_last + '</a>';

                        var navigation_html = "";

                        for (var i = 0; i < options.nav_order.length; i++) {
                                switch (options.nav_order[i]) {
                                case "first":
                                        navigation_html += first;
                                        break;
                                case "last":
                                        navigation_html += last;
                                        break;
                                case "next":
                                        navigation_html += '<a class="next_link ' + jquery_ui_default_class + '" href="">' + options.nav_label_next + '</a>';
                                        break;
                                case "prev":
                                        navigation_html += '<a class="previous_link ' + jquery_ui_default_class + '" href="">' + options.nav_label_prev + '</a>';
                                        break;
                                case "num":
                                        navigation_html += less;
                                        var current_link = 0;
                                        while (number_of_pages > current_link) {
                                                navigation_html += '<a class="page_link ' + jquery_ui_default_class + '" href="" longdesc="' + current_link + '">' + (current_link + 1) + '</a>';
                                                current_link++;
                                        }
                                        navigation_html += more;
                                        break;
                                default:
                                        break;
                                }

                        }

                        // And add it to the appropriate area of the DOM        
                        $nav_panels = $page_container.find(options.nav_panel_id);
                        $nav_panels.html(navigation_html).each(function() {

                                $(this).find('.page_link:first').addClass('first');
                                $(this).find('.page_link:last').addClass('last');

                        });

                        // Hide the more/less indicators
                        $nav_panels.children('.ellipse').hide();

                        // Set the active page link styling
                        $nav_panels.find('.previous_link').next().next().addClass('active_page ' + jquery_ui_active_class);

                        /* Setup Page Display */
                        // And hide all pages
                        $items.hide();
                        // Show the first page                        
                        $items.slice(0, meta.data(items_per_page)).show();

                        /* Setup Nav Menu Display */
                        // Page number slices
                        total_page_no_links = $page_container.find(options.nav_panel_id + ':first').children('.page_link').size();
                        options.num_page_links_to_display = Math.min(options.num_page_links_to_display, total_page_no_links);

                        $nav_panels.children('.page_link').hide(); // Hide all the page links
                        // And only show the number we should be seeing
                        $nav_panels.each(function() {
                                $(this).children('.page_link').slice(0, options.num_page_links_to_display).show();
                        });

                        /* Bind the actions to their respective links */

                        // Event handler for 'First' link
                        $page_container.find('.first_link').click(function(e) {
                                e.preventDefault();

                                movePageNumbersRight($(this), 0);
                                gotopage(0);
                        });

                        // Event handler for 'Last' link
                        $page_container.find('.last_link').click(function(e) {
                                e.preventDefault();
                                var lastPage = total_page_no_links - 1;
                                movePageNumbersLeft($(this), lastPage);
                                gotopage(lastPage);
                        });

                        // Event handler for 'Prev' link
                        $page_container.find('.previous_link').click(function(e) {
                                e.preventDefault();
                                showPrevPage($(this));
                        });


                        // Event handler for 'Next' link
                        $page_container.find('.next_link').click(function(e) {
                                e.preventDefault();
                                showNextPage($(this));
                        });

                        // Event handler for each 'Page' link
                        $page_container.find('.page_link').click(function(e) {
                                e.preventDefault();
                                gotopage($(this).attr('longdesc'));
                        });

                        // Goto the required page
                        gotopage(parseInt(options.start_page));
                        toggleMoreLess();
                        if (!options.wrap_around) tagNextPrev();
                });

                function showPrevPage(e) {
                        new_page = parseInt(meta.data(current_page)) - 1;

                        // Check that we aren't on a boundary link
                        if ($(e).siblings('.active_page').prev('.page_link').length == true) {
                                movePageNumbersRight(e, new_page);
                                gotopage(new_page);
                        }
                        else if (options.wrap_around) {
                                gotopage(total_page_no_links - 1);
                        }

                };

                function showNextPage(e) {
                        new_page = parseInt(meta.data(current_page)) + 1;

                        // Check that we aren't on a boundary link
                        if ($(e).siblings('.active_page').next('.page_link').length == true) {
                                movePageNumbersLeft(e, new_page);
                                gotopage(new_page);
                        }
                        else if (options.wrap_around) {
                                gotopage(0);
                        }

                };

                function gotopage(page_num) {

                        page_num = parseInt(page_num, 10)

                        var ipp = parseInt(meta.data(items_per_page));

                        // Find the start of the next slice
                        start_from = page_num * ipp;

                        // Find the end of the next slice
                        end_on = start_from + ipp;
                        // Hide the current page        
                        var items = $items.hide().slice(start_from, end_on);

                        items.show();

                        // Reassign the active class
                        $page_container.find(options.nav_panel_id).children('.page_link[longdesc=' + page_num + ']').addClass('active_page ' + jquery_ui_active_class).siblings('.active_page').removeClass('active_page ' + jquery_ui_active_class);

                        // Set the current page meta data                                                        
                        meta.data(current_page, page_num);
                        /*########## Ajout de l'option page courante + nombre de pages*/
                            var $current_page = parseInt(meta.data(current_page)+1);
                            // Get the total number of items
                            var total_items = $item_container.children().size();
                            // Calculate the number of pages needed
                            var $number_of_pages = Math.ceil(total_items / options.items_per_page);
                            /*##################################################################*/
                        $page_container.find(options.nav_info_id).html(options.nav_label_info.replace("{0}", start_from + 1).
                        replace("{1}", start_from + items.length).replace("{2}", $items.length).replace("{3}", $current_page).replace("{4}", $number_of_pages));

                        // Hide the more and/or less indicators
                        toggleMoreLess();

                        // Add a class to the next or prev links if there are no more pages next or previous to the active page
                        tagNextPrev();

                        // check if the onPage callback is available and call it
                        if (typeof(options.onPageDisplayed) !== "undefined" ) {
                                options.onPageDisplayed.call(this, page_num + 1)
                        }

                }

                // Methods to shift the diplayed index of page numbers to the left or right


                function movePageNumbersLeft(e, new_p) {
                        var new_page = new_p;

                        var $current_active_link = $(e).siblings('.active_page');

                        if ($current_active_link.siblings('.page_link[longdesc=' + new_page + ']').css('display') == 'none') {

                                $nav_panels.each(function() {
                                        $(this).children('.page_link').hide() // Hide all the page links
                                        .slice(parseInt(new_page - options.num_page_links_to_display + 1), new_page + 1).show();
                                });
                        }

                }

                function movePageNumbersRight(e, new_p) {
                        var new_page = new_p;

                        var $current_active_link = $(e).siblings('.active_page');

                        if ($current_active_link.siblings('.page_link[longdesc=' + new_page + ']').css('display') == 'none') {

                                $nav_panels.each(function() {
                                        $(this).children('.page_link').hide() // Hide all the page links
                                        .slice(new_page, new_page + parseInt(options.num_page_links_to_display)).show();
                                });
                        }
                }

                // Show or remove the ellipses that indicate that more page numbers exist in the page index than are currently shown


                function toggleMoreLess() {

                        if (!$nav_panels.children('.page_link:visible').hasClass('last')) {
                                $nav_panels.children('.more').show();
                        }
                        else {
                                $nav_panels.children('.more').hide();
                        }

                        if (!$nav_panels.children('.page_link:visible').hasClass('first')) {
                                $nav_panels.children('.less').show();
                        }
                        else {
                                $nav_panels.children('.less').hide();
                        }
                }

                /* Add the style class ".no_more" to the first/prev and last/next links to allow custom styling */

                function tagNextPrev() {
                        if ($nav_panels.children('.last').hasClass('active_page')) {
                                $nav_panels.children('.next_link').add('.last_link').addClass('no_more ' + jquery_ui_disabled_class);
                        }
                        else {
                                $nav_panels.children('.next_link').add('.last_link').removeClass('no_more ' + jquery_ui_disabled_class);
                        }

                        if ($nav_panels.children('.first').hasClass('active_page')) {
                                $nav_panels.children('.previous_link').add('.first_link').addClass('no_more ' + jquery_ui_disabled_class);
                        }
                        else {
                                $nav_panels.children('.previous_link').add('.first_link').removeClass('no_more ' + jquery_ui_disabled_class);
                        }
                }

        };

})(jQuery);