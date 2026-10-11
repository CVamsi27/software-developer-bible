---
layout: null
---
/* The rendered site, rather than the source corpus, owns publication availability. */
window.StudyPublishedPaths = [
{% for item in site.pages %}{% if item.url contains '.html' %}{{ item.url | relative_url | jsonify }},{% endif %}{% endfor %}
];
