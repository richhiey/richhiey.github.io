---
layout: page
title: Publications
permalink: /publications/
show_title: false
---

<div class="section-list">
  {%- assign publications = site.publications | sort: "date" | reverse -%}
  {%- for publication in publications -%}
    <article class="list-card publication-card">
      <div class="list-card__meta publication-card__meta">
        <span>{{ publication.eyebrow | default: "Publication" }}</span>
        <span>{{ publication.date | date: "%b %-d, %Y" }}</span>
      </div>
      <h2><a href="{{ publication.url | relative_url }}">{{ publication.title | escape }}</a></h2>
      <p>{{ publication.summary | default: publication.excerpt | strip_html | strip_newlines }}</p>
      <div class="badge-row">
        {%- if publication.acceptance -%}<span class="badge">{{ publication.acceptance | escape }}</span>{%- endif -%}
        {%- if publication.presentation_type -%}<span class="badge">{{ publication.presentation_type | escape }}</span>{%- endif -%}
        {%- if publication.session -%}<span class="badge">{{ publication.session | escape }}</span>{%- endif -%}
        {%- if publication.abstract_id -%}<span class="badge">{{ publication.abstract_id | escape }}</span>{%- endif -%}
      </div>
    </article>
  {%- endfor -%}
</div>
