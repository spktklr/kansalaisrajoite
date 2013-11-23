(function ($) {
	var convertToSlug = function(text, render) {
		return render(text)
		.toLowerCase()
		.replace(/[^\w ]+/g, '')
		.replace(/ +/g, '-');
	}
	
	var convertToDateStr = function(text, render) {
		var timestamp = parseInt(render(text))*1000;
		return new Date(timestamp).toLocaleDateString();
	}
	
	var percentCompleted = function(text, render) {
		var threshold = 5;
		return ((Math.min(parseInt(render(text)), threshold) / threshold) * 100);
	}
	
	var show = function(element, template, data) {
		$(element).mustache(template, (data === undefined ? null : data), { method: 'html' });
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
	/* modal event handlers end */

	/* login event handlers */
	$(document).on('submit', 'form.kirjautuminen', function(e) {
		e.preventDefault();
		
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
					data.isLogged = (data.name !== undefined);
					show('header div', 'kirjautumislaatikko', data);
					jQuery(document).trigger('close.facebox');
				},
				401: function() {
					// todo: tell user about invalid input
				}
			}
		});
	});
	
	$(document).on('click', 'a.ulos', function() {
		$.ajax({
			url: 'kayttaja/logout',
			type: 'POST',
			success: function() {
				location.reload();
			}
		});
		
		return false;
	});
	/* login event handlers end */
	
	// load templates
	$.Mustache.load('templates.html')
		.done(function() {
			// setup routing
			routie({
				'': function() {
					// default to the front page
					show('section', 'etusivu');
				},
				'/etusivu': function() {
					show('section', 'etusivu');
				},
				'/rajoitteet': function() {
					$.getJSON('rajoite', function(data) {
						data.slug = function() { return convertToSlug; };
						data.date = function() { return convertToDateStr; };
						data.percentCompleted = function() { return percentCompleted; };
						show('section', 'rajoitteet', data);
					});
				},
				'/rajoite/:id/*': function(id) {
					$.getJSON('rajoite/' + id, function(data) {
						data.date = function() { return convertToDateStr; };
						show('section', 'rajoite', data);
					});
				},
				'/rajoita': function() {
					show('section', 'teerajoite');
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
				'*': function() {
					// show 404 page for other urls
					show('section', '404');
				}
			});
			
			// load and display login status
			$.getJSON('kayttaja', function(data) {
				data.isLogged = (data.name !== undefined);
				show('header div', 'kirjautumislaatikko', data);
			});
			
			// catch all ajax errors and show error page
			$(document).ajaxError(function(event, request, settings) {
				if (request.status === 401) {
					show('section', 'kirjaudu');
				} else {
					show('section', 'virhe');
				}
			});
		});
})(jQuery);
