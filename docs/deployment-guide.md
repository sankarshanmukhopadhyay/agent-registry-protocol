---
layout: default
title: "Deployment Guide"
nav_exclude: true
---

# Deployment Guide

A production deployment should separate authoritative writes, projections, policy evaluation, evidence storage and appeal administration. Publish service objectives for query availability, status freshness, event latency, revocation propagation, incident acknowledgement and point-in-time reconstruction.

Use least privilege for registry administration. Protect signing keys independently from application credentials. Maintain tested runbooks for compromise, false registration, unauthorized control change, stale projection, event delivery failure, revocation, federation conflict and restoration.
