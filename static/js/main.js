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
	
	$.Mustache.load('templates.html')
		.done(function() {
			routie({
				'/etusivu': function() {
					$('section').mustache('etusivu', null, { method: 'html' });
				},
				'/rajoitteet': function() {
					$.getJSON('rajoite', function(data) {
						data.slug = function() { return convertToSlug; };
						data.date = function() { return convertToDateStr; };
						$('section').mustache('rajoitteet', data, { method: 'html' });
					});
				},
				'/rajoite/:id/*': function(id) {
					$.getJSON('rajoite/' + id, function(data) {
						data.date = function() { return convertToDateStr; };
						$('section').mustache('rajoite', data, { method: 'html' });
					});
				},
				'/kirjaudu': function() {
					$('section').mustache('kirjaudu', null, { method: 'html' });
				},
				'/rajoita': function() {
					$('section').mustache('teerajoite', null, { method: 'html' });
				},
				'/pasvenska': function() {
					$('section').mustache('pasvenska', null, { method: 'html' });
				},
				'/inenglish': function() {
					$('section').mustache('inenglish', null, { method: 'html' });
				},
				'/404': function() {
					$('section').mustache('404', null, { method: 'html' });
				},
				'*': function() {
					routie('/404');
				// VIRHEEN REITITYS PUUTTUU
				}
			});
		});
})(jQuery);
