/*
$Id: shareTools.js 119236 2013-01-14 23:59:09Z reed.emmons $
/js/common/sharetools/2.0/shareTools.js
(c) 2011 The New York Times Company
*/

NYTD = NYTD || {};
NYTD.shareTools = (function($) {
    
    var config = {
        mainClassName : 'shareTools',
        itemClassName : 'shareToolsItem',
        defaultActiveShares : ['facebook|Facebook', 'google|Google+', 'twitter|Twitter'],
        defaultUrl : window.location.href.replace( /#.*/, "" ),
        defaultTitle : $('meta[property="og:title"]').attr("content") || document.title,
        defaultDescription : $('meta[name=description]').attr("content") || "",
        defaultAdPosition : 'Frame4A',
        defaultOverlayAdPosition : 'Frame6A',
        defaultWidth : 600,
        defaultHeight : 450,
        defaultTransition : 'fade',
        labelSpecialChar : '|',
        loadedAdPositions : [],
        shortUrlApi : 'http://www.nytimes.com/svc/bitly/shorten.jsonp',
        emailThisUrl : NYTD.Hosts.wwwHost.replace('http', 'https') + '/mem/email-this.html?url=',
        count : 0
    };

    var templates = {

        overlay: function (data) {
            var i, sharesLen;
            var shareList = [];

            for (i = 0, sharesLen = data.shares.length; i < sharesLen; i += 1) {
                    shareList.push('<li data-share="', data.shares[i].name, '" class="', data.shares[i].classes, '"><span>', data.shares[i].label, '</span></li>');
            }
            shareList = shareList.join("");

            return [
                '<div id="shareToolsOverlayContainer" class="shareToolsOverlayContainer shareToolsInstance shareToolsThemeClassic" style="display:none;">',
                    '<div id="shareToolsOverlay" class="shareToolsOverlay"></div>',
                    '<div id="shareToolsDialogBox" class="shareToolsDialogBox">',
                        '<div class="shareToolsInset">',
                            '<div class="shareToolsHeader shareToolsOpposingFloatControl shareToolsWrap">',
                                '<a href="#" class="element2 shareToolsDialogBoxClose" id="shareToolsDialogBoxClose">Close</a>',
                                '<h5 class="element1">Share</h5>',
                            '</div>',
                            '<div id="shareToolsDialogBoxContent" class="shareToolsDialogBoxContent shareToolsSingleRule">',
                                '<div class="shareToolsBox shareToolsWrap">',
                                    '<div class="shareToolsColumn">',
                                        '<div class="shareToolsInset">',
                                            '<ul class="shareToolsList">',
                                                shareList,
                                            '</ul>',
                                        '</div>',
                                    '</div>',
                                    '<div class="shareToolsColumn shareToolsLastColumn">',
                                        '<div class="shareToolsInset">',
                                                '<ul class="shareToolsList"></ul>',
                                        '</div>',
                                    '</div>',
                                '</div>',
                            '</div>',
                            '<div id="shareToolsFooter" class="shareToolsFooter">',
                                '<div id="', data.options.adPosition, '" class="', data.options.adPosition, '"></div>',
                            '</div>',
                        '</div>',
                    '</div>',
                '</div>'
            ].join("");
        },

        shareList : function (data) {
            var i, shareLen;
            var shareList = [];

            for (i = 0, shareLen = data.shares.length; i < shareLen; i += 1) {
                if (data.shares[i].name === "ad") {
                        shareList.push('<li data-share="', data.shares[i].name, '" class="', data.shares[i].classes, ' ', data.shares[i].adPosition, '" id="', data.shares[i].adPosition, '"></li>');
                } else if (data.shares[i].type === "link") {
                        shareList.push('<li data-share="', data.shares[i].name, '" class="', data.shares[i].classes, '"><a href="', data.shares[i].postUrl, '">', data.shares[i].label, '</a></li>');
                } else {
                        shareList.push('<li data-share="', data.shares[i].name, '" class="', data.shares[i].classes, '"><span>', data.shares[i].label, '</span></li>');
                }
            }
            shareList = shareList.join("");

            return [
                '<div class="shareToolsBox">',
                    '<ul class="shareToolsList">',
                        shareList,
                    '</ul>',
                '</div>'
            ].join("");
        },

        emailThisModal : function (data) {
            var scrolling = (window.postMessage) ? 'no' : 'yes';
            return '<iframe src="' + config.emailThisUrl + encodeURIComponent(data.url) + '" title="Email This" id="emailthis" scrolling="' + scrolling + '" marginheight="0" marginwidth="0" frameborder="0"></iframe>';
        },

        xpsLoginModal : function () {
            return [
                '<div>',
                    '<div class="modalTitle">Log In to Save This Item</div>',
                    '<div class="modalBody">Items that you save may be read at any time on your computer, iPad, iPhone or Android devices</div>',
                    '<div class="modalFooter">',
                        '<a class="modalButton register" href="https://myaccount.nytimes.com/gst/regi.html">Create An Account</a>',
                        '<a class="modalButton login" href="' + (NYTD.Hosts.myaccountHost || "https://myaccount.nytimes.com") + '/auth/login?URI=' + config.defaultUrl + '">Log In</a>',
                    '</div>',
                '</div>'
            ].join('');
        },

        xpsSaveModal: function () {
            return [
                '<div>',
                    '<div class="modalTitle">Saved</div>',
                    '<div class="modalBody">Items that you save may be read at any time on your computer, iPad, iPhone or Android devices.  ',
                         'Access your saved items by selecting <a href="http://www.nytimes.com/saved">Saved Items</a> from the menu under your username ',
                         'at the top right of any page on NYTimes.com</div>',
                    '<div class="modalFooter">',
                    '</div>',
                '</div>'
            ].join('');
        }
    };
    
    var tools = {
        facebook : {
            active : true,
            onShowAll : true,
            label : "Facebook",
            postUrl : "http://www.facebook.com/sharer.php",
            postType : "popup",
            shareParameters : {
                url : "u"
            },
            smid : "fb-share",
            width : 655,
            height : 430
        },
        twitter : {
            active : true,
            onShowAll : true,
            label : "Twitter",
            postUrl : "https://twitter.com/share",
            postType : "popup",
            shareParameters : {
                url : "url",
                title : "text"
            },
            smid : "tw-share",
            width : 600,
            height : 450
        },
        google : {
            active : true,
            onShowAll : true,
            label : "Google+",
            postUrl : "https://plus.google.com/share",
            postType : "popup",
            shareParameters : {
                url : "url"
            },
            urlParameters : {
                hl : "en-US"
            },
            smid : "go-share",
            width : 600,
            height : 600
        },
        tumblr : {
            active : true,
            onShowAll : true,
            label : "Tumblr",
            postUrl : "http://www.tumblr.com/share/link",
            postType : "popup",
            shareParameters : {
                url : "url",
                title : "name",
                description : "description"
            },
            smid : "tu-share",
            width : 560
        },
        linkedin : {
            active : true,
            onShowAll : true,
            label : "Linkedin",
            postUrl : "http://www.linkedin.com/shareArticle",
            postType : "popup",
            shareParameters : {
                url : "url",
                title : "title",
                description : "summary"
            },
            urlParameters : {
                mini : "true",
                source : "The New York Times"
            },
            smid : "li-share",
            width : 750,
            height : 450
        },
        reddit : {
            active : true,
            onShowAll : true,
            label : "Reddit",
            postUrl : "http://www.reddit.com/submit",
            postType : "popup",
            shareParameters : {
                url : "url",
                title : "title"
            },
            smid : "re-share",
            width : 854,
            height : 550
        },
        email : {
            active : true,
            onShowAll : true,
            label : "E-mail"
        },
        permalink : {
            active : true,
            onShowAll : true,
            label : "Permalink",
            postUrl : "http://www.nytimes.com/export_html/common/new_article_post.html",
            postType : "popup",
            shareParameters : {
                url : "url",
                title : "title",
                description : "summary"
            },
            smid : "pl-share",
            width : 460,
            height : 380
        },
        showall : {
            active : true,
            onShowAll : false,
            label : "Show All"
        },
        reprints : {
            active : true,
            onShowAll : false,
            label : "Reprints",
            postUrl : "https://s100.copyright.com/AppDispatchServlet",
            postType : "popup",
            shareParameters : {
                url : "contentID"
            },
            urlParameters : {
                publisherName : "The New York Times",
                publication : "nytimes.com",
                token : "",
                orderBeanReset : "true",
                postType : "",
                wordCount : "12",
                title : $('.articleHeadline').text() !== "" ? $('.articleHeadline').text() : document.title,
                publicationDate : $('meta[name=dat]').attr('content') || "",
                author : $('meta[name=byl]').attr('content') || ""
            }
        },
        save : {
            active : true, //($('meta[http-equiv=Expires]').length === 0),
            onShowAll : false,
            label : "Save",
            postUrl : config.defaultUrl.replace(/\?.*/,''),
            postType: "popup",
            el : $()
        },
        print : {
            active : true,
            onShowAll : false,
            label : "Print",
            postUrl : config.defaultUrl,
            postType : "link",
            urlParameters : {
                pagewanted : "print"
            }
        },
        singlepage : {
            active : true,
            onShowAll : false,
            label : "Single Page",
            postUrl : config.defaultUrl,
            postType : "link",
            urlParameters : {
                pagewanted : "all"
            }
        },
        ad : {
            active : true,
            onShowAll : false,
            label : "Advertisement"
        }
    };

    var dialogs = {
        loginModal : {
            config: {
                uniqueId: "loginToSaveModal",
                positionType: "Fixed",
                overlayBackground: 'Light',
                additionalClasses: 'xpsModal',
                width: 485,
                modalHTML: templates.xpsLoginModal()
            },
            instance: null
        },
        saveModal : {
            config: {
                uniqueId: "firstSaveModal",
                positionType: "Center",
                overlayBackground: 'Light',
                additionalClasses: 'xpsModal',
                width: 660,
                modalHTML: templates.xpsSaveModal()
            },
            instance: null
        },
        // TODO:  Set up growls
        saveGrowl : {
            config: {},
            instance: null
        },
        removeGrowl : {
            config: {},
            instance: null
        }
    };

    function init(el, data) { // initialize and build a new shareTool
        var url, title, description, shares, adPosition, isMultiPage, transition, hasAd, list;
        var templateData, share, shareName, shareLabel, type, postUrl, hasSave, classes;
        var i = 0;
        var l = 0;

        el = $(el);
        data = data || el.data(); // If no data is passed, try looking for it on the element

        // Check if item has already been instantiated
        if (!el.hasClass('shareToolsInstance')) {
            url = data.url || config.defaultUrl; // Url or use default
            title = data.title || config.defaultTitle; // Title or use default
            description = data.description || config.defaultDescription; // Description or use default
            shares = data.shares ? data.shares.split(',') : config.defaultActiveShares; // Share list or use default
            adPosition = data.adPosition ? data.adPosition : config.defaultAdPosition;
            isMultiPage = $("#pageLinks").length > 0 ? true : false;
            transition = data.transition ? data.transition : config.defaultTransition;
            hasAd = false;
            templateData = [];
            config.count += 1;
            el.addClass('shareToolsInstance').data({
                url : url,
                title : title,
                description : description,
                count : config.count,
                transition : transition
            });
            
            for (l = shares.length; i < l; i+=1) {
                share = shares[i].split(config.labelSpecialChar);
                shareName = share[0];

                if (typeof tools[shareName] !== 'undefined') {
                    if (shareName !== "singlepage" || (shareName === "singlepage" && isMultiPage)) {
                        if (tools[shareName].active) {
                            if (shareName === 'ad') {
                                hasAd = true;
                            }
                            else if (shareName === 'save') {
                                hasSave = true;
                            }
                            type = tools[shareName].postType || "popup";
                            postUrl = type === "link" ? buildUrl(shareName) : "";
                            classes = config.itemClassName + ' ' + config.itemClassName + capitalizeFirstLetter(shareName);
                            if (shares[i].indexOf(config.labelSpecialChar) !== -1) { // custom or empty label
                                if (share[1]) {
                                    shareLabel = share[1];
                                } else {
                                    shareLabel = "";
                                    classes += ' noLabel';
                                }
                            } else {
                                shareLabel = tools[shareName].label; // get share Label from config
                            }

                            templateData.push({
                                label : shareLabel,
                                name : shareName,
                                classes : classes,
                                adPosition : hasAd ? adPosition : "",
                                type : type,
                                postUrl : postUrl
                            });
                        }
                    }
                }
            }
            el.html(templates.shareList({ shares : templateData })); // Inject new markup
            list = el.find('li'); // add first and last classes
            list.filter(':first').addClass('firstItem');
            list.filter(':last').addClass('lastItem');

            // Load ad
            if (hasAd) {
                loadAd(adPosition);
            }
            if (hasSave) {
                loadSave(list.filter('[data-share=save]'));
            }

            //Add event handlers for postmessage in email this
            if(window.attachEvent) {
                window.attachEvent("onmessage", NYTD.shareTools.iframeListener);
            } else if (window.addEventListener) {
                window.addEventListener("message", NYTD.shareTools.iframeListener, false);
            }
        }
    }
    
    function initOverlay() {
        var shareLabel, classes, shareItems, columnLength;
        var templateData = [];
            
        $.each(tools, function(share, obj) {
            if (tools[share].active && tools[share].onShowAll) {
                shareLabel = obj.label; // get share Label from config
                classes = config.itemClassName + ' ' + config.itemClassName + capitalizeFirstLetter(share);
                templateData.push({
                    label : shareLabel,
                    name : share,
                    classes : classes
                });
            }
        });

        $('body').append(templates.overlay({
            shares: templateData,
            options : { adPosition : config.defaultOverlayAdPosition }
        }));
                
        shareItems = $('#shareToolsDialogBoxContent').find('.shareToolsItem');
        columnLength = Math.ceil(shareItems.length / 2);
        $(shareItems).filter(':gt(' + (columnLength - 1) + ')').detach().appendTo($('#shareToolsDialogBoxContent .shareToolsLastColumn ul'));
        
        // Close button behavior
        $('#shareToolsDialogBoxClose').click(function(event) {
            event.preventDefault();
            if ($('#shareToolsOverlayContainer').data('transition') === 'toggle') {
                $('#shareToolsOverlayContainer').hide();
            } else {
                $('#shareToolsOverlayContainer').fadeOut();
            }
        });
    }

    function initEmailThisOverlay(url) {
        var emailThisModal = NYTD.UI.OverlayModal({
                uniqueId: "emailThisModal",
                modalTitle: "E-mail This",
                positionType: "Centered",
                width: 918,
                modalHTML: templates.emailThisModal({url: url}),
                addToPageCallback: function () {
                    $('#shareToolsOverlayContainer').hide();
                    emailThisModal.open({preventDefault: $.noop});
                },
                closeCallback: function () {
                    emailThisModal.removeFromPage();
                }
            });

        emailThisModal.addToPage();
    }
    
    function loadAd(adPosition) {
        // Load Ad
        if (window.adxads) {
            window.adxads = null;
        }
        $.getScript("http://www.nytimes.com/adx/bin/adx_remote.html?type=fastscript&page=www.nytimes.com/yr/mo/day&posall=" + adPosition + "&query=qstring&keywords=",
        function(data, textStatus, jqxhr) {
            if (window.adxads) {
                $('#' + adPosition).html(window.adxads[0]);
                config.loadedAdPositions.push(adPosition);
            }
        });
    }

    function initShareElements() {
        var widgets = $('.' + config.mainClassName);
        if (widgets.length > 0) {
            widgets.each(function(index,element) {
                init($(this));
            });
        }
    }
    
    function setupHandlers() {
        var selector = '.' + config.itemClassName + ' span'; // Build the selector
        
        $('body').delegate(selector, 'click', function(event) { // watch for clicks on selector and fire share function
            var shareName = $(this).parent().data('share');
            var elementData = $(this).closest('.shareToolsInstance').data();
            var options = tools[shareName];
            var data = $.extend(true, {}, elementData);

            if (options.smid) {
                data.url = data.url + paramChar(data.url) + "smid=" + options.smid; // append tracking id to url if present
            }
            if (shareName === 'showall') { // Click Show All
                $('#shareToolsOverlayContainer').data('z_loc', data.count + 'b');
                if ($.inArray(config.defaultOverlayAdPosition, config.loadedAdPositions) === -1) { // load Overlay Ad
                    loadAd(config.defaultOverlayAdPosition);
                }
                $('#shareToolsOverlayContainer').data('url', data.url).data('title', data.title).data('description', data.description).data('transition', data.transition);
                if ($('#shareToolsOverlayContainer').data('transition') === 'toggle') {
                    $('#shareToolsOverlayContainer').show();
                } else {
                    $('#shareToolsOverlayContainer').fadeIn();
                }
            }
            else if (shareName === 'email') { // Click Email This
                if (isLoggedIn()) {
                    initEmailThisOverlay(data.url);

                } else {
                    $('.shareToolsItemEmail span').addClass('sitewideLogInModal nytModalDirectionLeft');
                }
            }
            else if (shareName === 'twitter') { // Get short url
                shareShortUrl(shareName, data);
            }
            else if (shareName === 'save') {
                saveAction(data);
            }
            else { // Click on regular share link
                share(shareName, data);
            }
            
            track(
                'DCS.dcssip', 'www.nytimes.com',
                'DCS.dcsuri', '/Article-Tool-Share-' + capitalizeFirstLetter(shareName) + '.html',
                'WT.ti', 'Article-Tool-Share-' + capitalizeFirstLetter(shareName),
                'WT.z_dcsm', '1',
                'WT.z_loc', data.count || $('#shareToolsOverlayContainer').data('z_loc')
            );
        });
        
        $('html').delegate('#shareToolsOverlayDialogBox' , 'click', function(event) {
            event.stopPropagation();
        });
        
        $('html').delegate('#shareToolsOverlay', 'click', function(event) {
            event.preventDefault();
            if ($('#shareToolsOverlayContainer').data('transition') === 'toggle') {
                $('#shareToolsOverlayContainer').hide();
            } else {
                $('#shareToolsOverlayContainer').fadeOut();
            }
        });
    }

    function share(shareName, data) {
        var options = tools[shareName];
        var width = options.width ? options.width : config.defaultWidth;
        var height = options.height ? options.height : config.defaultHeight;
        var url = buildUrl(shareName, data);

        window.open(url, shareName + 'Share', 'toolbar=0,status=0,height=' + height + ',width=' + width + ',scrollbars=yes,resizable=yes');
    }

    function buildUrl(share, data) {
        var options = tools[share];
        var parameters = [];
        var postUrl = options.postUrl;
        // Check if we're using a rico URL
        var surlregex = /[\?&]share_url=([^&#]*)/;
        var results = surlregex.exec(window.location.search);

        data = data || {};

        if ( results !== null ) {
            data.url = decodeURIComponent(results[1].replace(/\+/g, ' '));
        }
    
        if (options.shareParameters && data) {
            var paramValue;
            $.each(options.shareParameters, function(paramName, paramKey) { // walk through parameters
                paramValue = data[paramName];
                parameters.push(paramKey + '=' + encodeURIComponent(paramValue));
            });
        }
        
        if (options.urlParameters) {
            $.each(options.urlParameters, function(paramName, paramValue) {
                parameters.push(paramName + '=' + encodeURIComponent(paramValue));
            });
        }

        parameters = parameters.join('&');
        postUrl = postUrl + paramChar(postUrl) + parameters;
        return postUrl;
    }

    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    function paramChar(string) {
        return string.indexOf('?') !== -1 ? '&' : '?';
    }

    function isLoggedIn() {
        var loggedIn = window.regstatus && window.regstatus === 'registered' ? true : false;
        return loggedIn;
    }
    
    function getURI() {
        var uri = window.location.href.replace(/[\?&]+gwh=[^&]+/, '');
        var parts = uri.split("?");
        var base = parts[0];
        var search = parts[1];

        if (search) {
            search = encodeURIComponent(search).replace('%', 'Q');
            uri = base + "&OQ=" + search;
        } else {
            uri = base;
        }
        return uri;
    }

    function shareShortUrl(shareName, shareData) {
        var ricoUrl = '';
        var surlregex = /[\?&]share_url=([^&#]*)/;
        var results = surlregex.exec(window.location.search);

        if ( results !== null ) {
            ricoUrl = decodeURIComponent(results[1].replace(/\+/g, ' '));
        }

        var content = ['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">',
                        '<html><head>',
                        '<script type="text/javascript" src="http://graphics8.nytimes.com/js/common.js"></script>',
                        '<script type="text/javascript">',
                        'function loadShortUrl() {',
                            'var url;',
                            'var ricoUrl = "', ricoUrl, '".replace(/\\s/g, "");',
                            'if (ricoUrl.length > 0) {',
                                'shortUrlRedirect(ricoUrl);',
                            '} else {',
                                'NYTD.jQuery.ajax({',
                                    'url: "', config.shortUrlApi, '",',
                                    'dataType: "jsonp",',
                                    'data: { "url" : "', shareData.url, '" },',
                                    'jsonpCallback: "callback",',
                                    'cache: true',
                                '}).success(function(data, textStatus, jqXHR){',
                                    'if (data && data.payload && data.payload.short_url) {',
                                        'short_url = data.payload.short_url;',
                                        'url = short_url;',
                                    '}',
                                    'shortUrlRedirect(url);',
                                '}).error(function(jqXHR, textStatus, errorThrown){',
                                    'shortUrlRedirect(url);',
                                '});',
                            '}',
                        '};',
                        'function shortUrlRedirect(url) {',
                            'window.location.href = "', tools[shareName].postUrl, '?url=" + encodeURIComponent(url) + "&text=', encodeURIComponent(shareData.title), '";',
                        '};',
                        '</script>',
                        '</head>',
                        '<body onload="loadShortUrl();"></body></html>'].join('');
        var w = window.open('', shareName + 'Share', 'toolbar=0,status=0,height=' + tools[shareName].height + ',width=' + tools[shareName].width + ',scrollbars=yes,resizable=yes');
        w.document.write(content);
        w.document.close(); // needed for chrome and safari
    }

    function track() {
        if ('dcsMultiTrack' in window) {
            window.dcsMultiTrack.apply(this, arguments);
        } else {
            setTimeout(function() {
                track.apply(this, arguments);
            }, 1000);
        }
    }

    function loadSave(el) {
        if (el && el.length > 0) {
            tools.save.el = tools.save.el.add(el);
        }

        setUpDialogs();
    }

    function setUpDialogs() {
        var hasDialogs = $('#firstSaveModalContainer').length > 0;

        if (!hasDialogs) {
            //add the modal css to the page
            $("<link/>", {href: NYTD.Hosts.cssHost + '/css/0.1/screen/common/modal/saveModal.css', rel: 'stylesheet', type: 'text/css'}).prependTo('head');

            dialogs.saveModal.instance = NYTD.UI.OverlayModal(dialogs.saveModal.config).addToPage();
            dialogs.loginModal.instance = NYTD.UI.OverlayModal(dialogs.loginModal.config).addToPage();

            dialogs.saveGrowl.instance = {
                open : function() {
                    NYTD.UI.Growl.save();
                }
            };
            dialogs.removeGrowl.instance = {
                open : function() {
                    NYTD.UI.Growl('Removed');
                }
            };
        }
    }

    function openDialog(name) {
        if (typeof name !== 'string' || !dialogs.hasOwnProperty(name)) {
            return false;
        }

        dialogs[name].instance.open({preventDefault: $.noop});
    }

    function toggleSaveButtonState(flag, optionalText) {
        var addClass, removeClass;
        var asset = NYTD.crossPlatformSave.check({
            url : tools.save.postUrl
        });

        if (!asset || asset.state !== 'active') {

            addClass = 'article-not-saved';
            removeClass = 'article-saved';

            tools.save.isSaved = false;
        }
        else {
            addClass = 'article-saved';
            removeClass = 'article-not-saved';

            tools.save.isSaved =  true;
        }

        tools.save.el.each(function() {
            if (flag) {
                $(this).removeClass('disabled ' + removeClass)
                       .addClass(addClass)
                       .find('span').text((optionalText || 'Save'));
            }
            else {
                $(this).addClass('disabled')
                       .find('span').text((optionalText || 'Saving...'));
            }
        });
    }

    function saveAction() {
        var success;
        var hasSaves = NYTD.cookieManager.get(NYTD.crossPlatformSave.getCookieName('save'));

        if (tools.save.isSaved) {
            openDialog('saveGrowl');
            return true;
        }

        if (isLoggedIn()) {
            success = NYTD.crossPlatformSave.request({
                requestType : 'save',
                success : function(response) {
                    toggleSaveButtonState(true);

                    if (hasSaves !== true && this.requestType === 'save') {
                        openDialog(this.requestType + 'Modal');
                    }
                    else {
                        openDialog(this.requestType + 'Growl');
                    }
                },
                fail : function() {
                    toggleSaveButtonState(false, 'Failed');
                    
                    setTimeout(function() {
                        toggleSaveButtonState(true);
                    }, 2000);

                },
                url : tools.save.postUrl
            });
        }
        else {
            openDialog('loginModal');
        }

        if (success) {
            toggleSaveButtonState(false);
        }
    }

    function iframeListener(e) {
        var messageObject;
        var wwwHost = NYTD.Hosts.wwwHost || 'http://www.nytimes.com';

        if (/\.nytimes\.com$/.test(e.origin)) {

            messageObject = e.data.match(/(.+)\:(.+)/);

            if (messageObject && messageObject[1] === 'frameheight') {
                $("#emailthis")
                    .css("height", messageObject[2])
                    .attr('scrolling', 'no');
            } else if (messageObject && messageObject[1] === 'closewindow') {
                $("#emailThisModalContainer .nytModalClose").click();
            } else if (messageObject && messageObject[1] === 'loginredirect') {
                window.location = wwwHost + '/auth/login?URI=' + config.defaultUrl;
            }
        }
    }
    
    return { //expose these to the outside
        init : init,
        initOverlay : initOverlay,
        initShareElements : initShareElements,
        setupHandlers : setupHandlers,
        iframeListener: iframeListener
    };
    
}(NYTD.jQuery));

NYTD.jQuery(document).ready(function() {
    NYTD.shareTools.initOverlay(); // Check if we have shareTools
    NYTD.shareTools.initShareElements(); // Initialize shareTools already on the page
    NYTD.shareTools.setupHandlers(); // Initialize click handlers
});
