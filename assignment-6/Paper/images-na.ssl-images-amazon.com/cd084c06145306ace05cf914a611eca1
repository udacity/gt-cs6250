jsIsLoaded = true;

var doLogging = true;
var loggingEnabled = window.console && window.console.firebug;

function log(value) {
	if (window.console && doLogging) {
		console.log(value);
	}
}

function logObject(obj) {
	if (loggingEnabled && doLogging) {
		console.dir(obj);
	}
}

function logGroup(name) {
	if (loggingEnabled && doLogging) {
		console.groupCollapsed(name);
	}
}

function logGroupEnd() {
	if (loggingEnabled && doLogging) {
		console.groupEnd();
	}
}

/*
 Script specific globals.
 */

// Functions for changing the information displayed. Mapped to specific selector
var INFO_SELECTORS = { 
	"TT_State": [
		function(element) { element.text(ttStrings.disabled); },
		function(element) { element.text(ttStrings.enabled); }
	],
	"TT_action": [
		function(element) {
			log("action set disable");
			element.text(ttStrings.turnOn);
			element.attr("title","enable");
		},
		function(element) {
			log("action set enable");
			element.text(ttStrings.turnOff);
			element.attr("title","disable");
		}
	],
	"TT_Phone": [
		function(element) { element.hide(); },
		function(element) { 
			element.show(); 
		}
	],
	"TT_Edit": [
		function(element) { element.hide(); },
		function(element) { 
			element.show(); 
		}
	],
	"TT_SeeAcct": [
		function(element) { 
			element.show(); 
		},
		function(element) { element.hide(); }
	]
};

var STATE_SELECTORS = {
	"tt_info": [
		function(element) { element.hide(); },
		function(element) { element.show(); }
	],
	"tt_signup": [
		function(element) { element.show(); },
		function(element) { element.hide(); }
	]
};

//==============================================================

/*
 Text Trace Package Level Classes
*/


/**
 * Stores Text Trace data associated with a tracking ID.
 *
 */
function TrackedPackage(trackingId) {
	var phoneDetails = {};
	widgetClass = 'div[id*="ST_' + trackingId + '_"]';
	log("widgetClass:  " + widgetClass);
	this.getPhoneDetails = function () {
		return phoneDetails;
	};
	
	this.isEnabled = null;

	this.updatePhoneDetails = function(newPhoneNumber) {
		logGroup("New Phone Number");
		logObject(newPhoneNumber);
		logGroupEnd();
		phoneDetails = {
			"phoneNumber" : newPhoneNumber.phoneNumber,
			"carrier" : newPhoneNumber.carrier
		};
		log("Updated Phone Details");
	};
	
	var updateElements = function(toUpdate, state) {
		for (var selector in toUpdate) {
			var element = jQuery("." + selector);
			toUpdate[selector][state](element);
		}
	};
	
	this.update = function(isEnabled, isSubscribed, newPhoneNumber) {
		this.updatePhoneDetails(newPhoneNumber);
		
		var phoneSelectors = {
			"phoneNumber": [ function(element) { element.text(newPhoneNumber.phoneNumber); } ]
		};
		
		jQuery(widgetClass).each( function() {
			var widget = jQuery(this);
			widget.find("tr.text_trace_row").fadeOut("fast", function() {
				logGroup("WIDGET INSTANCE");
				log(widget);
				updateElements(INFO_SELECTORS, +isEnabled);
				updateElements(STATE_SELECTORS, +isSubscribed);
				updateElements(phoneSelectors, 0);
				jQuery(this).fadeIn("slow");
				logGroupEnd();
			} );
		} );
		this.isEnabled = isEnabled;
	};
}

function TrackedPackageManager() {
	var twcs = {};
	
	this.getPackage = function(trackingId) {
		logGroup("Get Package Stored for Tracking ID");
		log("Track ID: \n" + trackingId);
		if (trackingId in twcs) {
			logGroupEnd();
			return twcs[trackingId];
		} else {
			var newTWC = new TrackedPackage(trackingId);
			log("created:");
			logObject(newTWC);
			twcs[trackingId] = newTWC;
			logGroupEnd();
			return newTWC;
		}
	};	
}

var myTPMManager = new TrackedPackageManager();

function displayErrorPopover(title, errorMessage, alignTo) {
	var content = "<span id='TT_errorSprite'></span><span id='TT_errorText'>";
	content += errorMessage;
	content += "</span><div class='TT_clear'></div>";
	var popOverSettings = { 
		"showOnHover": false, 
		"literalContent": content,
		"location": alignTo,
		"width": null,
		"title": title
	};

	popover = jQuery.AmazonPopover.displayPopover(popOverSettings);
}

function displayPopover(title, content, getAlignment, params) {
	var popOverSettings = {
		"showOnHover": false,
		"title": title,
		"literalContent": content,
		"location": getAlignment
	};
	jQuery.extend(popOverSettings, params);
	return jQuery.AmazonPopover.displayPopover(popOverSettings);
}

function postData(params, successHandler) {
	jQuery.post(texttraceAjaxURL, params, successHandler, "json");
}

function TextTracePopover(isEnabled, trackingId, type, phoneDetails, getAlignment, postHandler, addParams) {
	
	var action = type;
	if (action == "signup" || action == "edit") {
		type = "settings";
	}
	
	log("Popover saw type: " + type);
	
	var popContent = jQuery(jQuery(".tt_" + type + "_form").get(0)).clone().show();
	popContent.css("display", "inline-block");
	log(popContent);
	
	var inputFields = "[name='phoneNumber'],[name='carrier']";
	logGroup("InputFields");
	popContent.find(inputFields).each( function() {
		var name = jQuery(this).attr("name");
		log(jQuery(this));
		jQuery(this).val(phoneDetails[name]);
	});
	logGroupEnd();
	
	if (isAccountOn) {
		popContent.find("p.applyAllSetting").show();
	} else {
		popContent.find("p.applyAllSetting").hide();
	}
	var descContainer = popContent.find("p.tt_form_dsc");
	if (descContainer) {
		if (isEnabled) {
			descContainer.text(ttStrings.settingsDesc.edit);
		} else {
			descContainer.text(ttStrings.settingsDesc.signup);
		}
	}
	var enableBtn = popContent.find(".tt_enable");
	var saveBtn = popContent.find(".tt_save");
	if (action == "signup") {
		enableBtn.show();
		saveBtn.hide();
	} else if (action == "edit") {
		enableBtn.hide();
		saveBtn.show();
	}
	var popTitle = ttStrings.popoverTitle[type];
	jQuery.extend(addParams, {"showCloseButton": false});
	var popover = displayPopover(popTitle, popContent, getAlignment, addParams);
	
	function submitHandler(event) {
		event.preventDefault();
		logGroup("Handle Submit");
		log(event);
		var jForm = jQuery(this);
		var values = {
			"apply_all": "no",
			"action": action,
			"trackingId": trackingId
		};
		jQuery.each(jForm.serializeArray(), function(i, field) {
			values[field.name] = field.value;
		});
		popover.ajaxError(function() {
			popover.close();
			displayErrorPopover(popTitle, ttStrings.errors.acctpackage, getAlignment);
		});
		postData(values, function(data) { 
			log("Handle Post");
			log(postHandler);
			var handleSuccess = postHandler(data, jForm);
			if (handleSuccess) {
				jForm.unbind("submit");
				popover.close();
			}
		});
		logGroupEnd();
	}
	
	popover.find("form.phoneSettings").bind("submit", submitHandler);
	
	this.getPopover = function() {
		return popover;
	};
}

function ShipTrackWidget(orderId, trackingId) {
	var widget = jQuery("div#ST_" + trackingId + "_" + orderId);
	var trackedPackage = myTPMManager.getPackage(trackingId);

	var signUpControl = widget.find("a.TT_signup");
	var editControl = widget.find("a.TT_Edit");
	var actionControl = widget.find("a.TT_action");
	
	var widgetPosition = {
		"left": widget.offset().left,
		"top": widget.offset().top +widget.outerHeight() + 15
	};
	
	function getWidgetOffset() {
		return widgetPosition;
	}
	
	function unbindAllClickHandlers() {
		try {
			signUpControl.unbind("click");
			editControl.unbind("click");
			actionControl.unbind("click");
		} catch (error) {
			log("unbind error");
			log(error);
		}
	}
	
	function disableInteraction() {
		unbindAllClickHandlers();
		
		var nullClick = function(event) { event.preventDefault(); };
		
		signUpControl.bind("click", nullClick );
		editControl.bind("click", nullClick );
		actionControl.bind("click", nullClick );
	}
	
	function enableInteraction() {
		unbindAllClickHandlers();
		logGroup("enabling click handlers");
		signUpControl.bind("click", settingsClickHandler );
		editControl.bind("click", settingsClickHandler );
		log(actionControl);
		log(actionHandler);
		var a = actionControl.bind("click", actionHandler );
		log(a);
		log("end");
		logGroupEnd();
	}
	this.enableInteraction = enableInteraction;
	
	function handleSettingsPost(data, form) {
		logGroup("Handle Settings");
		log("Handling settings post");
		logGroup("data");
		log(data);
		logObject(data);
		logGroupEnd();
		try {
			log("Inside Try");
			log(form);
			if (data.general.error == "PHONE_ERROR") {
				log("PHONE ERROR ENCOUNTERED");
				var errorMsg = '<div class="message"><div id="TT_errorSprite"></div>' + 
					'<div id="TT_errorText">' + ttStrings.errors.phone + '</div>' + 
					'<div class="TT_clear"></div></div>';
				form.parents(".tt_settings_form").prepend(errorMsg);
				var inputs = form.find("[name='phoneNumber']");
				logGroup("inputs");
				logObject(inputs);
				logGroupEnd();
				inputs.each( function() {
					jQuery(this).css("border", "2px solid #A31919");
				});
				return false;
			}
			 if (data.general.error == "CARRIER_ERROR") {
					log("CARRIER ERROR ENCOUNTERED");
					var errorMsg = '<div class="message"><div id="TT_errorSprite"></div>' +
							'<div id="TT_errorText">' + ttStrings.errors.carrier + '</div>' +
							'<div class="TT_clear"></div></div>';
					form.parents(".tt_settings_form").prepend(errorMsg);
					var inputs = form.find("[name='carrier']");
					logGroup("inputs");
					logObject(inputs);
					logGroupEnd();
					inputs.each( function() {
							jQuery(this).css("border", "2px solid #A31919");
					});
					return false;
			}
		} catch (error) {
			log("Settings Post Error: ");
			log(error);
		}
		logGroupEnd();
		return handleEnablePost(data);
	}
		
	function handleEnablePost(data) {
		logGroup("data");
		log(data);
		logObject(data);
		logGroupEnd();
		var accountReturn = data.account;
		var packageReturn = data["package"];
		var errorKey = "";
		if (accountReturn.result == "SUCCESS") {
			isAccountOn = true;
		} else if (accountReturn.result !== "SKIPPED") {
			errorKey += "acct";
		} else {
			log("Account Skipped");
		}
		if (packageReturn.result == "SUCCESS") {
			logGroup("Return Values");
			logObject(data.values);
			logGroupEnd();
			trackedPackage.update(true, true, data.values);
			return true;
		} else {
			errorKey += "package";
		}
		log("Error key: " + errorKey);
		var settingsString = ttStrings.popoverTitle.settings;
		if (errorKey == "acctpackage") {
			displayErrorPopover(settingsString, ttStrings.errors.acctpackage, getWidgetOffset);
		} else {
			displayErrorPopover(settingsString, ttStrings.errors[data.action][errorKey], getWidgetOffset);
		}
		return true;
	}
	this.handleSettingsPost = handleSettingsPost;
	
	function settingsClickHandler(event) {
		event.preventDefault();
		disableInteraction();
		var phoneDetails = trackedPackage.getPhoneDetails();
		var type = jQuery(this).hasClass("TT_signup") ? "signup" : "edit";
		log("Settings Type: " + type);
		log(handleSettingsPost);
		var popover = new TextTracePopover(
			trackedPackage.isEnabled,
			trackingId, 
			type, 
			phoneDetails, 
			getWidgetOffset,
			handleSettingsPost,
			{ "onHide": enableInteraction }
		);
	}
	this.settingsClickHandler = settingsClickHandler;
	
	function handleDisablePost(data) {
		var errorKey = "";
		if (data.account.result == "SUCCESS") {
			isAccountOn = false;
		} else if ( data.account.result !== "SKIPPED" ) {
			errorKey += "acct";
		}
		if (data["package"].result == "SUCCESS") {
			trackedPackage.update(false, isAccountOn, data.values);
			return true;
		} else {
			errorKey += "package";
		}
		var settingsString = ttStrings.popoverTitle.disable;
		log("Error Key:  " + errorKey);
		if (errorKey == "acctpackage") {
			displayErrorPopover(settingsString, ttStrings.errors.acctpackage, getWidgetOffset);
		} else {
			displayErrorPopover(settingsString, ttStrings.errors[data.action][errorKey], getWidgetOffset);
		}
		return true;
	}
	
	function actionHandler(event) {
		event.preventDefault();
		disableInteraction();
		log("Action Handler");
		var action = jQuery(this).attr("title");
		var phoneDetails = trackedPackage.getPhoneDetails();
		if (action == "enable") {
			// DO ENABLE
			log("DO 1-Click ENABLE");
			var postParams = { "action": "signup", "trackingId": trackingId};
			jQuery.extend(postParams, phoneDetails);
			logObject(postParams);
			postData(postParams, function(data) {
				handleEnablePost(data);
				enableInteraction();
			});
		} else if (action == "disable") {
			//DO DISABLE
			log("Disable");
			var popover = new TextTracePopover(
				null,
				trackingId, 
				"disable", 
				phoneDetails, 
				getWidgetOffset, 
				handleDisablePost,
				{ "onHide": enableInteraction }
			);
		}
	}	
}

