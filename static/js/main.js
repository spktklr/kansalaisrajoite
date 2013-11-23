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
	
	$.Mustache.load('templates.html')
		.done(function() {
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
				'/kirjaudu': function() {
					show('section', 'kirjaudu');
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
			
			// load login box
			$.getJSON('kayttaja', function(data) {
				data.isLogged = (data.name !== undefined);
				show('header div', 'kirjautumislaatikko', data);
				
				// login form submit handler
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
							},
							401: function() {
								// todo: tell user about invalid input
							}
						}
					});
				});
				
				// logout button click handler
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
