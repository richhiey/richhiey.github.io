---
layout: page
title: Projects
permalink: /projects/
---

<div class="section-list">
  {%- assign projects = site.projects | sort: "date" | reverse -%}
  {%- for project in projects -%}
    <article class="section-card section-card--wide">
      <p class="card-label">Project · {{ project.date | date: "%b %-d, %Y" }}</p>
      <h2><a href="{{ project.url | relative_url }}">{{ project.title | escape }}</a></h2>
      <p>{{ project.summary | default: project.excerpt | strip_html | strip_newlines }}</p>
    </article>
  {%- endfor -%}
</div>
