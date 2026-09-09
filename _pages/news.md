---
layout: page
title: news
permalink: /news/
nav: true
nav_order: 2
_styles: |
  .news table th {
    width: auto !important;
    min-width: 7.5rem;
    white-space: nowrap;
    vertical-align: top;
  }

  .news table td img {
    display: block;
    width: 100%;
    max-width: 480px;
    height: auto;
    margin-top: 0.75rem;
  }

  @media (max-width: 576px) {
    .news table th {
      min-width: 6.5rem;
    }

    .news table td img {
      max-width: 100%;
    }
  }
---

{% include news.liquid %}
