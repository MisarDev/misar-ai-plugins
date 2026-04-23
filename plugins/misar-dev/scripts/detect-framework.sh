#!/bin/bash
# Misar Website Auditor — Framework Detection Script
# Detects the web framework, package manager, and dev port in the current directory.
# Output: JSON string

FRAMEWORK="unknown"
PKG_MANAGER="npm"
DEV_PORT="3000"

# Package manager detection
[ -f "pnpm-lock.yaml" ] && PKG_MANAGER="pnpm"
[ -f "yarn.lock" ] && PKG_MANAGER="yarn"
[ -f "bun.lockb" ] && PKG_MANAGER="bun"

# Framework detection (priority order — most specific first)
if [ -f "next.config.js" ] || [ -f "next.config.ts" ] || [ -f "next.config.mjs" ]; then
  FRAMEWORK="nextjs"
  DEV_PORT="3000"
elif [ -f "nuxt.config.ts" ] || [ -f "nuxt.config.js" ]; then
  FRAMEWORK="nuxt"
  DEV_PORT="3000"
elif [ -f "astro.config.mjs" ] || [ -f "astro.config.ts" ]; then
  FRAMEWORK="astro"
  DEV_PORT="4321"
elif [ -f "svelte.config.js" ]; then
  FRAMEWORK="sveltekit"
  DEV_PORT="5173"
elif [ -f "angular.json" ]; then
  FRAMEWORK="angular"
  DEV_PORT="4200"
elif [ -f "gatsby-config.js" ] || [ -f "gatsby-config.ts" ]; then
  FRAMEWORK="gatsby"
  DEV_PORT="8000"
elif [ -f "remix.config.js" ] || [ -f "remix.config.ts" ]; then
  FRAMEWORK="remix"
  DEV_PORT="3000"
elif [ -f "vite.config.ts" ] || [ -f "vite.config.js" ]; then
  FRAMEWORK="vite"
  DEV_PORT="5173"
elif [ -f "index.html" ]; then
  FRAMEWORK="static-html"
  DEV_PORT="none"
fi

echo "{\"framework\":\"$FRAMEWORK\",\"package_manager\":\"$PKG_MANAGER\",\"dev_port\":\"$DEV_PORT\"}"
