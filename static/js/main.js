(function ($) {
	var defaultLocale = 'fi-Fi';
	
	// user information
	var user = {
		isLogged: false,
		info: null,
		setLoggedIn: function(info) {
			this.isLogged = true;
			this.info = info;
		},
		setLoggedOut: function() {
			this.isLogged = false;
			this.info = null;
		}
	};
	
	var slugFunc = function(text) {
		// \u00E4 = ä
		// \u00F6 = ö
		return text
		.toLowerCase()
		.replace(/[^\w\u00E4\u00F6 ]+/g, '')
		.replace(/ +/g, '-');
	}
	
	var convertToSlug = function(text, render) {
		return slugFunc(render(text));
	}
	
	var convertToDateStr = function(text, render) {
		var timestamp = parseInt(render(text))*1000;
		return new Date(timestamp).toLocaleDateString(defaultLocale);
	}
	
	var percentCompleted = function(text, render) {
		var threshold = 101;
		return ((Math.min(parseInt(render(text)), threshold) / threshold) * 100);
	}
	
	var show = function(element, template, data) {
		$(element).mustache(template, (data === undefined ? null : data), { method: 'html' });
	}
	
	var scrollTo = function(element) {
		$(element)[0].scrollIntoView();
	}
	
	/* modal event handlers start */
	$(document).on('click', '#kirjaudu', function() {
		jQuery.facebox({ ajax: 'kirjaudu.html' });
		return false;
	});

	$(document).on('click', '#rekisteroidy', function() {
		jQuery.facebox({ ajax: 'rekisteroidy.html' });
		return false;
	});

	$(document).on('click', '#loginregister', function() {
		jQuery.facebox({ ajax: 'rekisteroidy.html' });
		return false;
	});

	$(document).on('click', '#registerlogin', function() {
		jQuery.facebox({ ajax: 'kirjaudu.html' });
		return false;
	});

	$(document).on('click', '#ota-yhteytta', function() {
		jQuery.facebox({ ajax: 'otayhteytta.html' });
		return false;
	});	

	$(document).on('click', '#forgotpassword', function() {
		jQuery.facebox({ ajax: 'salasana_unohtui.html' });
		return false;
	});	
	/* modal event handlers end */

	/* login event handlers */
	$(document).on('submit', 'form.kirjautuminen', function(e) {
		e.preventDefault();
		$('div.reglog p.alert').hide();
		
		$.ajax({
			url: 'kayttaja/login',
			global: false,
			data: {
				email: $('form.kirjautuminen input[name=email]').val(),
				password: $('form.kirjautuminen input[name=password]').val()
			},
			type: 'POST',
			statusCode: {
				200: function(data) {
					user.setLoggedIn(data);
					show('header', 'headerbox', user);
					jQuery(document).trigger('close.facebox');
					routie.reload();
				},
				400: function() {
					$('div.reglog p.alert').show('fast');
				},
				401: function() {
					$('div.reglog p.alert').show('fast');
				}
			}
		});
	});
	
	$(document).on('click', 'a.ulos', function() {
		$.ajax({
			url: 'kayttaja/logout',
			type: 'POST',
			success: function() {
				user.setLoggedOut();
				show('header', 'headerbox', user);
				routie.reload();
			}
		});
		
		return false;
	});
	/* login event handlers end */
	
	// registration event handlers
	$(document).on('submit', 'form.rekisteroityminen', function(e) {
		var name = $('form.rekisteroityminen input[name=name]').val(),
			city = $('form.rekisteroityminen input[name=city]').val(),
			email = $('form.rekisteroityminen input[name=email]').val(),
			pass1 = $('form.rekisteroityminen input[name=password1]').val(),
			pass2 = $('form.rekisteroityminen input[name=password2]').val();
		
		e.preventDefault();
		$('div.reglog p.alert').hide();
		
		// quick form validation
		if (pass1 !== pass2) {
			$('div.reglog p.alert.error-pwmismatch').show('fast');
			return;
		}
		
		if (pass1.length < 8) {
			$('div.reglog p.alert.error-pwlength').show('fast');
			return;
		}
		
		// bwhahahahahaha
		if (pass1 === 'kansalaisrajoite' || pass1 === 'salasana' || pass1 === 'password') {
			$('div.reglog p.alert.error-pwsimple').show('fast');
			return;
		}
		
		$.ajax({
			url: 'kayttaja/rekisteroidy',
			global: false,
			data: {
				email: email,
				password: pass1,
				name: name,
				city: city,
			},
			type: 'POST',
			statusCode: {
				200: function(data) {
					user.setLoggedIn(data);
					show('header', 'headerbox', user);
					jQuery(document).trigger('close.facebox');
					routie.reload();
				},
				400: function() {
					$('div.reglog p.alert.error-badrequest').show('fast');
				},
				409: function() {
					$('div.reglog p.alert.error-conflict').show('fast');
				}
			}
		});
	});
	
	/* restriction view click handlers */
	$(document).on('click', 'input[name="kannata"]', function() {
		$.ajax({
			url: 'kannatus/' + $(this).data('restriction-id'),
			type: 'POST',
			success: function() {
				routie.reload();
			}
		});
	});
	
	$(document).on('click', 'input[name="peruuta"]', function() {
		$.ajax({
			url: 'kannatus/' + $(this).data('restriction-id'),
			type: 'DELETE',
			success: function() {
				routie.reload();
			}
		});
	});
	
	$(document).on('click', 'input[name="vahvista"]', function() {
		$.ajax({
			url: 'rajoite/' + $(this).data('restriction-id') + '/vahvista',
			type: 'POST',
			success: function() {
				routie.reload();
			}
		});
	});
	
	$(document).on('click', 'input[name="poista"]', function() {
		$.ajax({
			url: 'rajoite/' + $(this).data('restriction-id'),
			type: 'DELETE',
			success: function() {
				routie('/rajoitteet');
			}
		});
	});
	/* restriction view click handlers end */
	
	// new restriction submit button click handler
	$(document).on('submit', 'form.teerajoite', function(e) {
		e.preventDefault();
		
		$.ajax({
			url: 'rajoite',
			global: false,
			data: {
				title: $('form.teerajoite input[name=title]').val(),
				body: $('form.teerajoite textarea[name=body]').val()
			},
			type: 'POST',
			statusCode: {
				200: function(data) {
					routie('/rajoite/' + data.id + '/' + slugFunc(data.title));
				},
				401: function() {
					// todo: tell user about invalid input
				}
			}
		});
	});
	
	/* content functions */
	var showRestrictions = function(data, order) {
		// sort functions
		var sort = {
			byAge: function(a, b) { return a.created < b.created },
			byVotes: function(a, b) { return a.votes < b.votes },
			byTitle: function(a, b) { return a.title.localeCompare(b.title, defaultLocale); }
		}
		
		switch(order) {
		case 'aika':
		default:
			data.restrictions.sort(sort.byAge);
			data.sort = {
				byAge: true,
				byAgeDesc: true
			}
			break;
		case '-aika':
			data.restrictions.sort(sort.byAge).reverse();
			data.sort = {
				byAge: true
			}
			break;
		case 'aanet':
			data.restrictions.sort(sort.byVotes);
			data.sort = {
				byVotes: true,
				byVotesDesc: true
			}
			break;
		case '-aanet':
			data.restrictions.sort(sort.byVotes).reverse();
			data.sort = {
				byVotes: true
			}
			break;
		case 'otsikko':
			data.restrictions.sort(sort.byTitle);
			data.sort = {
				byTitle: true,
				byTitleDesc: true
			}
			break;
		case '-otsikko':
			data.restrictions.sort(sort.byTitle).reverse();
			data.sort = {
				byTitle: true
			}
			break;
		}
		
		data.slug = function() { return convertToSlug; };
		data.date = function() { return convertToDateStr; };
		data.percentCompleted = function() { return percentCompleted; };
		
		show('section', 'rajoitteet', data);
	}
	/* content functions end */
	
	// load templates
	$.Mustache.load('templates.html')
		.done(function() {
			// catch all ajax errors and show error page
			$(document).ajaxError(function(event, request, settings) {
				switch (request.status) {
				case 401:
					show('section', 'error-login');
					break;
				case 403:
					show('section', 'error-unauthorized');
					break;
				case 404:
					show('section', 'error-notfound');
					break;
				default:
					show('section', 'error-generic');
					break;
				}
			});
			
			// load and display login status
			$.getJSON('kayttaja', function(data) {
				if (data.name !== undefined) {
					user.setLoggedIn(data);
				} else {
					user.setLoggedOut();
				}
				
				show('header', 'headerbox', user);
				
				// setup routing
				routie({
					'': function() {
						// default to the front page
						show('section', 'etusivu');
					},
					'/etusivu': function() {
						show('section', 'etusivu');
					},
					'/rajoitteet/:order?': function(order) {
						$.getJSON('rajoite', function(data) {
							showRestrictions(data, order);
						});
					},
					'/rajoite/:id/:slug?': function(id, slug) {
						$.getJSON('rajoite/' + id, function(data) {
							data.date = function() { return convertToDateStr; };
							data.isAdmin = (user.info ? user.info.admin : false);
							show('section', 'rajoite', data);
						});
					},
					'/rajoita': function() {
						if (user.isLogged) {
							show('section', 'teerajoite');
						} else {
							show('section', 'error-login');
						}
					},
					'/ohjeet/:anchor?': function(anchor) {
						show('section', 'ohjeet');
						if (anchor) {
							scrollTo('#' + anchor);
						}
					},
					'/tiedotteet': function() {
						$.getJSON('tiedote', function(data) {
							data.hasNews = (data.news.length > 0);
							data.date = function() { return convertToDateStr; };
							show('section', 'tiedotteet', data);
						});
					},
					'/pasvenska': function() {
						show('section', 'pasvenska');
					},
					'/inenglish': function() {
						show('section', 'inenglish');
					},
					'/ota-yhteytta': function() {
						show('section', 'ota-yhteytta');
					},
					'/rekisteriseloste': function() {
						show('section', 'rekisteriseloste');
					},
					'/henkilosuoja': function() {
						show('section', 'henkilosuoja');
					},
					'*': function() {
						// show 404 page for other urls
						show('section', 'error-notfound');
					}
				});
			});
		});
})(jQuery);
