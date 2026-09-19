#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function parseArgs(argv) {
  const options = {
    force: false,
    dryRun: false,
    list: false,
    check: false,
    only: null,
    concurrency: 1,
    config: "illustrations/config.json"
  };

  function addOnly(raw) {
    const values = String(raw)
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean);
    if (values.length === 0) {
      throw new Error("--only requires at least one non-empty search term");
    }
    if (!options.only) options.only = new Set();
    for (const value of values) options.only.add(value);
  }

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--force") options.force = true;
    else if (arg === "--dry-run") options.dryRun = true;
    else if (arg === "--list") options.list = true;
    else if (arg === "--check") options.check = true;
    else if (arg === "--only") {
      if (i + 1 >= argv.length) {
        throw new Error("--only requires a value");
      }
      addOnly(argv[++i]);
    } else if (arg.startsWith("--only=")) {
      addOnly(arg.slice("--only=".length));
    } else if (arg.startsWith("--concurrency=")) {
      const value = Number(arg.slice("--concurrency=".length));
      if (!Number.isInteger(value) || value < 1) {
        throw new Error("--concurrency must be a positive integer");
      }
      options.concurrency = value;
    } else if (arg.startsWith("--config=")) {
      options.config = arg.slice("--config=".length);
    } else if (arg === "--help" || arg === "-h") {
      console.log(`Usage: node scripts/generate_illustrations.mjs [options]

Options:
  --dry-run            Show what would be generated or converted without changing files
  --force              Regenerate even when an image already exists
  --list               List parsed illustration entries and exit
  --check              Audit manual prompt titles/dates against current achievements
  --only a,b           Generate only entries whose heading/title contains a or b
  --only=a,b           Same as above; --only may be repeated
  --concurrency=N      Number of concurrent generations (default: 1)
  --config=PATH        Config JSON path (default: illustrations/config.json)
  -h, --help           Show this help

Behavior:
  - Newly generated images are normalized and saved as JPEG (.jpg)
  - Existing .png/.webp/.jpeg images are converted locally to .jpg without an API call
  - Existing .jpg images are skipped unless --force is used
  - forced_negative_terms in config are always appended to the negative prompt

Environment:
  MODELSLAB_API_KEY    Required only when an API generation is needed
  MODELSLAB_MODEL_ID   Optional override for config model_id
`);
      process.exit(0);
    } else {
      throw new Error(`Unknown option: ${arg}`);
    }
  }
  return options;
}

function sanitizeFilename(value) {
  return value
    .normalize("NFKC")
    .replace(/[\\/:*?"<>|]/g, "-")
    .replace(/[\u0000-\u001f]/g, "")
    .replace(/\s+/g, "_")
    .replace(/_+/g, "_")
    .replace(/-+/g, "-")
    .replace(/^[-_.]+|[-_.]+$/g, "")
    .slice(0, 120);
}

function stripLegacyStyle(prompt, fragments = []) {
  let result = prompt;
  for (const fragment of fragments) {
    if (!fragment) continue;
    result = result.replaceAll(fragment, "");
  }
  return result
    .replace(/\s*,\s*,+/g, ", ")
    .replace(/^\s*,\s*|\s*,\s*$/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function extractCodeBlock(body, label) {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const re = new RegExp('\\*\\*' + escaped + '\\*\\*\\s*\\n+```(?:text)?\\s*\\n([\\s\\S]*?)\\n```', 'i');
  const match = body.match(re);
  return match ? match[1].trim() : null;
}

function parsePromptMarkdown(markdown) {
  const headingRe = /^###\s+(.+)$/gm;
  const headings = [...markdown.matchAll(headingRe)];
  const entries = [];
  for (let i = 0; i < headings.length; i += 1) {
    const heading = headings[i][1].trim();
    const start = headings[i].index + headings[i][0].length;
    const end = i + 1 < headings.length ? headings[i + 1].index : markdown.length;
    const body = markdown.slice(start, end);

    const positive = extractCodeBlock(body, "Positive prompt");
    const negative = extractCodeBlock(body, "Negative prompt");
    if (!positive || !negative) continue;
    const separator = heading.indexOf(" — ");
    const date = separator >= 0 ? heading.slice(0, separator).trim() : "undated";
    const title = separator >= 0 ? heading.slice(separator + 3).trim() : heading;
    const baseName = sanitizeFilename(`${date}_${title}`);

    entries.push({ heading, date, title, positive, negative, baseName });
  }

  return entries;
}


function plainText(value) {
  return String(value || "")
    .replace(/<!--[\s\S]*?-->/g, " ")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/[*_~`>#]/g, " ")
    .replace(/\\\|/g, "|")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeDate(value) {
  return String(value || "")
    .normalize("NFKC")
    .replace(/\s+/g, "")
    .replace(/[‐‑‒–—―]/g, "-")
    .replace(/^🔒/, "")
    .trim();
}

function parseAchievementMarkdown(markdown, sourceFile) {
  const entries = [];

  for (const line of markdown.split("\n")) {
    const match = line.match(/^\|([^|]*)\|\s*\*\*(.*?)\*\*\s*\|([^|]*)\|(.*)\|\s*$/);
    if (!match) continue;
    const [, dateRaw, titleRaw, tagsRaw, bodyRaw] = match;
    const title = plainText(titleRaw);
    if (!title) continue;
    entries.push({
      date: plainText(dateRaw),
      title,
      tags: plainText(tagsRaw)
        .split(",")
        .map((value) => value.trim())
        .filter(Boolean),
      body: plainText(bodyRaw),
      sourceFile
    });
  }

  const headingRe = /^###\s+(🔒\s+.+)$/gm;
  const headings = [...markdown.matchAll(headingRe)];
  for (let i = 0; i < headings.length; i += 1) {
    const title = plainText(headings[i][1]);
    const start = headings[i].index + headings[i][0].length;
    const end = i + 1 < headings.length ? headings[i + 1].index : markdown.length;
    const section = markdown.slice(start, end);
    const tagsMatch = section.match(/\*\*タグ:\*\*\s*([^\n]+)/);
    const conditionMatch = section.match(/\*\*解除条件:\*\*\s*([^\n]+)/);
    const tags = tagsMatch
      ? plainText(tagsMatch[1]).split(",").map((value) => value.trim()).filter(Boolean)
      : [];
    const body = plainText(
      [
        conditionMatch ? `解除条件: ${conditionMatch[1]}` : "",
        section
          .replace(/\*\*タグ:\*\*[^\n]*/g, "")
          .replace(/\*\*解除条件:\*\*[^\n]*/g, "")
      ].join(" ")
    );
    entries.push({ date: "未来", title, tags, body, sourceFile });
  }

  return entries;
}

async function loadAchievementEntries(directory) {
  const names = (await fs.readdir(directory))
    .filter((name) => name.endsWith(".md"))
    .sort();
  const entries = [];
  for (const name of names) {
    const sourceFile = path.join(directory, name);
    const markdown = await fs.readFile(sourceFile, "utf8");
    entries.push(...parseAchievementMarkdown(markdown, sourceFile));
  }
  return entries;
}

function isAutoExcluded(achievement, config) {
  const auto = config.auto_prompts || {};
  const sourceName = path.basename(achievement.sourceFile);
  if ((auto.exclude_source_files || []).includes(sourceName)) return true;
  if ((auto.exclude_titles || []).includes(achievement.title)) return true;
  const blockedTags = new Set(auto.exclude_tags || []);
  return achievement.tags.some((tag) => blockedTags.has(tag));
}

function makeAutoPromptEntry(achievement, config) {
  const auto = config.auto_prompts || {};
  const contextLimit = Number(auto.body_max_chars || 900);
  const context = achievement.body.slice(0, contextLimit);
  const themes = achievement.tags.length > 0 ? achievement.tags.join(", ") : "historical context";
  const positive = [
    auto.positive_prefix || "historically grounded editorial scene",
    `achievement title: ${achievement.title}`,
    `period: ${achievement.date || "undated"}`,
    `themes: ${themes}`,
    `factual context: ${context}`,
    "choose a concrete scene, place, object, scientific apparatus, infrastructure, landscape, or non-identifying human activity that communicates the event without copying any known photograph",
    "prefer symbolic material evidence and historically plausible surroundings over exact celebrity portraiture"
  ].join(". ");
  const negative = [
    auto.negative_prefix || "do not imitate any existing film, manga, anime, game, book cover, poster, museum photograph, news photograph, or branded visual identity",
    "no recognizable copyrighted character",
    "no direct recreation of a famous published image",
    "no readable logos or trademarks",
    "no gratuitous gore"
  ].join(", ");

  const heading = `${achievement.date || "undated"} — ${achievement.title}`;
  return {
    heading,
    date: achievement.date || "undated",
    title: achievement.title,
    positive,
    negative,
    baseName: sanitizeFilename(`${achievement.date || "undated"}_${achievement.title}`),
    origin: "auto",
    achievement
  };
}

function mergePromptCoverage(manualEntries, achievementEntries, config) {
  const manualByTitle = new Map();
  const duplicateManual = [];
  for (const entry of manualEntries) {
    if (manualByTitle.has(entry.title)) duplicateManual.push(entry.title);
    manualByTitle.set(entry.title, entry);
  }

  const achievementByTitle = new Map();
  const duplicateAchievements = [];
  for (const achievement of achievementEntries) {
    if (achievementByTitle.has(achievement.title)) duplicateAchievements.push(achievement.title);
    else achievementByTitle.set(achievement.title, achievement);
  }

  const staleManual = manualEntries.filter((entry) => !achievementByTitle.has(entry.title));
  const dateMismatches = [];
  const excluded = [];
  const entries = [];

  for (const achievement of achievementEntries) {
    const manual = manualByTitle.get(achievement.title);
    if (manual) {
      if (
        manual.date !== "undated" &&
        normalizeDate(manual.date) !== normalizeDate(achievement.date)
      ) {
        dateMismatches.push({
          title: achievement.title,
          promptDate: manual.date,
          achievementDate: achievement.date
        });
      }
      entries.push({ ...manual, origin: "manual", achievement });
      continue;
    }

    if (isAutoExcluded(achievement, config)) {
      excluded.push(achievement);
      continue;
    }

    if (config.auto_prompts?.enabled !== false) {
      entries.push(makeAutoPromptEntry(achievement, config));
    }
  }

  return {
    entries,
    staleManual,
    dateMismatches,
    duplicateManual,
    duplicateAchievements,
    excluded
  };
}

function printCoverage(coverage) {
  const manual = coverage.entries.filter((entry) => entry.origin === "manual").length;
  const auto = coverage.entries.filter((entry) => entry.origin === "auto").length;
  console.log(
    `Illustration coverage: manual=${manual}, auto=${auto}, excluded=${coverage.excluded.length}, stale_manual=${coverage.staleManual.length}`
  );
  for (const entry of coverage.staleManual) {
    console.error(`[STALE] prompt title not found in achievements: ${entry.heading}`);
  }
  for (const mismatch of coverage.dateMismatches) {
    console.error(
      `[DATE] ${mismatch.title}: prompt=${mismatch.promptDate}, achievement=${mismatch.achievementDate}`
    );
  }
  for (const title of coverage.duplicateManual) {
    console.error(`[DUP] duplicate manual prompt title: ${title}`);
  }
  for (const title of coverage.duplicateAchievements) {
    console.error(`[DUP] duplicate achievement title: ${title}`);
  }
}

function toPromptTerms(input) {
  if (!input) return [];
  const values = Array.isArray(input) ? input : [input];
  return values
    .flatMap((value) => String(value).split(","))
    .map((value) => value.trim())
    .filter(Boolean);
}

function mergePromptTerms(...sources) {
  const seen = new Set();
  const merged = [];
  for (const source of sources) {
    for (const term of toPromptTerms(source)) {
      const key = term.toLowerCase();
      if (seen.has(key)) continue;
      seen.add(key);
      merged.push(term);
    }
  }
  return merged.join(", ");
}

async function fileExists(file) {
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
}

async function findExistingImage(basePath) {
  for (const ext of [".jpg", ".jpeg", ".png", ".webp"]) {
    const candidate = `${basePath}${ext}`;
    if (await fileExists(candidate)) return candidate;
  }
  return null;
}

function isCanonicalJpg(filePath) {
  return path.extname(filePath).toLowerCase() === ".jpg";
}

let sharpFactory = null;

async function getSharp() {
  if (!sharpFactory) {
    const module = await import("sharp");
    sharpFactory = module.default;
  }
  return sharpFactory;
}

async function convertBufferToJpeg(buffer, outputPath, quality) {
  const sharp = await getSharp();
  await sharp(buffer).jpeg({ quality, mozjpeg: true }).toFile(outputPath);
  return outputPath;
}

async function convertFileToJpeg(inputPath, outputPath, quality) {
  const sharp = await getSharp();
  await sharp(inputPath).jpeg({ quality, mozjpeg: true }).toFile(outputPath);
  return outputPath;
}

async function postJson(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  const text = await response.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error(`ModelsLab returned non-JSON (${response.status}): ${text.slice(0, 500)}`);
  }

  if (!response.ok) {
    throw new Error(`ModelsLab HTTP ${response.status}: ${JSON.stringify(json).slice(0, 1000)}`);
  }

  return json;
}

async function waitForOutputs(initial, apiKey, config) {
  let data = initial;
  for (let attempt = 0; attempt <= config.max_poll_attempts; attempt += 1) {
    if (data.status === "success" && Array.isArray(data.output) && data.output.length > 0) {
      return data.output;
    }

    if (Array.isArray(data.output) && data.output.length > 0) {
      return data.output;
    }

    if (data.status === "error" || data.status === "failed") {
      throw new Error(data.message || data.messege || "ModelsLab generation failed");
    }
    if (data.status !== "processing" || !data.fetch_result) {
      throw new Error(`Unexpected ModelsLab response: ${JSON.stringify(data).slice(0, 1500)}`);
    }

    if (attempt === config.max_poll_attempts) {
      throw new Error(`Timed out waiting for ModelsLab result after ${config.max_poll_attempts} polls`);
    }

    await new Promise((resolve) => setTimeout(resolve, config.poll_interval_ms));
    data = await postJson(data.fetch_result, { key: apiKey });
  }
  throw new Error("Unexpected polling termination");
}

async function downloadAndConvertToJpeg(url, outputPath, quality) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to download generated image: HTTP ${response.status}`);
  }

  const bytes = Buffer.from(await response.arrayBuffer());
  return convertBufferToJpeg(bytes, outputPath, quality);
}

function matchesOnly(entry, onlySet) {
  if (!onlySet) return true;
  const haystack = `${entry.heading}\n${entry.title}\n${entry.baseName}`.toLowerCase();
  return [...onlySet].some((needle) => haystack.includes(needle.toLowerCase()));
}

async function generateEntry(entry, context) {
  const { config, options, apiKey, modelId } = context;
  const basePath = path.join(config.output_dir, entry.baseName);
  const jpgPath = `${basePath}.jpg`;
  const existing = await findExistingImage(basePath);
  if (existing && !options.force) {
    if (isCanonicalJpg(existing)) {
      return { status: "skipped", entry, file: existing };
    }

    if (options.dryRun) {
      return { status: "dry-convert", entry, source: existing, file: jpgPath };
    }
    const converted = await convertFileToJpeg(existing, jpgPath, config.jpeg_quality);
    if (config.remove_source_after_jpeg !== false && existing !== converted) {
      await fs.unlink(existing);
    }
    return { status: "converted", entry, source: existing, file: converted };
  }

  const scenePositive = stripLegacyStyle(entry.positive, config.strip_legacy_style_fragments);
  const sceneNegative = stripLegacyStyle(entry.negative, []);
  const positive = mergePromptTerms(
    config.common_positive,
    config.forced_positive_terms,
    scenePositive
  );
  const negative = mergePromptTerms(
    config.common_negative,
    config.forced_negative_terms,
    sceneNegative
  );

  if (options.dryRun) {
    return { status: "dry-run", entry, positive, negative, file: jpgPath };
  }

  const payload = {
    key: apiKey,
    model_id: modelId,
    prompt: positive,
    negative_prompt: negative,
    width: config.width,
    height: config.height,
    samples: config.samples
  };

  for (const key of ["num_inference_steps", "guidance_scale", "seed"]) {
    if (config[key] !== undefined && config[key] !== null) payload[key] = config[key];
  }

  const initial = await postJson(config.endpoint, payload);
  const outputs = await waitForOutputs(initial, apiKey, config);
  const files = [];
  for (let i = 0; i < outputs.length; i += 1) {
    const suffix = outputs.length > 1 ? `_${i + 1}` : "";
    files.push(
      await downloadAndConvertToJpeg(
        outputs[i],
        `${basePath}${suffix}.jpg`,
        config.jpeg_quality
      )
    );
  }
  const metadata = {
    heading: entry.heading,
    title: entry.title,
    date: entry.date,
    model_id: modelId,
    width: config.width,
    height: config.height,
    format: "jpg",
    jpeg_quality: config.jpeg_quality,
    files,
    generated_at: new Date().toISOString(),
    prompt: positive,
    negative_prompt: negative
  };
  await fs.writeFile(`${basePath}.meta.json`, `${JSON.stringify(metadata, null, 2)}\n`, "utf8");

  return { status: "generated", entry, files, prompt: positive, negative_prompt: negative };
}

async function runPool(items, concurrency, worker) {
  const results = new Array(items.length);
  let next = 0;
  async function run() {
    while (true) {
      const index = next;
      next += 1;
      if (index >= items.length) return;
      try {
        results[index] = await worker(items[index]);
      } catch (error) {
        results[index] = {
          status: "error",
          entry: items[index],
          error: error instanceof Error ? error.message : String(error)
        };
      }
    }
  }

  await Promise.all(Array.from({ length: concurrency }, () => run()));
  return results;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const config = JSON.parse(await fs.readFile(options.config, "utf8"));
  const source = await fs.readFile(config.prompt_source, "utf8");
  const manualEntries = parsePromptMarkdown(source);
  const achievementDir = config.auto_prompts?.achievement_dir || "achievements";
  const achievementEntries = await loadAchievementEntries(achievementDir);
  const coverage = mergePromptCoverage(manualEntries, achievementEntries, config);
  const allEntries = coverage.entries;
  const entries = allEntries.filter((entry) => matchesOnly(entry, options.only));

  if (allEntries.length === 0) {
    throw new Error(`No illustration entries found from ${config.prompt_source} and ${achievementDir}`);
  }

  if (options.check) {
    printCoverage(coverage);
    for (const item of coverage.excluded) {
      console.log(`[EXCLUDE] ${item.title} (${path.basename(item.sourceFile)})`);
    }
    if (
      coverage.staleManual.length > 0 ||
      coverage.dateMismatches.length > 0 ||
      coverage.duplicateManual.length > 0 ||
      coverage.duplicateAchievements.length > 0
    ) {
      process.exitCode = 1;
    }
    return;
  }

  if (options.list) {
    printCoverage(coverage);
    for (const entry of entries) {
      console.log(`[${entry.origin.toUpperCase()}]\t${entry.baseName}\t${entry.heading}`);
    }
    return;
  }

  const apiKey = process.env.MODELSLAB_API_KEY;
  if (!options.dryRun && !apiKey) {
    const allApiFree = await Promise.all(
      entries.map(async (entry) => {
        const basePath = path.join(config.output_dir, entry.baseName);
        const existing = await findExistingImage(basePath);
        return Boolean(existing && !options.force);
      })
    );
    if (!allApiFree.every(Boolean)) {
      throw new Error("MODELSLAB_API_KEY is required because at least one selected image must be generated.");
    }
  }

  const modelId = process.env.MODELSLAB_MODEL_ID || config.model_id;
  await fs.mkdir(config.output_dir, { recursive: true });

  const manualCount = allEntries.filter((entry) => entry.origin === "manual").length;
  const autoCount = allEntries.filter((entry) => entry.origin === "auto").length;
  console.log(`Prepared ${allEntries.length} illustration entries (manual=${manualCount}, auto=${autoCount}); selected ${entries.length}.`);
  console.log(`Model: ${modelId}; output: ${config.output_dir}; format: jpg`);
  if (Array.isArray(config.forced_negative_terms) && config.forced_negative_terms.length > 0) {
    console.log(`Forced negative terms: ${config.forced_negative_terms.join(", ")}`);
  }

  const results = await runPool(entries, options.concurrency, (entry) =>
    generateEntry(entry, { config, options, apiKey, modelId })
  );
  let errors = 0;
  for (const result of results) {
    if (result.status === "skipped") {
      console.log(`[SKIP] ${result.entry.heading} -> ${result.file}`);
    } else if (result.status === "converted") {
      console.log(`[JPG]  ${result.entry.heading} -> ${result.file} (from ${result.source})`);
    } else if (result.status === "dry-convert") {
      console.log(`[DRY]  ${result.entry.heading} -> convert ${result.source} => ${result.file}`);
    } else if (result.status === "dry-run") {
      console.log(`[DRY]  ${result.entry.heading} -> ${result.file}`);
    } else if (result.status === "generated") {
      console.log(`[OK]   ${result.entry.heading} -> ${result.files.join(", ")}`);
    } else if (result.status === "error") {
      errors += 1;
      console.error(`[ERR]  ${result.entry.heading}: ${result.error}`);
    }
  }
  const summary = results.reduce((acc, result) => {
    acc[result.status] = (acc[result.status] || 0) + 1;
    return acc;
  }, {});
  console.log(`Summary: ${JSON.stringify(summary)}`);

  if (errors > 0) process.exitCode = 1;
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : error);
  process.exit(1);
});
