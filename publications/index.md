---
layout: page
title: Publications
permalink: /publications/
---

<div class="section-list">
  {%- assign publications = site.publications | sort: "date" | reverse -%}
  {%- for publication in publications -%}
    <article class="section-card section-card--wide">
      <p class="card-label">Publication · {{ publication.date | date: "%b %-d, %Y" }}</p>
      <h2><a href="{{ publication.url | relative_url }}">{{ publication.title | escape }}</a></h2>
      <p>{{ publication.summary | default: publication.excerpt | strip_html | strip_newlines }}</p>
    </article>
  {%- endfor -%}
</div>
