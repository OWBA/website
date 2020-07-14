<?php
$URLs = array(
{%- for x in this.redirects.blocks %}
  '{{ x.slug }}' => {% if not "'" in x.redirect.ascii_url -%}
		'{{ x.redirect }}'
	{%- elif not '"' in x.redirect.ascii_url -%}
		"{{ x.redirect }}"
	{%- else -%}
		'{{ x.redirect.ascii_url.replace("'", "\\'") }}'
	{%- endif %},
{%- endfor %}
);

$url = $URLs[$_GET['to']];
if (isset($url)) { header("Location: $url", true, 302); }
else { print('unknown'); }
exit;
?>
