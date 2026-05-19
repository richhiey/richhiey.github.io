---
layout: page
title: Projects
permalink: /projects/
show_title: false
---

<div class="section-list">
  {%- assign projects = site.projects | sort: "date" | reverse -%}
  {%- for project in projects -%}
    <article class="list-card">
      <div class="list-card__meta">
        <span>Project</span>
        <span>{{ project.date | date: "%b %-d, %Y" }}</span>
      </div>
      <h2><a href="{{ project.url | relative_url }}">{{ project.title | escape }}</a></h2>
      <p>{{ project.summary | default: project.excerpt | strip_html | strip_newlines }}</p>
    </article>
  {%- endfor -%}
</div>
