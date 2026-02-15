#!/usr/bin/env node

const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const START_URL =
  process.argv[2] ||
  "https://app.klingai.com/global/dev/document-api/quickStart/productIntroduction/overview";
const LANG = process.argv.includes("--zh") ? "zh" : "en";
const SKILL_ROOT = path.resolve(__dirname, "..");
const REFERENCES_DIR = path.join(SKILL_ROOT, "references");
const PAGES_DIR = path.join(REFERENCES_DIR, "pages");
const API_DIR = path.join(REFERENCES_DIR, "api");

async function fetchText(url) {
  const res = await fetch(url, {
    headers: {
      "user-agent": "Mozilla/5.0 (Codex Kling Docs Skill Builder)",
      accept: "text/html,application/javascript,*/*",
    },
  });
  if (!res.ok) {
    throw new Error(`HTTP ${res.status} for ${url}`);
  }
  return await res.text();
}

function decodeJsSingleQuotedLiteral(raw) {
  // Decode JS escape sequences using a template literal parser.
  const expr = "`" + raw.replace(/`/g, "\\`").replace(/\$\{/g, "\\${") + "`";
  return vm.runInNewContext(expr);
}

function stripTags(html) {
  return html
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&#39;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/\s+/g, " ")
    .trim();
}

function prettyHtml(html) {
  return html
    .replace(/></g, ">\n<")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function collectStringLiterals(source) {
  const literals = [];
  const single = /'((?:\\.|[^'\\])*)'/g;
  const double = /"((?:\\.|[^"\\])*)"/g;

  let m;
  while ((m = single.exec(source)) !== null) {
    try {
      literals.push(decodeJsSingleQuotedLiteral(m[1]));
    } catch {
      // ignore malformed escape sequences
    }
  }
  while ((m = double.exec(source)) !== null) {
    try {
      literals.push(decodeJsSingleQuotedLiteral(m[1]));
    } catch {
      // ignore malformed escape sequences
    }
  }
  return literals;
}

function isUsefulLiteral(s) {
  if (!s) return false;
  const text = s.trim();
  if (text.length < 2) return false;
  if (text.length > 12000) return false;
  if (!/[A-Za-z]/.test(text) && !/[\u4e00-\u9fff]/.test(text)) return false;
  if (/^\.\/[A-Za-z0-9._/-]+$/.test(text)) return false;
  if (/^(https?:\/\/)?[A-Za-z0-9._/-]+$/.test(text) && !text.includes(" ")) return false;
  if (/^(true|false|null|undefined|module|default|__name|setup)$/.test(text)) return false;
  return true;
}

function uniquePreserveOrder(list) {
  const seen = new Set();
  const out = [];
  for (const item of list) {
    if (seen.has(item)) continue;
    seen.add(item);
    out.push(item);
  }
  return out;
}

function slugToRoute(slug) {
  return `/global/dev/document-api/${slug}`;
}

async function main() {
  fs.mkdirSync(PAGES_DIR, { recursive: true });
  fs.mkdirSync(API_DIR, { recursive: true });

  const landingHtml = await fetchText(START_URL);
  const indexMatch = landingHtml.match(
    /<script[^>]*type="module"[^>]*src="(https:\/\/[^"']+\/api-doc\/assets\/index-[^"']+\.js)"/
  );

  if (!indexMatch) {
    throw new Error("Could not locate index JS bundle URL from KLING docs landing page");
  }

  const indexJsUrl = indexMatch[1];
  const assetsBase = indexJsUrl.replace(/\/index-[^/]+\.js$/, "");
  const indexJs = await fetchText(indexJsUrl);

  const docsChunkCandidates = [
    ...new Set(
      [...indexJs.matchAll(/\.\/(Index-[A-Za-z0-9_-]+\.js)/g)].map((m) => m[1])
    ),
  ];

  if (!docsChunkCandidates.length) {
    throw new Error("Could not locate docs chunk from KLING main index bundle");
  }

  let docsChunkUrl = "";
  let docsBundleJs = "";
  for (const candidate of docsChunkCandidates) {
    const url = `${assetsBase}/${candidate}`;
    const content = await fetchText(url);
    if (content.includes("/src/docs/")) {
      docsChunkUrl = url;
      docsBundleJs = content;
      break;
    }
  }

  if (!docsBundleJs) {
    throw new Error("Could not find docs route map in any Index-*.js chunk");
  }

  const mapRegex = /"\/(src\/docs\/[^"]+?)\/(en|zh)\.md"\s*:\(\)=>[\s\S]*?import\("\.\/([^"]+?\.js)"\)/g;
  const entries = [];
  let m;
  while ((m = mapRegex.exec(docsBundleJs)) !== null) {
    entries.push({ srcBase: m[1], lang: m[2], chunk: m[3] });
  }

  if (!entries.length) {
    throw new Error("No docs entries found in KLING docs route map chunk");
  }

  let openApiChunkUrl = "";
  let openApiEntries = [];
  const openApiChunkMatch = docsBundleJs.match(/\.\/(OpenApi-[A-Za-z0-9_-]+\.js)/);
  if (openApiChunkMatch) {
    openApiChunkUrl = `${assetsBase}/${openApiChunkMatch[1]}`;
    const openApiChunkJs = await fetchText(openApiChunkUrl);
    const openApiMapRegex =
      /"\/(src\/docs\/[^"]+?)\/api\.ts"\s*:\(\)=>[\s\S]*?import\("\.\/([^"]+?\.js)"\)/g;
    let mApi;
    while ((mApi = openApiMapRegex.exec(openApiChunkJs)) !== null) {
      const srcBase = mApi[1];
      openApiEntries.push({
        srcBase,
        slug: srcBase.replace(/^src\/docs\//, ""),
        chunk: mApi[2],
      });
    }
    openApiEntries = openApiEntries.sort((a, b) => a.slug.localeCompare(b.slug));
  }

  const selected = entries
    .filter((e) => e.lang === LANG)
    .map((e) => {
      const slug = e.srcBase.replace(/^src\/docs\//, "");
      return {
        ...e,
        slug,
        route: slugToRoute(slug),
        sourceMarkdownPath: `/${e.srcBase}/${e.lang}.md`,
      };
    })
    .sort((a, b) => a.slug.localeCompare(b.slug));

  const generated = [];

  for (const doc of selected) {
    const chunkUrl = `${assetsBase}/${doc.chunk}`;
    const chunkJs = await fetchText(chunkUrl);

    const literalRegex = /'((?:\\.|[^'\\])*)'/g;
    let literal;
    let bestHtml = "";
    while ((literal = literalRegex.exec(chunkJs)) !== null) {
      const raw = literal[1];
      if (!raw.includes("<h1") && !raw.includes("<h2") && !raw.includes("<p")) {
        continue;
      }
      let decoded = "";
      try {
        decoded = decodeJsSingleQuotedLiteral(raw);
      } catch {
        continue;
      }
      if (decoded.includes("<h1") && decoded.length > bestHtml.length) {
        bestHtml = decoded;
      }
    }

    const titleMatch = bestHtml.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
    const h1FromVNode =
      chunkJs.match(/id:"[^"]+",tabindex:"-1"}\s*,\s*"([^"]+)"\s*,\s*-1/) ||
      chunkJs.match(/id:'[^']+',tabindex:'-1'}\s*,\s*'([^']+)'\s*,\s*-1/);
    const title = titleMatch
      ? stripTags(titleMatch[1])
      : h1FromVNode
      ? h1FromVNode[1]
      : doc.slug;

    const pretty = prettyHtml(bestHtml);
    const text = bestHtml ? stripTags(bestHtml) : "";

    const endpoints = uniquePreserveOrder(
      [...chunkJs.matchAll(/endpoint:"([^"]+)"/g)]
        .map((m) => m[1])
        .concat([...chunkJs.matchAll(/endpoint:'([^']+)'/g)].map((m) => m[1]))
    );
    const extractedStrings = uniquePreserveOrder(
      collectStringLiterals(chunkJs).filter(isUsefulLiteral)
    ).slice(0, 300);

    const pageFile = `${doc.slug.replace(/\//g, "__")}.md`;
    const pagePath = path.join(PAGES_DIR, pageFile);

    const content = [
      `# ${title}`,
      "",
      `- Route: \`${doc.route}\``,
      `- Source markdown path: \`${doc.sourceMarkdownPath}\``,
      `- Source chunk: \`${chunkUrl}\``,
      "",
      ...(bestHtml
        ? [
            "## Content (HTML)",
            "",
            pretty,
            "",
            "## Plain Text Snapshot",
            "",
            text,
            "",
          ]
        : []),
      ...(endpoints.length
        ? [
            "## API Endpoints Referenced",
            "",
            ...endpoints.map((e) => `- \`${e}\``),
            "",
          ]
        : []),
      ...(extractedStrings.length
        ? [
            "## Extracted String Literals",
            "",
            "```text",
            extractedStrings.join("\n"),
            "```",
            "",
          ]
        : []),
      "## Raw Chunk Source",
      "",
      "```javascript",
      chunkJs,
      "```",
      "",
    ].join("\n");

    fs.writeFileSync(pagePath, content, "utf8");
    generated.push({
      title,
      slug: doc.slug,
      route: doc.route,
      sourceMarkdownPath: doc.sourceMarkdownPath,
      chunkUrl,
      hasHtmlSnapshot: Boolean(bestHtml),
      file: `references/pages/${pageFile}`,
    });
  }

  const apiGenerated = [];
  for (const item of openApiEntries) {
    const chunkUrl = `${assetsBase}/${item.chunk}`;
    const chunkJs = await fetchText(chunkUrl);
    const titleMatch =
      chunkJs.match(/title:\{en:"([^"]+)"/) || chunkJs.match(/title:\{en:'([^']+)'/);
    const title = titleMatch ? titleMatch[1] : item.slug;
    const endpointIds = uniquePreserveOrder(
      [...chunkJs.matchAll(/id:"([^"]+)"/g)].map((m) => m[1])
    );
    const endpointPaths = uniquePreserveOrder(
      [...chunkJs.matchAll(/path:"([^"]+)"/g)].map((m) => m[1])
    );
    const apiFile = `${item.slug.replace(/\//g, "__")}.md`;
    const apiPath = path.join(API_DIR, apiFile);

    const apiContent = [
      `# ${title}`,
      "",
      `- Route: \`${slugToRoute(item.slug)}\``,
      `- Source API mapping path: \`/${item.srcBase}/api.ts\``,
      `- Source chunk: \`${chunkUrl}\``,
      "",
      ...(endpointIds.length
        ? [
            "## Endpoint IDs",
            "",
            ...endpointIds.map((id) => `- \`${id}\``),
            "",
          ]
        : []),
      ...(endpointPaths.length
        ? [
            "## Endpoint Paths",
            "",
            ...endpointPaths.map((p) => `- \`${p}\``),
            "",
          ]
        : []),
      "## Raw API Chunk Source",
      "",
      "```javascript",
      chunkJs,
      "```",
      "",
    ].join("\n");

    fs.writeFileSync(apiPath, apiContent, "utf8");
    apiGenerated.push({
      title,
      slug: item.slug,
      route: slugToRoute(item.slug),
      chunkUrl,
      endpointCount: endpointIds.length,
      file: `references/api/${apiFile}`,
    });
  }

  const grouped = generated.reduce((acc, item) => {
    const section = item.slug.split("/")[0] || "misc";
    if (!acc[section]) {
      acc[section] = [];
    }
    acc[section].push(item);
    return acc;
  }, {});

  const indexLines = [];
  indexLines.push("# Kling Docs Index");
  indexLines.push("");
  indexLines.push(`- Generated at: ${new Date().toISOString()}`);
  indexLines.push(`- Start URL: \`${START_URL}\``);
  indexLines.push(`- Main index JS: \`${indexJsUrl}\``);
  indexLines.push(`- Docs route map chunk: \`${docsChunkUrl}\``);
  if (openApiChunkUrl) {
    indexLines.push(`- OpenAPI chunk: \`${openApiChunkUrl}\``);
  }
  indexLines.push(`- Language: \`${LANG}\``);
  indexLines.push(`- Total pages: **${generated.length}**`);
  indexLines.push(`- API schema files: **${apiGenerated.length}**`);
  indexLines.push("");

  const sectionNames = Object.keys(grouped).sort();
  for (const section of sectionNames) {
    indexLines.push(`## ${section}`);
    indexLines.push("");
    const pages = grouped[section].sort((a, b) => a.slug.localeCompare(b.slug));
    for (const page of pages) {
      indexLines.push(
        `- **${page.title}**: \`${page.route}\` -> \`${page.file}\``
      );
    }
    indexLines.push("");
  }

  if (apiGenerated.length) {
    indexLines.push("## apiSchemas");
    indexLines.push("");
    for (const api of apiGenerated.sort((a, b) => a.slug.localeCompare(b.slug))) {
      indexLines.push(
        `- **${api.title}**: \`${api.route}\` -> \`${api.file}\` (${api.endpointCount} endpoints)`
      );
    }
    indexLines.push("");
  }

  fs.writeFileSync(path.join(REFERENCES_DIR, "index.md"), indexLines.join("\n"), "utf8");
  fs.writeFileSync(
    path.join(REFERENCES_DIR, "index.json"),
    JSON.stringify({
      generatedAt: new Date().toISOString(),
      startUrl: START_URL,
      mainIndexJs: indexJsUrl,
      docsRouteChunk: docsChunkUrl,
      openApiChunk: openApiChunkUrl || null,
      language: LANG,
      total: generated.length,
      apiTotal: apiGenerated.length,
      pages: generated,
      apiSchemas: apiGenerated,
    }, null, 2),
    "utf8"
  );

  console.log(
    `Generated ${generated.length} pages and ${apiGenerated.length} API schema files in ${REFERENCES_DIR}`
  );
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
