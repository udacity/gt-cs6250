amznJQ.onReady('JQuery', function() { (function($){

    if (window.isRatingsBarSharedJavascriptLoaded) return;
    
    var widgetTypeToRatingType = {
        starRating            : 'onetofive',
        isNotInterested       : 'not-interested',
        isOwned               : 'owned',
        isExcluded            : 'excluded',
        isExcludedClickstream : 'excludedClickstream',
        isGift                : 'isGift'
    };
    
    var checkboxTypeToNonNullRatingValue = {
        isNotInterested       : 'NOTINTERESTED',
        isOwned               : 'OWN',
        isExcluded            : 'EXCLUDED',
        isExcludedClickstream : 'EXCLUDED',
        isGift                : 'ISGIFT'
    };
    
    var checkboxTypeToNullRatingValue = {
        isNotInterested       : 'NONE',
        isOwned               : 'NONE',
        isExcluded            : 'NONE',
        isExcludedClickstream : 'NONE',
        isGift                : 'NONE'
    };
    
    var widgetTypeToRefTagKey = {
        starRating            : 'ss',
        isNotInterested       : 'ni',
        isOwned               : 'ioi',
        isExcluded            : 'ex',
        isExcludedClickstream : 'exc',
        isGift                : 'gf'
    };
    
    var savedState = {
        starRating            : {},
        isNotInterested       : {},
        isOwned               : {},
        isExcluded            : {},
        isExcludedClickstream : {},
        isGift                : {},
        neutralMessage        : {}
    };
    
    var ratingsUIRoot            = {};
    var isSaved                  = {};
    var starMouseOverState       = {};
    var starTwinkler             = {};
    var msgTwinkler              = {};
    
    var defaultSettings          = {
        useTemplate           : 0,
        template              : 'ys-list',
        starRating            : 0,
        isOwned               : 0,
        isGift                : 0,
        isExcluded            : 0,
        isExcludedClickstream : 0,
        neutralMessage        : 'rate-it',
        key                   : "#",
        itemId                : "#",
        type                  : "asin",
        refTagSuffix          : "#"
    };
    
    var delayTime = 500;
    
    var templates = {
    };

    $.fn.amazonRatingsInterface = function (customSettings) {
        if (customSettings.asin) {
            // Backwards compatibility
            customSettings.itemId = customSettings.asin;
        }
        var settings = $.extend({}, defaultSettings, customSettings);
        var typedId = getTypedId(settings.itemId, settings.type);

        for (var stateType in savedState) {
            // Don't overwrite the state if already set for that ASIN
            if (typeof(savedState[stateType][typedId]) == 'undefined') {
                savedState[stateType][typedId] 
                    = (typeof(settings[stateType]) != 'undefined' && settings[stateType] != '') 
                        ? (isNaN(parseInt(settings[stateType],10)) ? settings[stateType] 
                                                                   : parseInt(settings[stateType],10))
                        : 0;
            }
        }
        starMouseOverState[typedId] = -1;
        return this.each(function() {
            var ratingsUI = $(this);
            if (settings.useTemplate) {
                var templateHTML = templates[settings.template];
                ratingsUI = $(templateHTML).appendTo($(this));
            }
            // jQuery.add() does not duplicate matched elements.
            ratingsUIRoot[typedId] = ratingsUI.add(ratingsUIRoot[typedId] || []);
            swapContent(ratingsUI);
            renderCheckbox(ratingsUI, settings.key, settings.itemId, settings.type, settings.refTagSuffix);
            renderStars(ratingsUI, settings.key, settings.itemId, settings.type, settings.refTagSuffix);
            renderMessages(ratingsUI, settings.key, typedId, settings.refTagSuffix);
        });
    };

    $.fn.amazonRatingsInterface.onPopoverShow = function (popover, settings) {
        var typedId = getTypedId(settings.itemId, settings.type);

        // jQuery.add() does not duplicate matched elements.
        ratingsUIRoot[typedId] = popover.find("#ratings_"+settings.key+"_"+typedId).add(ratingsUIRoot[typedId] || []);
        updateStarMessages(typedId);
        updateStars(typedId);
        $.each(['isNotInterested',
           'isOwned',
           'isExcluded',
           'isExcludedClickstream',
           'isGift'], function(i, checkboxType) {
            updateCheckbox(checkboxType, typedId);
           });
    }

    $.fn.amazonRatingsInterface.starImages = [
        '#', /* (0) Unrated         */
        '#', /* (1) Hate it         */
        '#', /* (2) Don't like it   */
        '#', /* (3) It's OK         */
        '#', /* (4) Like it         */
        '#'  /* (5) Love it         */
    ];
    
    $.fn.amazonRatingsInterface.checkboxImages = [
        '#', /* Unchecked           */
        '#', /* Checked             */
        '#'  /* Hover               */
    ];
    
    $.fn.amazonRatingsInterface.starRatings = [
        '#', /* (0) Unrated         */
        '#', /* (1) Hate it         */
        '#', /* (2) Don't like it   */
        '#', /* (3) It's OK         */
        '#', /* (4) Like it         */
        '#'  /* (5) Love it         */
    ];
    
    $.fn.amazonRatingsInterface.checkboxLabels = {
        'isOwned'               : "#",
        'isNotInterested'       : "#",
        'isExcluded'            : "#",
        'isExcludedClickstream' : "#",
        'isGift'                : "#"
    };
    
    $.fn.amazonRatingsInterface.ratingMessages = {
        'no-text'               : '&nbsp;',
        'rate-it'               : "#",
        'ratings-saved'         : "#"
    };
    
    $.fn.amazonRatingsInterface.globalSettings = {
        'sessionID'             : "#",
        'submitURL'             : "#",
        'templateName'          : "#"
    };
    
    $.fn.amazonRatingsInterface.preloadImages = function() {
        // For caching to work, the images must be stored inside
        // a data structure under top-level 'window' object.
        if (typeof window.RECS_preloadedImages == 'undefined') {
            window.RECS_preloadedImages = [];
        }
        $.each(        $.fn.amazonRatingsInterface.starImages
               .concat($.fn.amazonRatingsInterface.checkboxImages), function(i, v) {
            if (typeof v != 'undefined') {
                var image = new Image();
                image.src = v;
                window.RECS_preloadedImages.push(image);
            }
        });
    };
    
    var getRatingValueForWidgetType = function (widgetType, typedId) {
        if (widgetType == 'starRating') {
            return savedState.starRating[typedId];
        }
        else {
            var state = savedState[widgetType][typedId];
            return state ? checkboxTypeToNonNullRatingValue[widgetType]
                         : checkboxTypeToNullRatingValue[widgetType];
        }
    };
    
    var submitRating = function (itemId, type, updatedWidgetTypes, refTagSuffix) {
        var typedId = getTypedId(itemId, type);
        isSaved[typedId] = 1;
        refTagSuffix = refTagSuffix ? refTagSuffix : 'dp';
        var url = $.fn.amazonRatingsInterface.globalSettings.submitURL + "/ref=pd_recs_rate_" + refTagSuffix;
        var data = {
            'session-id'        : $.fn.amazonRatingsInterface.globalSettings.sessionID,
            'rating.source'     : "ir",
            'rating_asin'       : itemId,
            'type'              : type,
            'template-name'     : $.fn.amazonRatingsInterface.globalSettings.templateName,
            'return.response'   : '204'
        };
        $.each(updatedWidgetTypes, function(i, widgetType) {
            data[typedId+'.rating.'+widgetTypeToRatingType[widgetType]] = 
                getRatingValueForWidgetType(widgetType, typedId);
        });
        try {
            $.post(url, data);
        } catch (e) {
            // TODO: Error handling
        }
        if (typeof window.RECS_onRatingsBarChange == "function") {
            window.RECS_onRatingsBarChange(itemId);
        }
    };

    var starsOnMouseClickHandler = function (starObj, itemId, type, rating, refTagSuffix) {
        var typedId = getTypedId(itemId, type);
        savedState.starRating[typedId] = parseInt(rating,10);
        updateStars(typedId);
        var updatedWidgetTypes = [];
        updatedWidgetTypes.push('starRating');
        refTagSuffix = widgetTypeToRefTagKey['starRating'] + '_' + refTagSuffix;
        if (   savedState.starRating[typedId] > 0
            && savedState.isNotInterested[typedId] > 0) {
            savedState.isNotInterested[typedId] = 0;
            updateCheckbox('isNotInterested', typedId);
            updatedWidgetTypes.push('isNotInterested');
        }
        window.setTimeout(function() {
            submitRating(itemId, type, updatedWidgetTypes, refTagSuffix);
            updateMessage(typedId, 
                '<span style="color: #009900">'+
                 $.fn.amazonRatingsInterface.ratingMessages['ratings-saved']+'</span>');
        }, delayTime);
    };

    var updateMessage = function (typedId, msg) {
        $('#messages_'+typedId, ratingsUIRoot[typedId]).html(msg);
    };

    var updateStarMessages = function (typedId, rating, isMouseOver) {
        if (typeof rating == 'undefined') {
            rating = savedState.starRating[typedId] || 0;
        }
        if (!isSaved[typedId]) {
            var msg;
            if (!isMouseOver) {
                msg = $.fn.amazonRatingsInterface.ratingMessages[savedState.neutralMessage[typedId] || 0];
            }
            else {
                msg = $.fn.amazonRatingsInterface.starRatings[rating];
            }
            updateMessage(typedId, msg);
        }
        else {
            updateMessage(typedId, '<span style="color: #009900">'+
                                 $.fn.amazonRatingsInterface.ratingMessages['ratings-saved']+'</span>');
        }
    };

    var updateStars = function (typedId, rating) {
        if (typeof rating == 'undefined') {
            rating = savedState.starRating[typedId];
        }
        rating = rating || 0;
        if (rating == starMouseOverState[typedId]) return;
        if (typeof starMouseOverState[typedId] == 'undefined' || starMouseOverState[typedId] < 0) {
            $('.arui_starRating', ratingsUIRoot[typedId]).removeClass("s_blueStar_0_0");
        }
        else if (starMouseOverState[typedId] >= 0) {
            $('.arui_starRating', ratingsUIRoot[typedId]).removeClass("s_blueStar_"+starMouseOverState[typedId]+"_0");
        }
        $('.arui_starRating', ratingsUIRoot[typedId]).addClass("s_blueStar_"+rating+"_0");
        $('.arui_starRating > span', ratingsUIRoot[typedId]).html($.fn.amazonRatingsInterface.starRatings[rating]);
        starMouseOverState[typedId] = rating;
    };

    var starsOnMouseOverHandler = function (starObj, typedId, index, refTagSuffix) {
        if (starTwinkler[typedId] != 0) {
            window.clearTimeout(starTwinkler[typedId]);
            starTwinkler[typedId] = 0;
        }
        if (msgTwinkler[typedId] != 0) {
            window.clearTimeout(msgTwinkler[typedId]);
            msgTwinkler[typedId] = 0;
        }
        updateStars(typedId, index);
        updateStarMessages(typedId, index, true);
        isSaved[typedId] = 0;
    };
    
    var starsOnMouseOutHandler = function (starObj, typedId, index, refTagSuffix) {
        starTwinkler[typedId] = window.setTimeout(function() {
            updateStars(typedId);
        }, delayTime);
        msgTwinkler[typedId] = window.setTimeout(function() {
            updateStarMessages(typedId);
        }, delayTime);
    };
    
    var updateCheckbox = function (checkboxType, typedId, newState) {
        if (typeof newState == 'undefined') {
            newState = savedState[checkboxType][typedId] || 0;
        }
        if (newState == 1) {
            $("#arui_checkboxImage_"+checkboxType+"_"+typedId, ratingsUIRoot[typedId])
                .removeClass('s_checkHover')
                .removeClass('s_checkUnmarked')
                .addClass('s_checkMarked');
        }
        else {
            $("#arui_checkboxImage_"+checkboxType+"_"+typedId, ratingsUIRoot[typedId])
                .removeClass('s_checkHover')
                .removeClass('s_checkMarked')
                .addClass('s_checkUnmarked');
        }
    };
    
    var checkboxOnMouseClickHandler = function (checkboxObj, checkboxType, itemId, type, refTagSuffix) {
        var typedId = getTypedId(itemId, type);

        savedState[checkboxType][typedId] = savedState[checkboxType][typedId] ? 0 : 1;
        var updatedWidgetTypes = [];
        updatedWidgetTypes.push(checkboxType);
        refTagSuffix = widgetTypeToRefTagKey[checkboxType] + '_' + refTagSuffix;
        updateCheckbox(checkboxType, typedId);
        if (checkboxType == 'isOwned') {
            if (savedState.isNotInterested[typedId] > 0) {
                savedState.isNotInterested[typedId] = 0;
                updateCheckbox('isNotInterested', typedId);
                updatedWidgetTypes.push('isNotInterested');
            }
        }
        else if (checkboxType == 'isNotInterested') {
            if (savedState.starRating[typedId] > 0) {
                savedState.starRating[typedId] = 0;
                updateStars(typedId);
                updatedWidgetTypes.push('starRating');
            }
            if (savedState.isOwned[typedId] == 1) {
                savedState.isOwned[typedId] = 0;
                updateCheckbox('isOwned', typedId);
                updatedWidgetTypes.push('isOwned');
            }
        }
        window.setTimeout(function() {
            submitRating(itemId, type, updatedWidgetTypes, refTagSuffix);
            updateMessage(typedId, 
                '<span style="color: #009900">'+
                 $.fn.amazonRatingsInterface.ratingMessages['ratings-saved']+'</span>');
        }, delayTime);
    };
    
    var checkboxOnMouseOverHandler = function (checkboxObj, checkboxType, typedId, refTagSuffix) {
        if (!savedState[checkboxType][typedId]) {
            $("#arui_checkboxImage_"+checkboxType+"_"+typedId, ratingsUIRoot[typedId])
                .removeClass('s_checkUnmarked')
                .addClass('s_checkHover');
        }
    };
    
    var checkboxOnMouseOutHandler = function (checkboxObj, checkboxType, typedId, refTagSuffix) {
        if (!savedState[checkboxType][typedId]) {
            $("#arui_checkboxImage_"+checkboxType+"_"+typedId, ratingsUIRoot[typedId])
                .removeClass('s_checkHover')
                .addClass('s_checkUnmarked');
        }
    };
    
    var swapContent = function (ratingsUI) {
        $('.arui_loading', ratingsUI).hide();
        $('.arui_content', ratingsUI).show();
    };
    
    var renderMessages = function (ratingsUI, key, typedId, refTagSuffix) {
        ratingsUI.find(".arui_message").attr('id', 'messages_'+typedId).empty();
        window.setTimeout(function() {
            updateStarMessages(typedId);
        }, delayTime);
    };
    
    var renderCheckbox = function (ratingsUI, key, itemId, type, refTagSuffix) {
        var typedId = getTypedId(itemId, type);

        $.each(['isNotInterested',
                'isOwned',
                'isExcluded',
                'isExcludedClickstream',
                'isGift'], function(i, checkboxType) {
            var checkboxId = checkboxType+'_'+typedId;
            var checkboxLabel = $.fn.amazonRatingsInterface.checkboxLabels[checkboxType];
            var checkboxClickableImageHTML = 
                '<span class="swSprite s_checkUnmarked arui_checkboxImage" \
                       id="arui_checkboxImage_'+checkboxId+'" \
                       tabIndex="0"><span>'+checkboxLabel+'</span></span>';
            var checkboxClickableLabelHTML = 
                '<span class="tiny arui_checkboxLabel" \
                       id="arui_checkboxLabel_'+checkboxId+'">'+checkboxLabel+'</span>';
            var checkboxClickableLabelPlaceholderFound = 
                ratingsUI.find('.arui_'+checkboxType+'_label').empty().html(checkboxClickableLabelHTML).size();
            ratingsUI.find('.arui_'+checkboxType).empty().html(
                checkboxClickableImageHTML + (checkboxClickableLabelPlaceholderFound ? "" : checkboxClickableLabelHTML));
            ratingsUI.find('#arui_checkboxImage_'+checkboxId +","+ '#arui_checkboxLabel_'+checkboxId)
                .focus(function() { checkboxOnMouseOverHandler($(this), checkboxType, typedId, refTagSuffix); })
                .blur(function() { checkboxOnMouseOutHandler($(this), checkboxType, typedId, refTagSuffix); })
                .click(function() { checkboxOnMouseClickHandler($(this), checkboxType, itemId, type, refTagSuffix); return false; })
                .mouseover(function() { checkboxOnMouseOverHandler($(this), checkboxType, typedId, refTagSuffix); }) 
                .mouseout(function() { checkboxOnMouseOutHandler($(this), checkboxType, typedId, refTagSuffix); })
                .keypress(function(e) { if (e.which == 32) { checkboxOnMouseClickHandler($(this), checkboxType, itemId, type, refTagSuffix); } });
            updateCheckbox(checkboxType, typedId);
        });
    };
    
    var renderStars = function (ratingsUI, key, itemId, type, refTagSuffix) {
        var typedId = getTypedId(itemId, type);

        starTwinkler[typedId] = 0;
        msgTwinkler[typedId] = 0;
        // TODO: Don't render the stars twice for the same ASIN, otherwise Safari fails to trigger the events.
        var starsHTML =   '<span class="arui_starRatingWrapper">'
                        +     '<span class="swSprite s_blueClearX arui_clearRating"><span></span></span>'
                        +     '<span class="swSprite s_blueStar_0_0 arui_starRating"><span></span></span>'
                        +     '<span class="arui_starRatingBox_0_0" tabIndex="0"></span>'
                        +     '<span class="arui_starRatingBox_1_0" tabIndex="0"></span>'
                        +     '<span class="arui_starRatingBox_2_0" tabIndex="0"></span>'
                        +     '<span class="arui_starRatingBox_3_0" tabIndex="0"></span>'
                        +     '<span class="arui_starRatingBox_4_0" tabIndex="0"></span>'
                        +     '<span class="arui_starRatingBox_5_0" tabIndex="0"></span>'
                        + '</span>';
        ratingsUI.find(".arui_stars").empty().html(starsHTML)
                 .find("span[class^='arui_starRatingBox']").each(function(i) {
                     $(this).click(function() { starsOnMouseClickHandler($(this), itemId, type, i, refTagSuffix); return false; })
                            .focus(function() { starsOnMouseOverHandler($(this), typedId, i, refTagSuffix); })
                            .blur(function() { starsOnMouseOutHandler($(this), typedId, i, refTagSuffix); })
                            .mouseover(function() { starsOnMouseOverHandler($(this), typedId, i, refTagSuffix); })
                            .mouseout(function() { starsOnMouseOutHandler($(this), typedId, i, refTagSuffix); })
                            .keypress(function(e) { if (e.which == 32) { starsOnMouseClickHandler($(this), itemId, type, i, refTagSuffix); } });
                 });
        updateStars(typedId);
    };
    
    window.isRatingsBarSharedJavascriptLoaded = true;

    function getTypedId (itemId, type) {
        return itemId + "_" + type;
    }      

    amznJQ.declareAvailable('amzn-ratings-bar');
})(jQuery); });
